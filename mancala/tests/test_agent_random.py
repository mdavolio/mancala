# -*- coding: utf-8 -*-
"""
Tests for the abstract agent class
"""

import unittest
from mancala.agents.random import AgentRandom
from mancala.game import Game


class TestAgentRandom(unittest.TestCase):
    """Tests for the random agent class"""

    def test_random_move(self):
        """Test move picks a random spot on the right side"""
        move = AgentRandom().move(Game())
        self.assertEqual(move, 2)

    def test_random_move_seed(self):
        """Test move is seeded properly"""
        move = AgentRandom(454).move(Game())
        self.assertEqual(move, 5)

    def test_random_no_moves_player1(self):
        """Test move is seeded properly"""
        move = AgentRandom(454).move(
            Game([0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 0]))
        self.assertEqual(move, 0)

    def test_random_no_moves_player2(self):
        """Test move is seeded properly"""
        move = AgentRandom(454).move(
            Game([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 2))
        self.assertEqual(move, 0)

    def test_random_move_02(self):
        """Test multiple moves"""
        game = Game()
        agent = AgentRandom(454)
        move = agent.move(game)
        self.assertEqual(move, 5)
        game.move(move)

        move = agent.move(game)
        self.assertEqual(move, 12)



if __name__ == '__main__':
    unittest.main()
