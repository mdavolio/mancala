
import argparse
import csv

from mancala.agents.random import AgentRandom
from mancala.arena import Arena


PARSER = argparse.ArgumentParser(
    description='Run the arena with availabe agents')

PARSER.add_argument('--output', type=str, default='arena.results.csv',
                    help='Path to write arena results')

ARGS = PARSER.parse_args()

print('Starting arena')

ARENA = Arena([
    # Place agents in this list as created
    # first in the tuple is the readable name
    # second is a lambda that ONLY takes a random seed. This can be discarded
    # if the the Agent does not require a seed
    ("Random", lambda seed: AgentRandom(seed)),
    
], 500)

print('Run the arena for: ', ARENA.csv_header())

with open(ARGS.output, 'w') as f:
    WRITER = csv.writer(f)
    WRITER.writerow(ARENA.csv_header())
    WRITER.writerows(ARENA.csv_results_lists())

print('Complete')
# print(AgentRandom().move(4))

# Agent().move()
