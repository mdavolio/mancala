# Play file
# Code to run game

from game import Game
import sys

game_current = Game()

while not game_current.over():
    # print("\n" * 100) # Screen clearing *hack*
    print("Play Mancala!")
    print("")
    print("Score | Player One | Player Two")
    print("        {0: >10} | {1: >10}".format(
          game_current.score()[0], game_current.score()[1]))
    print(game_current.board_render())
    print("Player {0}'s Turn".format(game_current.turn_player()))
    i = input()
    if (i == 'q'):
        break
    try:
        m = int(i)
        game_current.move(m)
    except:
        print("Unable to play that move...")
        pass
