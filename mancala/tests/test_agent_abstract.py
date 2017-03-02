# -*- coding: utf-8 -*-
"""
Tests for the abstract agent class
"""

import unittest
from mancala.agent import Agent


class TestAgentAbstract(unittest.TestCase):
    """Tests for the abstract agent class"""

    def test_player(self):
        """Test move throws"""
        with self.assertRaises(NotImplementedError):
            Agent().move(None)


if __name__ == '__main__':
    unittest.main()
