
import argparse
import json
import os
import re
import datetime
import subprocess

from tensorboard_logger import configure, log_value

from mancala.agents.dqn import TrainerDQN, AgentDQN
from mancala.arena import Arena
from mancala.agents.random import AgentRandom
from mancala.agents.exact import AgentExact



git_head = subprocess.check_output(['git',
                                    'rev-parse',
                                    '--short',
                                    'HEAD']).strip().decode('UTF-8')

configure("runs/{}".format(git_head), flush_secs=5)


PARSER = argparse.ArgumentParser(
    description='Train a DQN agent')

PARSER.add_argument('--verbose', action="store_true", default=True,
                    help='Log verbose results')

PARSER.add_argument('--epochs', type=int, default=100,
                    help='Number of epochs to train')

PARSER.add_argument('--input', type=str,
                    help='Path to read past trained start data')

PARSER.add_argument('--output', type=str, required=True,
                    help='Path to write trained results')

ARGS = PARSER.parse_args()
# ARGS = PARSER.parse_args(([
#     '--output',
#     'training/dqn.pth',
#     '--verbose'
# ]))

print('Starting Training')


def train(epochs, path_output, path_input=None, verbose=True):

    if path_input is not None:
        epoch_regexp = re.compile(r".*epoch\.(\d+)$")
        # regexp_result = epoch_regexp.match("training/dqn.epoch.00000233")
        regexp_result = epoch_regexp.match(path_input)
        starting_epoch = int(regexp_result.groups()[0])
    else:
        starting_epoch = 0


    trainer = TrainerDQN(path_input,
                         seed=451,
                         batch_size=2048,
                         gamma=0.9,
                         eps_start=0.9,
                         eps_end=0.05,
                         eps_decay=40000,
                         replay_size=25000,
                         learning_rate=0.02)

    for epoch in range(starting_epoch + 1, epochs):
        print(" Training Epoch {}".format(epoch))
        trainer.train(4500, print_mod=500)
        trainer.write_state_to_path("{}.epoch.{:0>8}".format(path_output, epoch))
        trainer.write_state_to_path(path_output)

        win_rate_v_random = Arena.compare_agents_float(
            lambda seed: AgentDQN(path_output, seed + epoch),
            lambda seed: AgentRandom(seed + epoch),
            800)
        win_rate_v_exact = Arena.compare_agents_float(
            lambda seed: AgentDQN(path_output, seed + epoch),
            lambda seed: AgentExact(seed + epoch),
            800)
        msg = " Epoch {: >3} | VsRandom: {: >4}% | VsExact: {: >4}%".format(
            epoch,
            round(win_rate_v_random * 100, 2),
            round(win_rate_v_exact * 100, 2)
        )

        log_value('win_rate_v_random', win_rate_v_random, epoch)
        log_value('win_rate_v_exact', win_rate_v_exact, epoch)

        print(' ───── ' + datetime.datetime.now().strftime("%c") + ' ───── ')
        print(msg)

train(ARGS.epochs, ARGS.output, ARGS.input, ARGS.verbose)

print('Complete')
