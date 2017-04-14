# -*- coding: utf-8 -*-
"""
Tests for the abstract agent class
"""

import unittest
from mancala.agents.max_min import AgentMinMax
from mancala.game import Game


class TestAgentMinMax(unittest.TestCase):
    """Tests for the random agent class"""

    def test_basic_move(self):
        """Test move picks a random spot on the right side"""
        move = AgentMinMax(seed=123, depth=2).move(Game())
        self.assertEqual(move, 1)
