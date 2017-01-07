import unittest
from game import Game


class TestInit(unittest.TestCase):

    def test_player(self):
        self.assertEqual(Game().turn_player(), 1)

    def test_score(self):
        self.assertEqual(Game().score(), (0, 0))

    def test_over(self):
        self.assertFalse(Game().over())

    def test_board(self):
        self.assertEqual(Game().board_render(),
                         """     3  1  0  0  0  0\n  0                    0 \n     4  4  4  4  4  4""")

    def test_board_raw(self):
        self.assertEqual(Game()._board,
                         [3, 1, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 0])


class TestMoves(unittest.TestCase):

    def test_move_00(self):
        g = Game()
        g.move(0)
        self.assertEqual(g._board,
                         [0, 2, 1, 1, 0, 0, 0, 4, 4, 4, 4, 4, 4, 0])
        self.assertEqual(g.score(), (0, 0))

    def test_move_01(self):
        g = Game()
        g.move(1)
        self.assertEqual(g._board,
                         [3, 0, 1, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 0])


if __name__ == '__main__':
    unittest.main()
