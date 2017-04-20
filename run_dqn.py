
import argparse
import json
import os

from mancala.agents.dqn import TrainerDQN, AgentDQN
from mancala.arena import Arena
from mancala.agents.random import AgentRandom
from mancala.agents.exact import AgentExact


PARSER = argparse.ArgumentParser(
    description='Train a DQN agent')

PARSER.add_argument('--verbose', action="store_true", default=True,
                    help='Log verbose results')

PARSER.add_argument('--input', type=str,
                    help='Path to read past trained start data')

PARSER.add_argument('--output', type=str, required=True,
                    help='Path to write trained results')

# ARGS = PARSER.parse_args()
ARGS = PARSER.parse_args(([
    '--output',
    'training/dqn.pth',
    '--verbose'
]))


print('Starting Training')


def train(path_output, path_input=None, verbose=True):
    trainer = TrainerDQN(path_input,
                         seed=451,
                         batch_size=128,
                         gamma=0.9,
                         eps_start=0.9,
                         eps_end=0.05,
                         eps_decay=500,
                         replay_size=10000,
                         learning_rate=0.02)

    for epoch in range(10):
        trainer.train(10, print_mod=2)
        trainer.write_state_to_path(path_output)

        win_rate_v_random = Arena.compare_agents_float(
            lambda seed: AgentDQN(path_output, seed + epoch),
            lambda seed: AgentRandom(seed + epoch),
            200)
        win_rate_v_exact = Arena.compare_agents_float(
            lambda seed: AgentDQN(path_output, seed + epoch),
            lambda seed: AgentExact(seed + epoch),
            200)
        msg = "Epoch {: >3} | VsRandom: {: >4}% | VsExact: {: >4}%".format(
            epoch,
            round(win_rate_v_random * 100, 2),
            round(win_rate_v_exact * 100, 2)
        )
        print(msg)

train(ARGS.output, ARGS.input, ARGS.verbose)

print('Complete')
