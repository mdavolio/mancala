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
        if (game.board()[idx] % 13) == (6 - idx):
            return 1
        return 0

    @staticmethod
    def _score_of_move(move_test, game):
        """Makes the move and returns the score of player one"""
        game.move(move_test)
        return game.score()[0]

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

        available_scores = list(map(lambda move_slot:
                                    AgentExact._score_of_move(
                                        move_slot,
                                        game_clone.clone()
                                    ),
                                    move_options))

        final_options = [move for exact, move in
                         zip(distance, move_options)
                         if exact == 1]

        if not final_options:
            score_max = max(available_scores)
            final_options = [move for score, move in
                             zip(available_scores, move_options)
                             if score == score_max]
            final_move = Game.rotate_board(rot_flag, random.choice(final_options))
        else:
            final_move = Game.rotate_board(rot_flag, max(final_options))

        return final_move
