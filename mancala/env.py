
import numpy as np
import gym
from gym import spaces
from gym.utils import seeding

from .game import Game
from .agents.exact import AgentExact


class MancalaEnv(gym.Env):
    """Mancala Game Environment"""

    def __init__(self, agent_other, seed=451):

        self.action_space = spaces.Discrete(6)
        self.observation_space = spaces.Box(low=0, high=1, shape=(12,))

        self._agent_other = AgentExact(
            seed) if agent_other is None else agent_other
        self._seed(seed)
        self._game = None
        self._reset()

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _step(self, action):
        assert self.action_space.contains(action)

        state_init = MancalaEnv.game_state(self._game)
        score_init = self._game.score()
        options = self._agent_other.valid_indices(self._game)

        if action not in options:
            return state_init, -5, self._game.over(), {}

        self._game.move(action)

        while not self._game.over() and self._game.turn_player() == 2:
            move = self._agent_other.move(self._game)
            self._game.move(move)

        state_new = MancalaEnv.game_state(self._game)
        score_new = self._game.score()
        if self._game.over() and score_new[0] > score_new[1]:
            reward = 100
        elif self._game.over():
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
        return np.array(board[0:6] + board[7:13]) / 48
