# -*- coding: utf-8 -*-

from flask import Flask, jsonify
from flask import send_from_directory
from utility import split_string
from game import Game
import datetime
import os


app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def show():
    """Returns current time"""
    return jsonify({ 'current_time': datetime.datetime.utcnow().isoformat() })

@app.route('/play/<string:board>/<int:player_turn>/<int:move>')
def show_user_profile(board, player_turn, move):
    board_arr = split_string(board, 2)

    if (len(board_arr) != 14):
        return jsonify({"error": "Invalid Board"}), 400

    if (player_turn != 1 and player_turn != 2):
        return jsonify({"error": "Invalid Player"}), 400

    if (move < 0 or move > 13):
        return jsonify({"error": "Invalid move"}), 400

    game = Game(board_arr, player_turn)
    game.move(move)
    return jsonify({
        'board': game.board(),
        'player_turn': game.turn_player(),
        'score': game.score(),
        'current_time': datetime.datetime.utcnow().isoformat()
    })

@app.route('/<path:filename>')
def serve_static(filename):
    full_path = os.path.join(os.getcwd(), 'www')
    return send_from_directory(full_path, filename)

app.run()
