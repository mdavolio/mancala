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
        values = agent.do_learn(epochs=2, games_per_epoch=5)
        self.assertEqual(len(values), 160)
        for action_values in values.values():
            self.assertEqual(len(action_values), 6)

    def test_weighted_pick(self):
        """Make weighted picks"""
        values = [1, 2, 5]
        pick = AgentQBinary.weighted_pick(values, 1)
        self.assertEqual(pick, 1)
        pick = AgentQBinary.weighted_pick(values, 2)
        self.assertEqual(pick, 2)
        pick = AgentQBinary.weighted_pick(values, 3)
        self.assertEqual(pick, 2)
        pick = AgentQBinary.weighted_pick(values, 5)
        self.assertEqual(pick, 2)
        pick = AgentQBinary.weighted_pick(values, 6)
        self.assertEqual(pick, 2)

    def test_max_pick(self):
        """Make pick of the max values"""
        values = [1, 2, 5]
        for idx in range(0, 20):
            pick = AgentQBinary.max_pick(values, idx)
            self.assertEqual(pick, 2)

        values = [1, 2, 2, 1]
        for idx in range(0, 20):
            pick = AgentQBinary.max_pick(values, idx)
            result = pick == 1 or pick == 2
            self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
