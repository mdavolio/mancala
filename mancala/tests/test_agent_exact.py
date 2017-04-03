# -*- coding: utf-8 -*-
"""
Tests for the agent Exact class
"""

import unittest
from mancala.agents.exact import AgentExact
from mancala.game import Game


class TestAgentExact(unittest.TestCase):
    """Tests for the exact agent class"""

    def test_move_p1(self):
        '''Test move picks correct 1st player move'''
        move = AgentExact().move(Game())
        self.assertEqual(move, 2)

    def test_move_p2(self):
        '''Test move correctly picks 2nd player move'''
        game = Game()
        game.move(4)
        self.assertEqual(game.turn_player(), 2)
        move = AgentExact().move(game)
        self.assertEqual(move, 8)

if __name__ == '__main__':
    unittest.main()
