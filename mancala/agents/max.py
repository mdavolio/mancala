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

    @staticmethod
    def _checkMax(move_test, game):

        game.move(move_test)

        return game.score()[game.turn_player() - 1]

    def _move(self, game):
        """Return a random valid move"""
        self._idx = self._idx + 1
        random.seed(self._seed + self._idx)
        myGame, rot_flag = game.clone_turn()
        
        options = Agent.valid_indices(myGame)

        max_score = list(map(lambda move_slot: AgentMax._checkMax(move_slot, game.clone()), options))
        # return max_score

        maxs = max(max_score)
        final_opts = [i for i, j in enumerate(max_score) if j == maxs]

        final_move = Game.rotate_board(rot_flag, random.choice(final_opts))
        return final_move
