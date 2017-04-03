# -*- coding: utf-8 -*-

"""
RL Learning, Q learning with binary space Agent for the a Mancala AI
"""

from ..rlqlearning import AgentRL_QLearning
from ..random import AgentRandom


class AgentQBinary(AgentRL_QLearning):
    """RL Learning, Q learning with binary space Agent for the a Mancala AI"""

    def _state(self, game):
        """Return the derived state from a game"""
        board = game.board()
        board_relevant = board[0:6] + board[7:13]
        board_str = str([1 if i > 0 else 0 for i in board_relevant])
        return board_str.replace(' ', '') \
                        .replace('[', '') \
                        .replace(']', '')

    def do_learn(self,
                 action_values=None,
                 epochs=100,
                 games_per_epoch=100,
                 other_agent=AgentRandom(451),
                 alpha=0.1,
                 gamma=0.1,
                 decay=0.1,  # lambda
                 epsilon=0.1,
                 update_period=10,
                 update_callback=None):
        """Do learning for QBinary"""
        return self.learn(lambda seed, a_vs: AgentQBinary(seed, a_vs),
                          action_values,
                          epochs,
                          games_per_epoch,
                          other_agent,
                          alpha,
                          gamma,
                          decay,  # lambda
                          epsilon,
                          update_period,
                          update_callback)
