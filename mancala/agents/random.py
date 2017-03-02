# -*- coding: utf-8 -*-

"""
Abstract Agent for the a Mancala AI
"""

import random
from .agent import Agent


class AgentRandom(Agent):
    """Random Player Class for play Mancala."""

    def __init__(self, seed=451):
        self._seed = seed
        self._idx = 0

    def _move(self, game):
        """Return a random valid move"""
        self._idx = self._idx + 1
        random.seed(self._seed + self._idx)

        return random.choice(Agent.valid_indices(game))

