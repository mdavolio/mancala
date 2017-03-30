# -*- coding: utf-8 -*-

"""
Q Learning Agent for the Mancala AI
"""

import random
from .agent import Agent
from .random import AgentRandom
from ..game import Game


class AgentRL_QLearning(Agent):
    """Reinforcement Q Learning Class for play Mancala."""

    def __init__(self, seed=451):
        self._seed = seed
        self._idx = 0

    def _state(self, game):
        """Return the derived state from a game"""
        raise NotImplementedError("Class {} doesn't implement _state()".format(
            self.__class__.__name__))

    def _move(self, game):
        """Return the move"""
        self._idx = self._idx + 1
        random.seed(self._seed + self._idx)

        options = Agent.valid_indices(game)
        if len(options) < 1:
            return 0

        return random.choice(options)

    # @staticmethod
    # def learn(other_agent=AgentRandom(451)):
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
    def _pick_action(action_values, state, epsilon):
        """Pick an action based on the values"""
        action_values = AgentRL_QLearning._ensure_exists(action_values, state)
        if random.uniform(0, 1) < epsilon:
            return random.choice(range(0, 6)), action_values  # pick a random slot
        values = action_values[state]
        action_max = [1 if i == max(values) else 0 for i in values]
        action_fraction = [i / sum(action_max) for i in action_max]
        total = 0
        pick = random.uniform(0, 0.99999)
        for action, value in enumerate(action_fraction):
            total = total + value
            if total >= pick:
                return action, action_values

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
            (scores_after[1] - scores_before[1]) * 0.5 # attenuate other player's score
        return game, reward

    def learn_policy(
            self,
            games_to_play=100,
            action_values=None,
            other_agent=AgentRandom(451),
            alpha=0.1,
            gamma=0.1,
            decay=0.1,  # lambda
            epsilon=0.1):
        """Generate an updated action_values from playing"""
        action_values = {} if action_values is None else action_values  # Q
        eligibility_trace = {}  # e
        self._idx = self._idx + 1
        random.seed(self._seed + self._idx)

        for _ in range(0, games_to_play):
            game = Game()
            state_current = self._state(game)
            action_current, action_values = AgentRL_QLearning._pick_action(
                action_values, state_current, epsilon)

            while not game.over():
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
                    epsilon)

                delta = reward + gamma * \
                    action_values[state_next][action_next] - \
                    action_values[state_current][action_current]

                eligibility_trace = AgentRL_QLearning._ensure_exists(
                    eligibility_trace, state_current)
                eligibility_trace[state_current][action_current] = eligibility_trace[
                    state_current][action_current] + 1

                for state in action_values.keys():
                    for idx in range(0, 6):
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
