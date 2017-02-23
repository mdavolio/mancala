# -*- coding: utf-8 -*-

from flask import Flask, jsonify
from flask import send_from_directory
import datetime
import os


app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def show():
    """Returns current time"""
    return jsonify({ 'current_time': datetime.datetime.utcnow().isoformat() })


@app.route('/<path:filename>')
def serve_static(filename):
    full_path = os.path.join(os.getcwd(), 'www')
    return send_from_directory(full_path, filename)

app.run()
