"""Kick off for training A3C agent training"""

import argparse

import torch
import torch.multiprocessing as _mp
mp = _mp.get_context('spawn')


from mancala.env import MancalaEnv
from mancala.arena import Arena
from mancala.agents.random import AgentRandom
from mancala.agents.agent import Agent

from mancala.trainers.a3c_model import ActorCritic
from mancala.trainers.a3c_train import train
from mancala.trainers.a3c_test import test

# Based on
# https://github.com/pytorch/examples/tree/master/mnist_hogwild
# Training settings
parser = argparse.ArgumentParser(description='A3C for Mancala')
parser.add_argument('--lr', type=float, default=0.0001, metavar='LR',
                    help='learning rate (default: 0.0001)')
parser.add_argument('--gamma', type=float, default=0.99, metavar='G',
                    help='discount factor for rewards (default: 0.99)')
parser.add_argument('--tau', type=float, default=1.00, metavar='T',
                    help='parameter for GAE (default: 1.00)')
parser.add_argument('--beta', type=float, default=0.01, metavar='B',
                    help='parameter for entropy (default: 0.01)')
parser.add_argument('--seed', type=int, default=1, metavar='S',
                    help='random seed (default: 1)')
parser.add_argument('--num-processes', type=int, default=4, metavar='N',
                    help='how many training processes to use (default: 4)')
parser.add_argument('--num-steps', type=int, default=20, metavar='NS',
                    help='number of forward steps in A3C (default: 20)')
parser.add_argument('--max-episode-length', type=int, default=100, metavar='M',
                    help='maximum length of an episode (default: 100)')
parser.add_argument('--evaluate', action="store_true",
                    help='whether to evaluate results')

parser.add_argument('--save-name', metavar='FN', default='default_model',
                    help='path/prefix for the filename to save shared model\'s parameters')
parser.add_argument('--load-name', default=None, metavar='SN',
                    help='path/prefix for the filename to load shared model\'s parameters')


if __name__ == '__main__':
    args = parser.parse_args()

    torch.manual_seed(args.seed)

    dtype = torch.cuda.FloatTensor if torch.cuda.is_available() else torch.FloatTensor

    env = MancalaEnv(AgentRandom(args.seed), args.seed)
    state = env.reset()
    shared_model = ActorCritic(state.shape[0], env.action_space).type(dtype)
    if args.load_name is not None:
        shared_model.load_state_dict(torch.load(args.load_name))
    shared_model.share_memory()

    # train(1,args,shared_model,dtype)
    processes = []

    p = mp.Process(target=test, args=(
        args.num_processes, args, shared_model, dtype))
    p.start()
    processes.append(p)

    if not args.evaluate:
        for rank in range(0, args.num_processes):
            p = mp.Process(target=train, args=(
                rank, args, shared_model, dtype))
            p.start()
            processes.append(p)
    for p in processes:
        p.join()
