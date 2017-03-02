# -*- coding: utf-8 -*-

"""
Abstract Agent for the a Mancala AI
"""

PLAYER_ONE_SPACES = [True, True, True, True, True, True, False,
                     False, False, False, False, False, False, False]
PLAYER_TWO_SPACES = [False, False, False, False, False, False,
                     False, True, True, True, True, True, True, False]


class Agent():
    """Abstract Class for agent to play Mancala."""

    def move(self, game=None):
        """Return a move index based on a game"""
        return self._move(game)

    def _move(self, game):
        """Return a move index based on a game"""
        raise NotImplementedError("Class {} doesn't implement _move()".format(
            self.__class__.__name__))

    @staticmethod
    def valid_indices(game):
        """Returns valid moves based on a current game"""

        board = game.board()
        spaces = PLAYER_ONE_SPACES if game.turn_player() == 1 else PLAYER_TWO_SPACES

        valid_spaces = map(lambda t: t[0] and t[1] > 0, zip(spaces, board))
        possible_indices = map(lambda p: p[0] if p[1] else None, zip(range(0, 13), valid_spaces))
        only_indices = filter(lambda idx: idx is not None, possible_indices)
        valid_indices = list(only_indices)

        return valid_indices
