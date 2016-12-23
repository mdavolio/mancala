from game import *
import sys

while p1_stones > 0 and p2_stones > 0:
    print('Which Player are you?')
    sys.stdout.flush()
    p = int(raw_input()) - 1

    print('Which hole would you like to move?')
    sys.stdout.flush()
    h = int(raw_input())

    move(p,h)

    print(p1_score)
    print(p2_score)
