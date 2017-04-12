# -*- coding: utf-8 -*-
"""
Mancala Gym object
"""

import time

from mancala.agents.reinforcementlearning.qbinary import AgentQBinary
from mancala.agents.reinforcementlearning.qquad import AgentQQuad
from mancala.agents.reinforcementlearning.qmod import AgentQMod
from mancala.agents.random import AgentRandom


class Gym():
    """
    Wrapper functions to train agents

    All agents must accept:
        * start_data - A dict of starting data, whatever the agent uses to start training, or None
        * config_data - A dict of any configuration data
    And return only
        * end_data - A dict of resulting data. This may be capable of feeding back as start_data
    """

    _rl_config_defaults = {
        "epochs": 30,
        "games_per_epoch": 1000,
        "alpha": 0.3,
        "gamma": 0.1,
        "decay": 0.5,
        "epsilon": 0.2
    }

    @staticmethod
    def qbinary(starting_data, config_data=None, verbose=False):
        """
        Work with RL QBinary
        """
        return Gym._learn_rl(AgentQBinary(), starting_data, config_data, verbose)

    @staticmethod
    def qquad(starting_data, config_data=None, verbose=False):
        """
        Work with RL QQuad
        """
        return Gym._learn_rl(AgentQQuad(), starting_data, config_data, verbose)

    @staticmethod
    def qmod(starting_data, config_data=None, verbose=False):
        '''
        Works with RL QMod
        '''
        return Gym._learn_rl(AgentQMod(), starting_data, config_data, verbose)

    @staticmethod
    def _learn_rl(agent, starting_data, config_data=None, verbose=False):
        """
        Wrapper for all RL Gym operations
        """
        config_data = Gym._rl_config_defaults if config_data is None else config_data
        config_data = {**Gym._rl_config_defaults, **config_data}

        action_values = None if starting_data is None else starting_data["action_values"]

        action_values_new = agent.do_learn(
            action_values,
            config_data["epochs"],
            config_data["games_per_epoch"],
            AgentRandom(451),
            config_data["alpha"],
            config_data["gamma"],
            config_data["decay"],
            config_data["epsilon"],
            10,
            Gym.report if verbose else lambda tup: tup
        )

        return {
            "action_values": action_values_new
        }

    @staticmethod
    def report(tup):
        """Print the 4th element in the tuple, the message"""
        print("{} || {}".format(time.strftime("%Y-%m-%d %H:%M"), tup[3]))
