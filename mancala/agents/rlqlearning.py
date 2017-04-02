# -*- coding: utf-8 -*-

"""
Q Learning Agent for the Mancala AI
"""

import random
from .agent import Agent
from .random import AgentRandom
from ..game import Game
from ..arena import Arena


class AgentRL_QLearning(Agent):
    """Reinforcement Q Learning Class for play Mancala."""

    def __init__(self, seed=451, action_values=None):
        self._seed = seed
        self._idx = 0
        self._action_values = {} if action_values is None else action_values

    def _state(self, game):
        """Return the derived state from a game"""
        raise NotImplementedError("Class {} doesn't implement _state()".format(
            self.__class__.__name__))

    def do_learn(self,
                 action_values=None,
                 epochs=100,
                 games_per_epoch=100,
                 other_agent=AgentRandom(451),
                 alpha=0.1,
                 gamma=0.1,
                 decay=0.1,  # lambda
                 epsilon=0.1):
        """Do learning for a specific class"""
        raise NotImplementedError("Class {} doesn't implement do_learn()".format(
            self.__class__.__name__))

    def _move(self, game):
        """Return the move"""
        self._idx = self._idx + 1
        random.seed(self._seed + self._idx)
        game_clone, rotation_flag = game.clone_turn()
        state_current = self._state(game_clone)

        options = Agent.valid_indices(game_clone)
        if len(options) < 1:
            return 0  # TODO: conform this to standard

        if state_current not in self._action_values:
            # guess if state unknown
            pick = random.choice(options)
        else:
            action_value = self._action_values[state_current]
            pick = AgentRL_QLearning.weighted_pick_filter(
                action_value, options)

        final_move = Game.rotate_board(rotation_flag, pick)
        return final_move

    def learn(self,
              create_new_agent,
              action_values=None,
              epochs=100,
              games_per_epoch=100,
              other_agent=AgentRandom(451),
              alpha=0.1,
              gamma=0.1,
              decay=0.1,  # lambda
              epsilon=0.1,
              update_period=10,
              update_callback=None):
        """Learn action values over epochs"""
        for epoch in range(epochs):
            self._idx = self._idx + 1
            agent = other_agent if action_values is None else \
                create_new_agent(self._idx + 1, action_values)
            action_values = self._learn_values(action_values,
                                               games_per_epoch,
                                               agent,
                                               alpha,
                                               gamma,
                                               decay,  # lambda
                                               epsilon)
            if update_callback is None:
                continue
            if epoch % update_period == 0:
                arena = Arena([
                    ("Random", lambda seed: AgentRandom(seed)),
                    ("QLearner", lambda seed: create_new_agent(
                        seed, action_values))
                ], 501)
                results = arena.results()
                result = [result for result in results if
                          result[0] == "Random" and result[1] == "QLearner"][0][2]
                win_rate_v_random = round(100 * (501 - result) / 501, 2)
                msg = "Epoch {: >3} Complete | Win Rate: {: >4}% | States: {: 5}".format(
                    epoch, win_rate_v_random, len(action_values))
                update_callback(
                    (epoch, win_rate_v_random, len(action_values), msg))

        return action_values

    @staticmethod
    def generate_states(
            games=100,
            agent_01=AgentRandom(451),
            agent_02=AgentRandom(451)):
        """Generate games from agents acting"""
        boards = {}
        for _ in range(0, games):
            game = Game()
            while not game.over():
                boards = AgentRL_QLearning._add_to_key(
                    boards, str(game.board()))
                if game.turn_player() == 1:
                    game.move(agent_01.move(game))
                else:
                    game.move(agent_02.move(game))

            # record last state
            boards = AgentRL_QLearning._add_to_key(
                boards, str(game.board()))

        return boards

    @staticmethod
    def _pick_action(action_values, state, epsilon, seed=451):
        """Pick an action based on the values"""
        random.seed(seed)
        action_values = AgentRL_QLearning._ensure_exists(action_values, state)
        if random.uniform(0, 1) < epsilon:
            # pick a random slot
            return random.choice(range(0, 6)), action_values
        values = action_values[state]
        return AgentRL_QLearning.max_pick(values, seed), action_values

    @staticmethod
    def _take_action(game, action, agent):
        """Given a game (ie state) and an action, return the new state and reward"""
        scores_before = game.score()
        game.move(action)
        while game.turn_player() != 1 and not game.over():
            game.move(agent.move(game))
        scores_after = game.score()
        if game.over():
            return (game, (50 if scores_after[0] > scores_after[1] else -50))
        reward = (scores_after[0] - scores_before[0]) - \
            (scores_after[1] - scores_before[1]) * \
            0.5  # attenuate other player's score
        return game, reward

    def _learn_values(
            self,
            action_values=None,
            games_to_play=100,
            other_agent=AgentRandom(451),
            alpha=0.1,
            gamma=0.1,
            decay=0.1,  # lambda
            epsilon=0.1):
        """Generate an updated action_values from playing"""
        action_values = {} if action_values is None else action_values  # Q
        self._idx = self._idx + 1
        random.seed(self._seed + self._idx)

        for _ in range(games_to_play):
            game = Game()
            state_current = self._state(game)
            action_current, action_values = AgentRL_QLearning._pick_action(
                action_values, state_current, epsilon, self._idx)
            eligibility_trace = {}  # reset on every game

            while not game.over():
                self._idx = self._idx + 1
                game, reward = AgentRL_QLearning._take_action(
                    game, action_current, other_agent)
                state_next = self._state(game)

                # Ensure both states exist in the action space
                action_values = AgentRL_QLearning._ensure_exists(
                    action_values, state_next)
                eligibility_trace = AgentRL_QLearning._ensure_exists(
                    eligibility_trace, state_next)

                action_next, action_values = AgentRL_QLearning._pick_action(
                    action_values,
                    state_current,
                    epsilon,
                    self._idx)

                delta = reward + gamma * \
                    action_values[state_next][action_next] - \
                    action_values[state_current][action_current]

                eligibility_trace = AgentRL_QLearning._ensure_exists(
                    eligibility_trace, state_current)
                eligibility_trace[state_current][action_current] = eligibility_trace[
                    state_current][action_current] + 1

                for state in action_values.keys():
                    for idx in range(6):
                        # only bother to decay an eligibility trace if we have it
                        # otherwise it's zero
                        if state not in eligibility_trace:
                            continue

                        action_values[state][idx] = action_values[state][idx] \
                            + alpha * delta * eligibility_trace[state][idx]
                        eligibility_trace[state][idx] = gamma * \
                            decay * eligibility_trace[state][idx]

                action_current = action_next
                state_current = state_next

        return action_values

    @staticmethod
    def _ensure_exists(dictionary, key, value=None):
        """Ensures a key exists in a dictionary"""
        value = [0] * 6 if value is None else value
        if key not in dictionary:
            dictionary[key] = value
        return dictionary

    @staticmethod
    def _add_to_key(dictionary, key):
        if key in dictionary:
            dictionary[key] = dictionary[key] + 1
        else:
            dictionary[key] = 1
        return dictionary

    @staticmethod
    def weighted_pick_filter(values, valid_indices, seed=451):
        """Make a weighted pick, choosing randomly if all equal. Only uses valid indices."""
        values_available = [(idx, value) for idx, value in enumerate(
            values) if idx in valid_indices]
        values_valid = [value for idx, value in values_available]
        picked_valid = AgentRL_QLearning.weighted_pick(values_valid, seed)
        real_index = values_available[picked_valid][0]
        return real_index

    @staticmethod
    def weighted_pick(values, seed=451):
        """Make a weighted pick, choosing randomly if all equal"""
        random.seed(seed)

        # action_max = [1 if i == max(values) else 0 for i in values]
        values_floor = [value - min(values) for value in values]
        if all(value == 0 for value in values_floor):
            return random.choice(range(0, len(values)))

        action_fraction = [value / sum(values_floor) for value in values_floor]
        total = 0
        pick = random.uniform(0, 1)
        for action, value in enumerate(action_fraction):
            total = total + value
            if total >= pick:
                return action

        return 0  # TODO: should this raise?

    @staticmethod
    def max_pick(values, seed=451):
        """Make a weighted pick, choosing randomly if all equal"""
        values_max = [1 if i == max(values) else 0 for i in values]
        return AgentRL_QLearning.weighted_pick(values_max, seed)
