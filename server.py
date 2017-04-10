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


FLASKAPP = Flask(__name__)
FLASKAPP.config.from_object(__name__)

# Define agents
AGENT_RANDOM = AgentRandom(454)
AGENT_MAX = AgentMax(454)
AGENT_MINNY = AgentMinMax(454, 8)


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
    return game


@FLASKAPP.route('/time')
def time():
    """Returns current time"""
    return jsonify({'current_time': datetime.datetime.utcnow().isoformat()})


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
