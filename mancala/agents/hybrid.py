"""Agent with uses a hybrid of systems"""

import random

import torch
import torch.nn.functional as F
from torch.autograd import Variable

import numpy as np
from gym.utils import seeding

from mancala.game import Game
from mancala.env import MancalaEnv
from mancala.agents.agent import Agent
from mancala.agents.a3c import AgentA3C
from mancala.agents.exact import AgentExact
from mancala.agents.max_min import AgentMinMax


class AgentHybrid(Agent):
    '''Agent which leverages A3C/Exact/MinMax'''

    def __init__(self,
                 model_path,
                 dtype,
                 seed=451):
        self._seed = seed
        self.np_random, _ = seeding.np_random(seed)
        self._a3c = AgentA3C(model_path, dtype, seed)
        self._exact = AgentExact(seed + 1)
        self._minmax = AgentMinMax(seed + 2)


    def _move(self, game):
        '''Return move which ends in score hole'''
        assert not game.over()

        move_a3c = self._a3c.move(game)
        move_exact = self._exact.move(game)
        move_minmax = self._minmax.move(game)

        if move_a3c == move_exact and \
            move_a3c == move_minmax and \
            move_exact == move_minmax:
            # perfect agreement
            return move_a3c

        if move_exact == move_minmax:
            # simple methods agree, pick that
            return move_exact

        if sum(game.score()) < 38:
            return move_a3c

        return move_exact
