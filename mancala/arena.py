# -*- coding: utf-8 -*-
"""
Mancala Arena object
"""

import itertools
from mancala.game import Game


class Arena():
    """
    Pairs agents and compares performance.

    Note that agents must be of a list of tuples of the form:
    `(agent_str, agent_lambda)`

    Where `agent_str` is the display name of the agent and
    `agent_lambda` is a lambda function that takes **only** a random
    seed to create a new object of the agent
    """

    def __init__(self,
                 agents=None,
                 games_to_play=101):
        self._agents = agents if agents is list else []
        self._games_to_play = games_to_play
        self._names = list(sorted(map(lambda t: t[0], agents)))

        # this ensures all agent pairs and pairs with themselves
        combos = list(itertools.combinations(agents, 2)) + \
            list(zip(agents, agents))
        self._combos = sorted(combos, key=lambda t: t[0][0] + '_' + t[1][0])
        self._results = list(map(lambda t: Arena._handle_combo(
            t[1], games_to_play, t[0]), enumerate(self._combos)))

    @staticmethod
    def _handle_combo(combo, games_to_play, seed):
        wins = Arena.compare_agents(
            combo[0][1], combo[1][1], games_to_play, seed)
        return (combo[0][0], combo[1][0], wins)

    @staticmethod
    def compare_agents(lambda_01, lambda_02, games_to_play=51, seed=451):
        """
        Returns number of times agent created from lambda_01
        wins over agent created from lambda_02
        """
        wins = 0
        for idx in range(games_to_play):
            game = Game()
            agent_one = (lambda_01)(seed + idx)
            agent_two = (lambda_02)(seed + idx)
            # max_size = 0
            while not game.over():
                if game.turn_player() == 1:
                    game.move(agent_one.move(game))
                else:
                    game.move(agent_two.move(game))
            #     max_size = max([max_size] + game.board())
            # print("Max Size", max_size)
            if game.score()[0] > game.score()[1]:
                wins = wins + 1
        return wins

    @staticmethod
    def compare_agents_float(lambda_01, lambda_02, games_to_play=51, seed=451):
        """
        Returns fraction of times agent created from lambda_01
        wins over agent created from lambda_02
        """
        wins = Arena.compare_agents(lambda_01, lambda_02, games_to_play, seed)
        return wins / games_to_play

    def names(self):
        """Sorted names of agents"""
        return self._names[:]

    def results(self):
        """Sorted results of agents"""
        return self._results[:]

    def csv_header(self):
        """A header row for a csv result"""
        return ['opponent'] + self.names()

    def csv_results_lists(self):
        """
        List of Lists, corresponding to the player 2 results
        The first element is the opponent type
        """
        return list(map(self._row_from_name, self._names))

    def _row_from_name(self, name):
        """Returns a row of results, each from the perspective of """
        results_for_player_2 = list(
            filter(lambda t: t[0] == name or t[1] == name, self._results))
        results_fixed_for_row = list(map(lambda t: Arena._fix_for_row(
            name, t, self._games_to_play), results_for_player_2))
        results_ordered = list(
            sorted(results_fixed_for_row, key=lambda t: t[0]))
        results_final = list(map(lambda t: t[1], results_ordered))
        return [name] + results_final

    @staticmethod
    def _fix_for_row(name, match_tuple, game_count):
        """Reduce a row to the player 2 and note the correct win percentage for player 1"""
        if match_tuple[0] == name and match_tuple[1] != name:
            win_percent = (game_count - match_tuple[2]) / game_count
            return (match_tuple[1], win_percent)
        # if match_tuple[0] != name and match_tuple[1] == name:
        return (match_tuple[0], match_tuple[2] / game_count)