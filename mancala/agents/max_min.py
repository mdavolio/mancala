# -*- coding: utf-8 -*-

"""
Abstract Agent for the a Mancala AI

Max-Min Agent
"""

import random
from mancala.game import Game
from .agent import Agent


class AgentMinMax(Agent):
    """Agent which picks a move by the next score"""

    def __init__(self, seed=451, depth=4):
        self._seed = seed
        self._idx = 0
        self._depth = depth

    @staticmethod
    def _score_of_move(move_test, game):
        """Makes the move and returns the score of player one"""
        game.move(move_test)
        return game.score()[0]

    @staticmethod
    def _evaluate_board(game):
        return game.score()[game.turn_player() - 1]

    @staticmethod
    def _min_max_move(depth, game, player, move):
        clone = game.clone()
        clone.move(move)
        return AgentMinMax._min_max(depth, clone, player)

    def _move(self, game):
        """Return best value from Min_Max"""
        self._idx = self._idx + 1
        random.seed(self._seed + self._idx)
        game_clone, rot_flag = game.clone_turn()

        move_options = Agent.valid_indices(game_clone)

        available_scores = list(
            map(lambda move_slot:
                AgentMinMax._min_max_move(
                    self._depth,
                    game_clone,
                    True,
                    move_slot
                ),
                move_options))

        score_max = max(available_scores)
        final_options = [move for score, move in
                         zip(available_scores, move_options)
                         if score == score_max]

        final_move = Game.rotate_board(rot_flag, random.choice(final_options))
        return final_move

    @staticmethod
    def _min_max(depth, game, player):

        if depth == 0:
            return -AgentMinMax._evaluate_board(game)

        move_options = Agent.valid_indices(game)

        available_scores = list(
            map(lambda move_slot:
                AgentMinMax._min_max_move(
                    depth - 1,
                    game,
                    not player,
                    move_slot
                ),
                move_options))

        if player:
            return max(available_scores)
        else:
            return min(available_scores)
