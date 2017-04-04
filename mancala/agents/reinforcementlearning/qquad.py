# -*- coding: utf-8 -*-

"""
RL Learning, Q learning with binary space Agent for the a Mancala AI
"""

from ..rlqlearning import AgentRL_QLearning
from ..random import AgentRandom


class AgentQQuad(AgentRL_QLearning):
    """
    RL Learning, Q learning with quad space Agent for the a Mancala AI
    Slots are either 0,1,2-3, or more
    """

    def _state(self, game):
        """Return the derived state from a game"""
        board = game.board()
        board_relevant = board[0:6] + board[7:13]
        board_str = str([AgentQQuad._slot(i) for i in board_relevant])
        return board_str.replace(' ', '') \
                        .replace('[', '') \
                        .replace(']', '')

    @staticmethod
    def _slot(stones):
        if stones == 0:
            return 0
        if stones == 1:
            return 1
        if stones > 1 and stones < 4:
            return 2
        return 3

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
        return self.learn(lambda seed, a_vs: AgentQQuad(seed, a_vs),
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
