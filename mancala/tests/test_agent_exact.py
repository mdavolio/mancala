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
        game.move(5)
        self.assertEqual(game.turn_player(), 2)
        move = AgentExact().move(game)
        self.assertEqual(move, 8)

    def test_double_exact(self):
        """If more than one exact, choose closest to score first"""
        game = Game([6, 5, 4, 3, 2, 1, 0, 1, 1, 1, 1, 1, 1, 1])
        move = AgentExact().move(game)
        self.assertEqual(move, 5)
        game.move(move)
        move = AgentExact().move(game)
        self.assertEqual(move, 4)
        game.move(move)
        move = AgentExact().move(game)
        self.assertEqual(move, 5)

if __name__ == '__main__':
    unittest.main()
