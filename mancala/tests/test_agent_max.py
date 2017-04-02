# -*- coding: utf-8 -*-
"""
Tests for the agent Max class
"""

import unittest
from mancala.agents.max import AgentMax
from mancala.game import Game


class TestAgentMax(unittest.TestCase):
    """Tests for the random agent class"""

    def test_move_p1(self):
        """Test move picks a paying move for player 1"""
        move = AgentMax().move(Game())
        self.assertEqual(move, 4)

    def test_move_p2(self):
        """Test move picks a max move for player 2"""
        game = Game()
        game.move(4)
        self.assertEqual(game.turn_player(), 2)
        move = AgentMax().move(game)
        self.assertEqual(move, 10)

    def test_capture_p1(self):
        """Max should spot a capture as the highest option"""
        game = Game([1, 0, 0, 4, 0, 0, 0, 2, 3, 0, 0, 1, 0, 0])
        move = AgentMax().move(game)
        self.assertEqual(move, 0)
        game.move(move)
        self.assertEqual(game.board(),
                         [0, 0, 0, 4, 0, 0, 2, 2, 3, 0, 0, 0, 0, 0])
        self.assertEqual(game.score(), (2, 0))

if __name__ == '__main__':
    unittest.main()
