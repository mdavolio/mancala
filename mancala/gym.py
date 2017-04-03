# -*- coding: utf-8 -*-
"""
Mancala Gym object
"""

import time

from mancala.agents.reinforcementlearning.qbinary import AgentQBinary
from mancala.agents.random import AgentRandom


class Gym():
    """
    Wrapper functions to train agents

    All agents must accept:
        * start_data - A dict of starting data, whatever the agent could use to start training, or None
        * config_data - A dict of any configuration data
    And return only
        * end_data - A dict of resulting data. This may be capable of feeding back as start_data
    """

    _rl_config_defaults = {
        "epochs": 5,
        "games_per_epoch": 100,
        "alpha": 0.1,
        "gamma": 0.1,
        "decay": 0.1,
        "epsilon": 0.1
    }

    @staticmethod
    def qbinary(starting_data, config_data=None, verbose=False):
        """
        Work with RL QBinary
        """
        return Gym._learn_rl(AgentQBinary(), starting_data, config_data, verbose)

    @staticmethod
    def _learn_rl(agent, starting_data, config_data=None, verbose=False):
        """
        Wrapper for all RL Gym operations
        """
        config_data = Gym._rl_config_defaults if config_data is None else config_data
        config_data = {**config_data, **Gym._rl_config_defaults}

        action_values = None if starting_data is None else starting_data.action_values

        action_values_new = agent.do_learn(
            action_values,
            config_data["epochs"],
            config_data["games_per_epoch"],
            AgentRandom(451),
            config_data["alpha"],
            config_data["gamma"],
            config_data["decay"],
            config_data["epsilon"],
            1,
            Gym.report if verbose else lambda tup: tup
        )

        return {
            "action_values": action_values_new
        }

    @staticmethod
    def report(tup):
        """Print the 4th element in the tuple, the message"""
        print("{} || {}".format(time.strftime("%Y-%m-%d %H:%M"), tup[3]))
