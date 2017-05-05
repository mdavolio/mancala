
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
            arena.names(), ["Random A", "Random C", "Random B"])


class TestArenaResults(unittest.TestCase):
    """Test the arena"""

    def test_init_single(self):
        """Define the arena with one version"""
        arena = Arena([
            ("Random", lambda seed: AgentRandom(seed))
        ], 5)
        results = arena.results()
        self.assertEqual(len(results), 1)
        self.assertListEqual(results, [["Random", 0.4]])

    def test_init_multiple(self):
        """Define the arena with several agents"""
        arena = Arena([
            ("Random A", lambda seed: AgentRandom(seed)),
            ("Random C", lambda seed: AgentRandom(seed)),
            ("Random B", lambda seed: AgentRandom(seed))
        ], 5)
        results = arena.results()
        self.assertEqual(len(results), 3)
        self.assertListEqual(results, [['Random A', 0.4, 0.4, 0.4],
                                       ['Random C', 0.4, 0.4, 0.4],
                                       ['Random B', 0.4, 0.4, 0.4]])


class TestArenaCsv(unittest.TestCase):
    """Test the arena csv tools"""

    def test_header(self):
        """Define the arena with one version"""
        arena = Arena([
            ("Random A", lambda seed: AgentRandom(seed)),
            ("Random C", lambda seed: AgentRandom(seed)),
            ("Random B", lambda seed: AgentRandom(seed))
        ], 5)
        self.assertListEqual(arena.csv_header(), [
                             "opponent", "Random A", "Random C", "Random B"])

    def test_list(self):
        """Define the arena with one version"""
        arena = Arena([
            ("Random A", lambda seed: AgentRandom(seed)),
            ("Random C", lambda seed: AgentRandom(seed)),
            ("Random B", lambda seed: AgentRandom(seed))
        ], 5)
        self.assertEqual(len(arena.csv_results_lists()), 3)
        self.assertListEqual(arena.csv_results_lists(), [
            ['Random A', 0.4, 0.4, 0.4],
            ['Random C', 0.4, 0.4, 0.4],
            ['Random B', 0.4, 0.4, 0.4]
        ])


if __name__ == '__main__':
    unittest.main()
