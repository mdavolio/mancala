# -*- coding: utf-8 -*-
"""
Play file
Code to run game in the terminal
"""

from mancala.game import Game

# def Play():
GAME_CURRENT = Game()

def clear_screen():
    """Screen clearing *hack*"""
    print("\n" * 100)


clear_screen()
while not GAME_CURRENT.over():
    print("Play Mancala!")
    print("")
    print("Score | Player One | Player Two")
    print("        {0: >10} | {1: >10}".format(
        GAME_CURRENT.score()[0], GAME_CURRENT.score()[1]))
    print(GAME_CURRENT.board_render())
    print("Player {0}'s Turn".format(GAME_CURRENT.turn_player()))
    i = input()
    if i == 'q':
        break
    clear_screen()
    try:
        GAME_CURRENT.move(int(i))
    except ValueError:
        print("Invalid Move")

