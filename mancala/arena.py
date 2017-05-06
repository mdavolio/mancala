# -*- coding: utf-8 -*-
"""
Mancala Arena object
"""

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
                 games_to_play=101,
                 seed=451):
        agents = [] if agents is None else agents
        names = [a[0] for a in agents]
        self._names = names

        data = [names]  # opponent names
        # data = [names]  # opponent names
        for primary in agents:
            name_primary, lambda_primary = primary
            scores = []
            for opponent in agents:
                name_opponent, lambda_opponent = opponent
                # print(" Testing {} vs {}".format(name_primary, name_opponent))
                win_rate = Arena.compare_agents_float(
                    lambda_primary, lambda_opponent, games_to_play, seed)
                # print(" Testing {} vs {} -> {}%".format(name_primary,
                #                                         name_opponent, round(win_rate * 100, 2)))
                scores.append(win_rate)
            data.append(scores)

        self._results = Arena._transpose(data)

    @staticmethod
    def _transpose(list_list):
        return [list(i) for i in zip(*list_list)]

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
        return self.results()

    @staticmethod
    def _fix_for_row(name, match_tuple, game_count):
        """Reduce a row to the player 2 and note the correct win percentage for player 1"""
        if match_tuple[0] == name and match_tuple[1] != name:
            win_percent = (game_count - match_tuple[2]) / game_count
            return (match_tuple[1], win_percent)
        # if match_tuple[0] != name and match_tuple[1] == name:
        return (match_tuple[0], match_tuple[2] / game_count)
