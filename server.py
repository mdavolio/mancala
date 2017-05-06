# -*- coding: utf-8 -*-
"""
Flask Server for Mancala games
"""

import datetime
import os
from flask import Flask, jsonify
from flask import send_from_directory
from mancala.utility import split_string
from mancala.game import Game
from mancala.agents.random import AgentRandom
from mancala.agents.max import AgentMax
from mancala.agents.max_min import AgentMinMax
from mancala.agents.exact import AgentExact
from mancala.agents.mcts import AgentMCTS

# Create an A3C Agent if pytorch is available in any form
try:
    import torch
    from mancala.agents.a3c import AgentA3C
    dtype = torch.cuda.FloatTensor if torch.cuda.is_available() else torch.FloatTensor
    AGENT_A3C = AgentA3C(os.path.join("models", "a3c.model"), dtype, 454)
except ImportError:
    AGENT_A3C = None

FLASKAPP = Flask(__name__)
FLASKAPP.config.from_object(__name__)

# Define agents
AGENT_RANDOM = AgentRandom(454)
AGENT_MAX = AgentMax(454)
AGENT_MINNY = AgentMinMax(454, 3)
AGENT_EXACT = AgentExact(454)
AGENT_MCTS = AgentMCTS(454, 3, 500)


def board_str_to_game(board, player_turn):
    """Turns parameters into game or error tuple"""
    board_arr = split_string(board, 2)

    if len(board_arr) != 14:
        return jsonify({"error": "Invalid Board"}), 400

    if player_turn != 1 and player_turn != 2:
        return jsonify({"error": "Invalid Player"}), 400

    game = Game(board_arr, player_turn)
    return game


def agent_play(game, agent_str):
    """Play a game, based on agent string. Or no move."""
    if agent_str == "random":
        game.move(AGENT_RANDOM.move(game))
    elif agent_str == 'max':
        game.move(AGENT_MAX.move(game))
    elif agent_str == 'min_max':
        game.move(AGENT_MINNY.move(game))
    elif agent_str == 'exact':
        game.move(AGENT_EXACT.move(game))
    elif agent_str =='mcts':
        game.move(AGENT_MCTS.move(game))
    return game


@FLASKAPP.route('/time')
def time():
    """Returns current time"""
    return jsonify({'current_time': datetime.datetime.utcnow().isoformat()})


@FLASKAPP.route('/agents')
def agents():
    """Returns available agent strings"""
    agents = ['random', 'max', 'min_max', 'exact', 'mcts']
    if AGENT_A3C is not None:
        agents.append('a3c')
    return jsonify({'agents': agents})


@FLASKAPP.route('/play/<string:board>/<int:player_turn>/<int:move>')
def play_board(board, player_turn, move):
    """Make a move based on a player and a board"""

    if move < 0 or move > 13:
        return jsonify({"error": "Invalid move"}), 400

    game = board_str_to_game(board, player_turn)
    if not isinstance(game, Game):
        return game

    game.move(move)
    return jsonify({
        'board': game.board(),
        'player_turn': game.turn_player(),
        'score': game.score(),
        'game_over': game.over(),
        'current_time': datetime.datetime.utcnow().isoformat()
    })


@FLASKAPP.route('/agent/<string:board>/<int:player_turn>/<string:agent>')
def play_agent(board, player_turn, agent):
    """Make a move based on a player and a board"""

    game = board_str_to_game(board, player_turn)
    if not isinstance(game, Game):
        return game

    game = agent_play(game, agent)

    return jsonify({
        'board': game.board(),
        'player_turn': game.turn_player(),
        'score': game.score(),
        'game_over': game.over(),
        'current_time': datetime.datetime.utcnow().isoformat()
    })


@FLASKAPP.route('/')
def serve_index():
    """Serve index"""
    full_path = os.path.join(os.getcwd(), 'www')
    return send_from_directory(full_path, 'index.html')


@FLASKAPP.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    full_path = os.path.join(os.getcwd(), 'www')
    return send_from_directory(full_path, filename)


FLASKAPP.run()
