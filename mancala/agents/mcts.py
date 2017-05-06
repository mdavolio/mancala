# -*- coding: utf-8 -*-

"""
Abstract Agent for the a Mancala AI

Max-Min Agent
"""

import random
import sys
import math
from mancala.game import Game
from .agent import Agent
from .exact import AgentExact


class AgentMCTS(Agent):
    """Agent which picks a move by the next score"""

    def __init__(self, seed=451, depth=4, iterations=3):
        self._seed = seed
        self._idx = 0
        self._depth = depth
        self._iterations = iterations
    
    @staticmethod
    def basemove(game):
        agent = AgentExact(seed=random.randint(0,15000))
        while not game.over():
            game.move(agent.move(game))
        return game.score()[0] > game.score()[1]

    @staticmethod
    def explore(game, dictionary, depth):
        alpha = -sys.maxsize

        if depth == 0 or game.over():
            success = AgentMCTS.basemove(game)
            return success, dictionary
        
        move_options = Agent.valid_indices(game)
        for move in move_options:
            if move not in dictionary:
                dictionary[move] = (0,1,{})
        t = sum([n for _,n,_ in dictionary.values()])
        for move in move_options:
            w = dictionary[move][0]
            n = dictionary[move][1]

            score = (w/n) + math.sqrt(2) * math.sqrt(math.log(t)/n)

            if score > alpha:
                alpha = score
                best_move = move
        
        clone = game.clone()
        clone.move(best_move)

        w,n,children = dictionary[best_move]

        success,new_children = AgentMCTS.explore(clone, children, depth - 1)

        dictionary[best_move] = (w + 1 if success else w, n + 1, new_children)

        return success, dictionary
                        
    def _move(self, game):
        """Return best value from MCTS"""
        self._idx = self._idx + 1
        random.seed(self._seed + self._idx)
        game_clone, rot_flag = game.clone_turn()
        
        alpha = -sys.maxsize
        move_dict = {}

        for _ in range(self._iterations):
            _,move_dict = AgentMCTS.explore(game_clone, move_dict, self._depth)
        
        move_options = Agent.valid_indices(game_clone)

        t = sum([n for _,n,_ in move_dict.values()])
        for move in move_options:
            w = move_dict[move][0]
            n = move_dict[move][1]

            score = (w/n) + math.sqrt(2) * math.sqrt(math.log(t)/n)

            if score > alpha:
                alpha = score
                best_move = move        

        final_move = Game.rotate_board(rot_flag, best_move)
        
        return final_move
