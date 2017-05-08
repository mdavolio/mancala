# Mancala
[![Build Status](https://travis-ci.org/mdavolio/mancala.svg?branch=master)](https://travis-ci.org/mdavolio/mancala)

Simulator and Agents for the game of [Mancala](https://en.wikipedia.org/wiki/Mancala). Mancala is a 2-player, turn-based strategy board game based on small stones on a board. The objective is to capture more stones than your opponent.

This project implements the game logic, multiple interfaces, and a variety of AI bots.

## Agents

| Agent  | Description                                                |
|--------|------------------------------------------------------------|
| Random | From valid moves, selects randomly                         |
| Max    | Maximize score increase for that turn                      |
| Exact  | Maximizes repeating turns                                  |
| MinMax | Implements Min/Max tree exploration with alpha/beta tuning |
| A3C    | Implements an Actor-Critic Reinforcement Learner           |

![Agent Performance](www/performance_results.png "Agent Performance")


## Play

Run with `python server.py` or `make serve` and browse to `http://127.0.0.1:5000/` to play Mancala.

![Mancala GUI](www/mancala_gui.png "Mancala GUI")

Play in the terminal with `python play.py` or `make play`

![Mancala Terminal](www/mancala_terminal.png "Mancala Terminal")

## Test

Run the unittest tests with `python -m unittest discover` or `make test`. Tests are also run on Travis CI [![Build Status](https://travis-ci.org/mdavolio/mancala.svg?branch=master)](https://travis-ci.org/mdavolio/mancala).