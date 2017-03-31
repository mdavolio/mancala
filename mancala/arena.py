# -*- coding: utf-8 -*-
"""
Mancala Arena object
"""

import itertools


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
        combos = list(itertools.combinations(agents, 2)) + list(zip(agents, agents))
        self._combos = sorted(combos, key=lambda t: t[0][0] + '_' + t[1][0])

    def names(self):
        """Sorted names of agents"""
        return self._names[:]
