# -*- coding: utf-8 -*-

"""
Abstract Agent for the a Mancala AI
"""


class Agent():
    """Abstract Class for agent to play Mancala."""

    def move(self, game=None):
        """Return a move index based on a game"""
        return self._move(game)

    def _move(self, game):
        """Return a move index based on a game"""
        raise NotImplementedError("Class {} doesn't implement _move()".format(
            self.__class__.__name__))
