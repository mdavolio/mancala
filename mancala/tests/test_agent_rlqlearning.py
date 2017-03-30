# -*- coding: utf-8 -*-
"""
Tests for the abstract agent class
"""

import unittest
from mancala.agents.random import AgentRandom
from mancala.agents.reinforcementlearning.qbinary import AgentQBinary
from mancala.game import Game


class TestAgentRLQLearning(unittest.TestCase):
    """Tests for the RL Q-Learning Agent class"""


    def test_learning_small(self):
        """Do some small learning with Random opponent"""
        agent = AgentQBinary()
        values = agent.learn_policy(2)
        self.assertEqual(len(values), 37)
        for action_values in values.values():
            self.assertEqual(len(action_values), 6)


if __name__ == '__main__':
    unittest.main()
