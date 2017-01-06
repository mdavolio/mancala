### Game file
### Code for a turn

import numpy as np

### creates board, 2 players by 6 holes
### current testing situations:
### Player 1: testing
### Player 2: Full
grid  = np.array([[3,1,0,0,0,0], [4,4,4,4,4,4]])
# print(grid)

global p1_score, p2_score ### score tracker
global stones_1, stones_2 ### Number of total stones a player has
global player ### Player Number

p1_score = 0
p2_score = 0
stones_1 = np.sum(grid[0,:]) ### Sum total player 1 remaining
stones_2 = np.sum(grid[1,:]) ### Sum total player 2 remaining

### called when a player scores a point
def score():
    if player == 1:
        p1_score += 1
        return p1_score
    elif player == 2:
        p2_score += 1
        return p2_score
    count = count - 1 ### Calculates for stone placed in end hole
    return

### Called to calculate moves
def move(x,y):
    global player
    global count ### number of stones in chosen hole`
    global p1_score
    global p2_score

    # print(x)

    ### defines player variable
    if x == 0:
        player = 1
    elif x == 1:
        player = 2
    # print('player: ', player)

    ### Calculate stones in chosen hole
    count = grid[x,y]

    # grid[x,y] = 0

    ### While still stones to move
    while count > 0:
        if x == 0:
            y -= 1 ### Player one moves right to left

            if y == -1: ### Switch direction when y goes negative
                x = 1
                # if player == 1:
                #    p1_score += 1
            else:
                grid[x,y] += 1

        elif x == 1:
            y += 1 ### Player two moves left to right

            if y == 6: ### Switch directions when y gets to end of board
                x = 0
                # if player == 2:
                #    p2_score +=1
            else:
                grid[x,y] += 1

        count -= 1 ### one less stone to move

        # print(count)
        # print(grid)
        # print(p1_score)
        # print(p2_score)
    return
