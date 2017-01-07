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


if __name__ == '__main__':
    unittest.main()
