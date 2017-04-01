# -*- coding: utf-8 -*-
"""
Mancala Arena object
"""

import itertools
from mancala.game import Game


class Arena():
    """
    Pairs agents and compares performance.

    Note that agents must be of a list of tuples of the form:
    `(agent_str, agent_lambda)`

    Where `agent_str` is the display name of the agent and
    `agent_lambda` is a lambda function that takes **only** a random
    seed to create a new object of the agent
    """

    def __init__(self,
                 agents=None,
                 games_to_play=101,
                 verbose=False):
        self._agents = agents if agents is list else []
        self._games_to_play = games_to_play
        self._names = list(sorted(map(lambda t: t[0], agents)))

        # this ensures all agent pairs and pairs with themselves
        combos = list(itertools.combinations(agents, 2)) + \
            list(zip(agents, agents))
        self._combos = sorted(combos, key=lambda t: t[0][0] + '_' + t[1][0])
        self._results = list(map(lambda t: Arena._handle_combo(
            t[1], t[0], games_to_play), enumerate(self._combos)))

    @staticmethod
    def _handle_combo(combo, seed, games_to_play):
        wins = 0
        for idx in range(0, games_to_play):
            game = Game()
            agent_one = (combo[0][1])(seed + idx)
            agent_two = (combo[1][1])(seed + idx)
            while not game.over():
                if game.turn_player() == 1:
                    game.move(agent_one.move(game))
                else:
                    game.move(agent_two.move(game))
            if game.score()[0] > game.score()[1]:
                wins = wins + 1
        return (combo[0][0], combo[1][0], wins)

    def names(self):
        """Sorted names of agents"""
        return self._names[:]

    def results(self):
        """Sorted results of agents"""
        return self._results[:]
