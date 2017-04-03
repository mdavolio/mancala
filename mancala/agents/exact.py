# -*- coding: utf-8 -*-

"""
Abstract Agent for the a Mancala AI

Exact score: If move allows for last stone to end in
                score shell, make move
"""

import random
from mancala.game import Game
from .agent import Agent


class AgentExact(Agent):
    '''Agent which picks a move by the next score'''

    def __init__(self, seed=451):
        self._seed = seed
        self._idx = 0

    @staticmethod
    def _hole_to_score(idx, game):
        if (game.board[idx] % 13) == (6 - idx):
            return 1
        return 0

    def _move(self, game):
        '''Return move which ends in score hole'''
        self._idx = self._idx + 1
        random.seed(self._seed + self._idx)
        game_clone, rot_flag = game.clone_turn()

        move_options = Agent.valid_indices(game_clone)


        distance = list(map(lambda move_slot:
                            AgentExact._hole_to_score(
                                move_slot,
                                game_clone.clone()
                            ),
                            move_options))

        final_options = [i for i, j in enumerate(distance) if j == 1]

        final_move = Game.rotate_board(rot_flag, random.choice(final_options))
        return final_move
