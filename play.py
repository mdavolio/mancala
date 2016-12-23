from game import *
import sys




print('Which Player are you?')
sys.stdout.flush()
p = int(raw_input()) - 1

print('Which hole would you like to move?')
sys.stdout.flush()
h = int(raw_input())

move(p,h)
