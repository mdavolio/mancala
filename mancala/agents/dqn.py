# -*- coding: utf-8 -*-

"""
Deep Q Learning Agent for the a Mancala AI
"""

import random
import math
from collections import namedtuple

import torch
import torch.nn as nn
import torch.optim as optim
import torch.autograd as autograd
import torch.nn.functional as F
import torchvision.transforms as T
from torch.autograd import Variable

from mancala.game import Game
from .agent import Agent
from .exact import AgentExact


class AgentDQN(Agent):
    '''
    Agent which leverages Deep Q Learning

    Based on
    http://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html
    '''

    def __init__(self, seed=451):
        self._seed = seed
        self._idx = 0

    def _move(self, game):
        '''Return move which ends in score hole'''
        self._idx = self._idx + 1
        random.seed(self._seed + self._idx)
        game_clone, rot_flag = game.clone_turn()

        return 0


class TrainerDQN():
    """Training class for simple Deep Q Learning"""

    def __init__(self, seed=451):
        self._seed = seed
        self._run = 0
        self._steps_done = 0

        self._BATCH_SIZE = 128
        self._GAMMA = 0.999
        self._EPS_START = 0.9
        self._EPS_END = 0.05
        self._EPS_DECAY = 200
        self._USE_CUDA = torch.cuda.is_available()

        self._model = ModelDQN()
        self._memory = ReplayMemory(10000)
        self._optimizer = optim.RMSprop(self._model.parameters(), lr=0.01)

    def train(self, num_episodes=10, agent=None):
        self._run += 1
        agent = AgentExact(self._seed + self._run) if agent is None else agent

        for idx in range(num_episodes):
            # Initialize the environment and state
            game = Game()
            state = TrainerDQN.game_to_state(game)
            score_previous = game.score()
            done = False
            while not game.over():
                # Select and perform an action
                action = self._select_action(state)
                move = TrainerDQN._action_tensor_to_int(action)
                game.move(move)

                player_two_acted = False
                while game.turn_player() != 1 and not game.over():
                    player_two_acted = True
                    game.move(agent.move(game))

                # Observe new state
                reward = TrainerDQN.game_to_reward(
                    score_previous, game, player_two_acted)
                next_state = None if game.over() else \
                    TrainerDQN.game_to_state(game)

                # Store the transition in memory
                self._memory.push(state, action, next_state, reward)

                # Move to the next state
                state = next_state
                score_previous = game.score()

                # Perform one step of the optimization (on the target network)
                self._optimize_model()

    def _optimize_model(self):

        if len(self._memory) < self._BATCH_SIZE:
            return
        transitions = self._memory.sample(self._BATCH_SIZE)
        # Transpose the batch (see http://stackoverflow.com/a/19343/3343043 for
        # detailed explanation).
        # this makes batch a tuple where the keys are iterable for the entire
        # batch
        batch = Transition(*zip(*transitions))

        # Compute a mask of non-final states and concatenate the batch elements
        non_final_mask = torch.ByteTensor(
            tuple(map(lambda s: s is not None, batch.next_state)))
        if self._USE_CUDA:
            non_final_mask = non_final_mask.cuda()

        # We don't want to backprop through the expected action values and
        # volatile will save us on temporarily changing the model parameters'
        # requires_grad to False!
        non_final_next_states = self.variable(torch.stack(
                [s for s in batch.next_state if s is not None]
            ), True)
        state_batch = self.variable(torch.stack(batch.state))
        action_batch = self.variable(torch.stack(batch.action))
        reward_batch = self.variable(torch.stack(batch.reward))

        # Compute Q(s_t, a) - the model computes Q(s_t), then we select the
        # columns of actions taken
        state_action_values = self._model(state_batch)
        state_action_values = state_action_values.gather(1, action_batch)

        # Compute V(s_{t+1}) for all next states.
        next_state_values = self.variable(torch.zeros(self._BATCH_SIZE))
        next_state_values[non_final_mask] = self._model(
            non_final_next_states).max(1)[0]
        # Now, we don't want to mess up the loss with a volatile flag, so let's
        # clear it. After this, we'll just end up with a Variable that has
        # requires_grad=False
        next_state_values.volatile = False
        # Compute the expected Q values
        expected_state_action_values = (next_state_values * self._GAMMA) + \
            reward_batch

        # Compute Huber loss
        loss = F.smooth_l1_loss(state_action_values,
                                expected_state_action_values)

        # Optimize the model
        self._optimizer.zero_grad()
        loss.backward()
        # for param in self._model.parameters():
        #     param.grad.data.clamp_(-1, 1)
        self._optimizer.step()

    @staticmethod
    def game_to_state(game):
        """Resolve a game's current state to a model input state"""
        return torch.FloatTensor(game._board[0:6] + game._board[7:13]).div(48)

    @staticmethod
    def game_to_reward(score_previous, game, player_two_acted):
        """Reward based on the past score. Always player 1 POV"""
        score = game.score()
        if game.over():
            reward = 100 if score[0] > score[1] else -100
        else:
            # penalize waiting
            # penalize less if keeping turn
            # earning score is worth something
            # letting score is penalized
            reward = 0 + \
                (-1 if player_two_acted else 0) + \
                0.5 * (score[0] - score_previous[0]) - \
                0.25 * (score[1] - score_previous[1])

        return torch.Tensor([reward])

    @staticmethod
    def _action_tensor_to_int(action):
        return action[0]

    def _select_action(self, state):
        """
        Based on the current model and a game state, pick a new action (move)
        """
        sample = random.random()
        self._steps_done += 1
        eps_threshold = self._EPS_END + (self._EPS_START - self._EPS_END) * \
            math.exp(-1. * self._steps_done / self._EPS_DECAY)
        if sample > eps_threshold:
            return self._model(
                    self.variable(state.unsqueeze(0))
                ).data.max(1)[1][0].cpu()
        else:
            return torch.LongTensor([random.randrange(6)])
            # pick = random.randrange(6)
            # return torch.LongTensor([[
            #     0 if pick != i else 1 for i in range(6)
            # ]])

    def variable(self, tensor, volatile=False):
        if self._USE_CUDA:
            tensor = tensor.cuda()
        return Variable(tensor, volatile=volatile)


class ModelDQN(nn.Module):
    """The DQN Model. From the 12 slots, pick of the six choices"""

    def __init__(self):
        super(ModelDQN, self).__init__()
        self.layer1 = nn.Linear(12, 32)
        self.layer2 = nn.Linear(32, 64)
        self.layer3 = nn.Linear(64, 32)
        self.layer4 = nn.Linear(32, 6)

    def forward(self, x):
        x = F.sigmoid(self.layer1(x))
        x = F.sigmoid(self.layer2(x))
        x = F.sigmoid(self.layer3(x))
        x = F.softmax(self.layer4(x))
        return x


Transition = namedtuple('Transition',
                        ('state', 'action', 'next_state', 'reward'))


class ReplayMemory(object):
    """
    Stores the transitions that the agent observes, allowing us to reuse this
    data later. By sampling from it randomly, the transitions that build up a
    batch are decorrelated. It has been shown that this greatly stabilizes and
    improves the DQN training procedure.

    http://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html#replay-memory
    """

    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []
        self.position = 0

    def push(self, *args):
        """Saves a transition."""
        if len(self.memory) < self.capacity:
            self.memory.append(None)
        self.memory[self.position] = Transition(*args)
        self.position = (self.position + 1) % self.capacity

    def sample(self, batch_size):
        """Sample from the memories"""
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)