from game import *
import sys


while stones_1 > 0 and stones_2 > 0:
    print('Which Player are you?')
    sys.stdout.flush()
    p = int(raw_input()) - 1

    print('Which hole would you like to move?')
    sys.stdout.flush()
    h = int(raw_input())

    move(p,h)
