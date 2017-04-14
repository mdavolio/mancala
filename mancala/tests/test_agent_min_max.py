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

    def test_basic_move_depth_1(self):
        """Test move picks a random spot on the right side w/ depth 1"""
        move = AgentMinMax(seed=123, depth=1).move(Game())
        self.assertEqual(move, 2)

    def test_basic_move_depth_3(self):
        """Test move picks a random spot on the right side w/ depth 3"""
        move = AgentMinMax(seed=123, depth=3).move(Game())
        self.assertEqual(move, 2)

    def test_basic_move_depth_5(self):
        """Test move picks a random spot on the right side w/ depth 5"""
        move = AgentMinMax(seed=123, depth=5).move(Game())
        self.assertEqual(move, 2)

    def test_max_min_max_move(self):
        """Should spot a capture as the highest option"""
        game = Game([1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0])
        move = AgentMinMax(seed=123, depth=3).move(game)
        self.assertEqual(move, 5)

    def test_min_max_minimize_p2_score(self):
        '''Should avoid move which gives p2 more score next turn'''
        game = Game([0, 0, 3, 0, 0, 3, 0, 0, 1, 0, 0, 1, 0, 0])
        move = AgentMinMax(seed=123, depth=1).move(game)
        self.assertEqual(move, 2)
