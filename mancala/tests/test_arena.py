
import unittest
from mancala.arena import Arena


class TestArena(unittest.TestCase):
    """Test the arena"""

    def test_init(self):
        """Define the arena init"""
        arena = Arena([], 5)
        self.assertEqual(arena.names(), [])


if __name__ == '__main__':
    unittest.main()
