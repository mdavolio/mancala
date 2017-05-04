
import numpy as np
import gym
from gym import spaces
from gym.utils import seeding

from .game import Game
from .agents.random import AgentRandom
from .agents.exact import AgentExact
from .agents.max_min import AgentMinMax


class MancalaEnv(gym.Env):
    """Mancala Game Environment"""

    def __init__(self, seed=451, agents=None, weights=None):
        self._seed(seed)

        self.action_space = spaces.Discrete(6)
        self.observation_space = spaces.Box(low=0, high=1, shape=(12,))

        if agents is None and weights is None:
            agents = np.array([
                AgentRandom(seed),
                AgentExact(seed),
                AgentMinMax(seed, 3)
            ])
            weights = np.array([1 / 20, 9 / 20, 10 / 20])

        self._agents = agents
        self._weights = weights / sum(weights)
        self._game = None
        self._reset()

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _step(self, action):
        assert self.action_space.contains(action)

        state_init = MancalaEnv.game_state(self._game)
        score_init = self._game.score()
        options = self._agents[0].valid_indices(self._game)

        if action not in options:
            # print("Wrong move penalty")
            return state_init, -5, self._game.over(), {}

        self._game.move(action)

        agent = self.np_random.choice(self._agents, 1, p=self._weights)[0]
        while not self._game.over() and self._game.turn_player() == 2:
            move = agent.move(self._game)
            self._game.move(move)

        state_new = MancalaEnv.game_state(self._game)
        score_new = self._game.score()
        if self._game.over() and score_new[0] > score_new[1]:
            # print("Player 0 wins!")
            reward = 100
        elif self._game.over():
            # print("Player 1 wins!")
            reward = -100
        else:
            reward = score_new[0] - score_init[0] - 0.2

        return state_new, reward, self._game.over(), {}

    def _reset(self):
        self._game = Game()
        return MancalaEnv.game_state(self._game)

    def force(self, game):
        """Force the environment to a certain game state"""
        self._game = game
        return MancalaEnv.game_state(self._game)

    @staticmethod
    def game_state(game):
        """Returns np.array of board state"""
        board = game.board()
        b = board[0:6] + board[7:13]
        s = [MancalaEnv._board_index_to_hot_encoding(count) for count in b]
        return np.array(s).flatten()

    @staticmethod
    def _board_index_to_hot_encoding(count, count_max=48):
        count = count if count < count_max else count_max
        return np.bincount([count], minlength=count_max)[:count_max]
