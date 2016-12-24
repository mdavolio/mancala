from game import *
import sys

p = 0

while stones_1 > 0 and stones_2 > 0:

    if p == 0:
        print("Player 1's Turn")
    if p == 1:
        print("Player 2's Turn")
    print(grid)

    print('Which hole would you like to move?')
    sys.stdout.flush()
    h = int(raw_input())

    move(p,h)

    if p == 0:
        p = 1
    elif p == 1:
        p = 0

    stones_1 = np.sum(grid[0,:])
    stones_2 = np.sum(grid[1,:])

    print stones_1
    # print(player)
    # print(p1_score)
    # print(p2_score)
    print('\n')
