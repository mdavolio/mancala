
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
        self.assertListEqual(
            arena.names(), ["Random A", "Random B", "Random C"])


class TestArenaResults(unittest.TestCase):
    """Test the arena"""

    def test_init_single(self):
        """Define the arena with one version"""
        arena = Arena([
            ("Random", lambda seed: AgentRandom(seed))
        ], 5)
        results = arena.results()
        self.assertEqual(len(results), 1)
        self.assertListEqual(results, [("Random", "Random", 3)])

    def test_init_multiple(self):
        """Define the arena with several agents"""
        arena = Arena([
            ("Random A", lambda seed: AgentRandom(seed)),
            ("Random C", lambda seed: AgentRandom(seed)),
            ("Random B", lambda seed: AgentRandom(seed))
        ], 5)
        results = arena.results()
        self.assertEqual(len(results), 6)
        self.assertListEqual(results, [
            ("Random A", "Random A", 3),
            ("Random A", "Random B", 3),
            ("Random A", "Random C", 2),
            ("Random B", "Random B", 1),
            ("Random C", "Random B", 1),
            ("Random C", "Random C", 1),
        ])


if __name__ == '__main__':
    unittest.main()
