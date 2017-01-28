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
                         """     4  4  4  4  4  4\n  0                    0 \n     4  4  4  4  4  4""")

    def test_board_raw(self):
        self.assertEqual(Game()._board,
                         [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0])


class TestMoves(unittest.TestCase):

    def test_move_00(self):
        g = Game()
        g.move(0)
        self.assertEqual(g._board,
                         [0, 5, 5, 5, 5, 4, 0, 4, 4, 4, 4, 4, 4, 0])
        self.assertEqual(g.score(), (0, 0))
        self.assertEqual(g.turn_player(), 2)

    def test_move_01(self):
        g = Game()
        g.move(1)
        self.assertEqual(g._board,
                         [4, 0, 5, 5, 5, 5, 0, 4, 4, 4, 4, 4, 4, 0])
        self.assertEqual(g.turn_player(), 2)

    def test_move_04(self):
        g = Game()
        g.move(4)
        self.assertEqual(g._board,
                         [4, 4, 4, 4, 0, 5, 1, 5, 5, 4, 4, 4, 4, 0])
        self.assertEqual(g.score(), (1, 0))
        self.assertEqual(g.turn_player(), 2)

    def test_move_05(self):
        g = Game()
        g.move(0)
        g.move(11)
        self.assertEqual(g._board,
                         [1, 6, 5, 5, 5, 4, 0, 4, 4, 4, 4, 0, 5, 1])
        self.assertEqual(g.score(), (0, 1))
        self.assertEqual(g.turn_player(), 1)


if __name__ == '__main__':
    unittest.main()
