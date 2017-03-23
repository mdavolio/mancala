# -*- coding: utf-8 -*-

"""
Abstract Agent for the a Mancala AI

Maximize score: test each possible legal move, creating list of score after
                each move, chooses move that maximizes score, if tie random
"""

from .agent import Agent
from mancala.game import Game
import random


class AgentMax(Agent):

    def __init__(self, seed=451):
        self._seed = seed
        self._idx = 0

    def _checkMax(move_test):
        board = game.board()

        game.move(move_test)

        if game.turn_player() == 1:
            max_score[move_test] = game.score()[0]
        else:
            max_score[move_test] = game.score()[1]

        return max_score

    def _move(self, game):
        """Return a random valid move"""
        self._idx = self._idx + 1
        random.seed(self._seed + self._idx)

        max_score = []
        options = Agent.valid_indices(game)

        if len(options) < 1:
            return 0

        map(_checkMax, options)

        maxs = max(max_score)
        [i for i, j in enumerate(max_score) if j == maxs]


        return random.choice(maxs)
