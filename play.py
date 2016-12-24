from game import *
import sys

p = 0

while stones_1 > 0 and stones_2 > 0:

    stones_0 = np.sum(grid)

    if p == 0:
        print("Player 1's Turn")
    if p == 1:
        print("Player 2's Turn")
    print(grid)

    print('Which hole would you like to move?')
    sys.stdout.flush()
    h = int(raw_input())

    move(p,h)

    stones_1 = np.sum(grid[0,:])
    stones_2 = np.sum(grid[1,:])
    stones_N = np.sum(grid)

    if p == 0:
        p1_score += (stones_0 - stones_N)
        p = 1
    elif p == 1:
        p2_score += (stones_0 - stones_N)
        p = 0

    print('\n')
    print('Player 1 Score: ', p1_score)
    print('Player 2 Score: ', p2_score)
    print('\n')
