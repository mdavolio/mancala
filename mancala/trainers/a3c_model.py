
import torch
import torch.nn as nn
import torch.nn.init as init
import torch.nn.functional as F
from torch.autograd import Variable


def normalized_columns_initializer(weights, std=1.0):
    out = torch.randn(weights.size())
    out *= std / torch.sqrt(out.pow(2).sum(1).expand_as(out))
    return out


def weights_init(m):
    classname = m.__class__.__name__
    if classname.find('Linear') != -1:
        init.xavier_uniform(m.weight.data)
        m.bias.data.fill_(0)


class ActorCritic(torch.nn.Module):

    def __init__(self, num_inputs, action_space):
        super(ActorCritic, self).__init__()
        self.linear1 = nn.Linear(num_inputs, 512)
        self.linear1_dropout = nn.Dropout(p=0.2)
        self.linear2 = nn.Linear(512, 400)

        self.lstm = nn.LSTMCell(400, 400)

        num_outputs = action_space.n
        self.critic_linear = nn.Linear(400, 1)
        self.actor_linear = nn.Linear(400, num_outputs)

        self.apply(weights_init)

        self.train()

    def forward(self, inputs):
        inputs, (hx, cx) = inputs
        y = F.elu(self.linear1_dropout(self.linear1(inputs)))
        x = F.elu(self.linear2(y))

        hx, cx = self.lstm(x, (hx, cx))

        x = hx

        return self.critic_linear(x), self.actor_linear(x), (hx, cx)