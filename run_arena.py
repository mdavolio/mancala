
import os
import argparse
import csv

from mancala.agents.random import AgentRandom
from mancala.agents.max_min import AgentMinMax
from mancala.agents.max import AgentMax
from mancala.agents.exact import AgentExact
from mancala.arena import Arena


# Create an A3C Agent if pytorch is available in any form
try:
    import torch
    from mancala.agents.a3c import AgentA3C
    dtype = torch.cuda.FloatTensor if torch.cuda.is_available() else torch.FloatTensor
    AGENT_A3C = ("A3C", lambda seed: AgentA3C(
        os.path.join("models", "a3c.model"), dtype, seed))
except ImportError:
    AGENT_A3C = None


PARSER = argparse.ArgumentParser(
    description='Run the arena with availabe agents')

PARSER.add_argument('--output', type=str, default='arena.results.csv',
                    help='Path to write arena results')

ARGS = PARSER.parse_args()

print('Starting arena')

agents = [
    # Place agents in this list as created
    # first in the tuple is the readable name
    # second is a lambda that ONLY takes a random seed. This can be discarded
    # if the the Agent does not require a seed
    ("Random", lambda seed: AgentRandom(seed)),
    ('Max', lambda seed: AgentMax(seed)),
    ('Exact', lambda seed: AgentExact(seed)),
    ('MinMax', lambda seed: AgentMinMax(seed, depth=3))
]
if AGENT_A3C is not None:
    agents.append(AGENT_A3C)

ARENA = Arena(agents, 500)


print('Run the arena for: ', ARENA.csv_header())

with open(ARGS.output, 'w') as f:
    WRITER = csv.writer(f)
    WRITER.writerow(ARENA.csv_header())
    WRITER.writerows(ARENA.csv_results_lists())

print('Complete')
# print(AgentRandom().move(4))

# Agent().move()
