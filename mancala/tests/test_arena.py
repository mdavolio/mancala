
import unittest
from mancala.arena import Arena
from mancala.agents.random import AgentRandom


class TestArenaNames(unittest.TestCase):
    """Test the arena"""

    def test_init(self):
        """Define the arena init"""
        arena = Arena([], 5)
        self.assertListEqual(arena.names(), [])

    def test_init_single(self):
        """Define the arena with one version"""
        arena = Arena([
            ("Random", lambda seed: AgentRandom(seed))
        ], 5)
        self.assertListEqual(arena.names(), ["Random"])

    def test_init_multiple(self):
        """Define the arena with several agents"""
        arena = Arena([
            ("Random A", lambda seed: AgentRandom(seed)),
            ("Random C", lambda seed: AgentRandom(seed)),
            ("Random B", lambda seed: AgentRandom(seed))
        ], 5)
        self.assertListEqual(arena.names(), ["Random A", "Random B", "Random C"])


if __name__ == '__main__':
    unittest.main()
