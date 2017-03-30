# -*- coding: utf-8 -*-

"""
RL Learning, Q learning with binary space Agent for the a Mancala AI
"""

from ..rlqlearning import AgentRL_QLearning


class AgentQBinary(AgentRL_QLearning):
    """RL Learning, Q learning with binary space Agent for the a Mancala AI"""

    def _state(self, game):
        """Return the derived state from a game"""
        board = game.board()
        board_relevant = board[0:6] + board[7:13]
        board_str = str([1 if i > 0 else 0 for i in board_relevant])
        return board_str.replace(' ', '') \
                        .replace('[', '') \
                        .replace(']', '') \
                        .replace(',', '')
