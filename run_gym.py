
import argparse
import json
import os

from mancala.gym import Gym


PARSER = argparse.ArgumentParser(
    description='Train an agent')

PARSER.add_argument('--agent', type=str, required=True,
                    help='Agent str id to use')

PARSER.add_argument('--verbose', action="store_true", default=True,
                    help='Log verbose results')

PARSER.add_argument('--input', type=str,
                    help='Path to read json trained start data')

PARSER.add_argument('--config', type=str,
                    help='Path to read json configuration data')

PARSER.add_argument('--output', type=str, required=True,
                    help='Path to write json trained results')

ARGS = PARSER.parse_args()
# ARGS = PARSER.parse_args(([
#     '--output',
#     'training/results.json',
#     '--agent',
#     'qbinary',
#     '--verbose'
# ]))


print('Starting gym')

def load_path(path):
    """Load data if exists, else None"""
    if path is not None and os.path.exists(path):
        with open(path) as json_data:
            return json.load(json_data)
    return None


def load_data(input_path, config_path):
    """Load data paths if they exist"""
    input_data = load_path(input_path)
    config_data = load_path(config_path)
    return input_data, config_data


def handle_agent(input_data, config_data, agent_name, verbose):
    """Do agent work"""
    agent = agent_name.lower()
    if agent == "qbinary":
        return Gym.qbinary(input_data, config_data, verbose)
    if agent == "qquad":
        return Gym.qquad(input_data, config_data, verbose)

    print("Agent id of {} not recognized.".format(agent_name))
    return None

INPUT_DATA, CONFIG_DATA = load_data(ARGS.input, ARGS.config)

RESULTS = handle_agent(INPUT_DATA, CONFIG_DATA, ARGS.agent, ARGS.verbose)

with open(ARGS.output, 'w') as f:
    json.dump(RESULTS, f)

print('Complete')
