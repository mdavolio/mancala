# -*- coding: utf-8 -*-

"""
Deep Q Learning Agent for the a Mancala AI
"""

import random
import math
import time
import sys
from collections import namedtuple

import torch
import torch.nn as nn
import torch.optim as optim
import torch.autograd as autograd
import torch.nn.functional as F
from torch.autograd import Variable

from mancala.game import Game
from .agent import Agent
from .exact import AgentExact


class AgentDQN(Agent):
    '''
    Agent which leverages Deep Q Learning
    '''

    def __init__(self,
                 model_path=None,
                 seed=451):
        self._seed = seed
        self._idx = 0
        self._model = ModelDQN()
        ModelDQN.Seed(seed)

        if ModelDQN.USE_CUDA:
            self._model.cuda()

        if model_path is not None:
            self._model.load_state_dict(torch.load(model_path))

    def _move(self, game):
        '''Return move which ends in score hole'''
        self._idx = self._idx + 1
        ModelDQN.Seed(self._seed + self._idx)
        game_clone, rot_flag = game.clone_turn()

        state = TrainerDQN.game_to_state(game_clone)
        action = self._model(
            ModelDQN.Variable(state.unsqueeze(0))
        ).data.cpu()
        move_options = Agent.valid_indices(game_clone)
        move_values = action[0][torch.LongTensor(move_options)].tolist()
        move_idx = action[0][torch.LongTensor(move_options)].max(0)[
            1].tolist()[0]
        move = move_options[move_idx]

        return Game.rotate_board(rot_flag, move)


class TrainerDQN():
    """
    Training class for simple Deep Q Learning

    Based on
    http://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html
    """

    def __init__(self,
                 model_path=None,
                 seed=451,
                 batch_size=128,
                 gamma=0.999,
                 eps_start=0.9,
                 eps_end=0.05,
                 eps_decay=200,
                 replay_size=10000,
                 learning_rate=0.02
                 ):
        self._run = 0
        self._steps_done = 0
        self._seed = seed

        self._BATCH_SIZE = batch_size
        self._GAMMA = gamma
        self._EPS_START = eps_start
        self._EPS_END = eps_end
        self._EPS_DECAY = eps_decay
        ModelDQN.Seed(seed)

        self._model = ModelDQN()
        self._memory = ReplayMemory(replay_size)
        self._optimizer = optim.RMSprop(
            self._model.parameters(), lr=learning_rate)

        if ModelDQN.USE_CUDA:
            self._model.cuda()
        if model_path is not None:
            self._model.load_state_dict(torch.load(model_path))

    def write_state_to_path(self, path):
        torch.save(self._model.state_dict(), path)

    def train(self, num_episodes=10, agent=None, print_mod=1):
        self._run += 1
        actions = 0
        self._steps_done = 0
        time_start = time.time()
        agent = AgentExact(self._seed + self._run) if agent is None else agent

        for idx in range(num_episodes):
            # Initialize the environment and state
            if idx % print_mod == 0 or time.time() - time_last > 30:
                sys.stdout.write(
                    " {:0>5}/{:0>5}/{:0>5}:".format(self._steps_done, idx, len(self._memory)))
                sys.stdout.flush()
                time_last = time.time()
            game = Game()
            state = TrainerDQN.game_to_state(game)
            score_previous = game.score()
            done = False
            while not game.over():
                # Select and perform an action
                actions += 1
                action = self._select_action(state)
                move = TrainerDQN.action_tensor_to_int(action)
                game.move(move)

                player_two_acted = False
                while game.turn_player() != 1 and not game.over():
                    player_two_acted = True
                    game.move(agent.move(game))

                # Observe new state
                reward = TrainerDQN.game_to_reward(
                    score_previous, game, player_two_acted)
                next_state = torch.FloatTensor([-1] + [0] * 11) if \
                    game.over() else TrainerDQN.game_to_state(game)

                # Store the transition in memory
                self._memory.push(state, action, next_state, reward)

                # Move to the next state
                state = next_state
                score_previous = game.score()

                # Perform one step of the optimization (on the target network)
                if actions % 5 == 0:
                    self._optimize_model()

        aps = actions / (time.time() - time_start)
        print(' :EOF {:.2f} action/second'.format(aps))

    def _optimize_model(self):

        if not self._memory.full:
            return
        (state_batch, action_batch, state_next_batch, reward_batch) = \
            self._memory.sample(self._BATCH_SIZE)

        indices_normal = []
        indices_final = []
        for idx, value in enumerate(state_next_batch[:, 0]):
            if value != -1:
                indices_normal.append(idx)

        # Compute a mask of non-final states and concatenate the batch elements
        mask_normal = torch.LongTensor(indices_normal)
        mask_bit_normal = state_next_batch[:, 0] != -1
        if ModelDQN.USE_CUDA:
            mask_bit_normal = mask_bit_normal.cuda()
            # mask_normal = mask_normal.cuda()

        # We don't want to backprop through the expected action values and
        # volatile will save us on temporarily changing the model parameters'
        # requires_grad to False!
        state_batch = ModelDQN.Variable(state_batch)
        action_batch = ModelDQN.Variable(action_batch)
        reward_batch = ModelDQN.Variable(reward_batch)

        # Compute Q(s_t, a) - the model computes Q(s_t), then we select the
        # columns of actions taken
        state_action_values = self._model(state_batch)
        state_action_values = state_action_values.gather(1, action_batch)

        # Compute V(s_{t+1}) for all next states.
        next_state_values = ModelDQN.Variable(torch.zeros(self._BATCH_SIZE))
        state_next_batch_normal = ModelDQN.Variable(
            state_next_batch.index_select(0, mask_normal), True)

        next_state_values[mask_bit_normal] = self._model(
            state_next_batch_normal).max(1)[0]

        # Now, we don't want to mess up the loss with a volatile flag, so let's
        # clear it. After this, we'll just end up with a Variable that has
        # requires_grad=False
        # next_state_values.volatile = False
        # Compute the expected Q values
        expected_state_action_values = (next_state_values * self._GAMMA) + \
            reward_batch

        # Compute Huber loss
        loss = F.smooth_l1_loss(state_action_values,
                                expected_state_action_values)

        # if self._memory.position % 200 == 0:
        #     print("Loss: ", loss.data[0])

        # Optimize the model
        self._optimizer.zero_grad()
        loss.backward()
        for param in self._model.parameters():
            param.grad.data.clamp_(-1, 1)
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
                0.5 * (score[0] - score_previous[0])
            # reward = 0

        return torch.Tensor([reward])

    @staticmethod
    def action_tensor_to_int(action):
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
                ModelDQN.Variable(state.unsqueeze(0))
            ).data.max(1)[1][0].cpu()
        else:
            return torch.LongTensor([random.randrange(6)])


class ModelDQN(nn.Module):
    """The DQN Model. From the 12 slots, pick of the six choices"""
    USE_CUDA = torch.cuda.is_available()

    def __init__(self):
        super(ModelDQN, self).__init__()
        self.layer1 = nn.Linear(12, 32)
        self.layer2 = nn.Linear(32, 64)

        self.conv1 = nn.Conv2d(1, 32, kernel_size=2, stride=1)
        # aside from batch - this flattens to size 160
        # torch.Size([batch, 32, 1, 5])
        self.bn1 = nn.BatchNorm2d(32)

        self.layer3 = nn.Linear(64 + 160, 128)
        self.layer4 = nn.Linear(128, 64)
        self.layer5 = nn.Linear(64, 6)

    def forward(self, input_vector):
        # x is batch*state
        # x is batch*12
        # i should be batch*1*2*6

        x1 = F.relu(self.layer1(input_vector))
        x2 = F.relu(self.layer2(x1))  # linear result

        i = ModelDQN.linear_batch_to_img(input_vector)
        i2 = F.relu(self.bn1(self.conv1(i)))
        # i3 = F.relu(self.bn2(self.conv2(i2)))
        # i4 = F.relu(self.bn3(self.conv3(i3)))
        i3 = i2.view(i2.size(0), -1)  # cnn result

        joined = torch.cat([x2, i3], 1)

        j = F.relu(self.layer3(joined))
        j3 = F.relu(self.layer4(j))
        j4 = self.layer5(j3)

        return j4

    @staticmethod
    def linear_batch_to_img(linear_batch):
        y = linear_batch.unsqueeze(1)
        z = torch.split(y, 6, 2)
        result = torch.stack(z, 2)
        return result

    @staticmethod
    def Variable(tensor, volatile=False):
        if ModelDQN.USE_CUDA:
            tensor = tensor.cuda()
        return Variable(tensor, volatile=volatile)

    @staticmethod
    def Seed(seed):
        torch.manual_seed(seed)
        if ModelDQN.USE_CUDA:
            torch.cuda.manual_seed_all(seed)


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
        self.position = 0
        self.states = torch.zeros(capacity, 12)
        self.actions = torch.zeros(capacity, 1).type(torch.LongTensor)
        self.states_next = torch.zeros(capacity, 12)
        self.rewards = torch.zeros(capacity, 1)
        self.full = False
        if ModelDQN.USE_CUDA:
            self.states.cuda()
            self.actions.cuda()
            self.states_next.cuda()
            self.rewards.cuda()

    def push(self, state, action, state_next, reward):
        """Saves a transition."""
        self.states[self.position] = state
        self.actions[self.position] = action
        self.states_next[self.position] = state_next
        self.rewards[self.position] = reward
        self.position = (self.position + 1) % self.capacity
        self.full = self.full or self.position == 0

    def sample(self, batch_size):
        """Sample from the memories"""
        rand_batch = torch.randperm(self.capacity)
        index = torch.split(rand_batch, batch_size)[0]
        states_batch = self.states[index]
        action_batch = self.actions[index]
        states_next_batch = self.states_next[index]
        rewards_batch = self.rewards[index]
        return (states_batch, action_batch, states_next_batch, rewards_batch)

    def __len__(self):
        return self.capacity if self.full else self.position
