### Play file
### Code to run game

from game import *
import sys

### Start with player 1
p = 0

### Continue game while still stones in play
while stones_1 > 0 and stones_2 > 0:

    ### Calculate total stones on board in attempt to calculalte score
    stones_0 = np.sum(grid)

    if p == 0:
        print("Player 1's Turn")
    if p == 1:
        print("Player 2's Turn")
    print(grid)

    ### Player chooses which hole, currently 0-5
    print('Which hole would you like to move?')
    sys.stdout.flush()
    h = int(raw_input())

    ### Run move function, doesn't calculate score
    move(p,h)

    ### Calculate stones on board in attempt to calculate score
    stones_1 = np.sum(grid[0,:])
    stones_2 = np.sum(grid[1,:])
    stones_N = np.sum(grid)

    # Score calculator based on stones remaining in play
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
