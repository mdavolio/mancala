### Game file
### Code for a turn

import numpy as np

class Game():
    def __init__(self):

        ### creates board, 2 players by 6 holes
        ### current testing situations:
        ### Player 1: testing
        ### Player 2: Full
        self.grid  = np.array([[3,1,0,0,0,0], [4,4,4,4,4,4]])
        # print(grid)

        ### score tracker
        self.p1_score = 0
        self.p2_score = 0
        self.player = 1
        ### number of stones in chosen hole`
        self.count = self.grid[0,0] # TODO: Initilize this properly
        ### Number of total stones a player has
        self.stones_1 = np.sum(self.grid[0,:]) ### Sum total player 1 remaining
        self.stones_2 = np.sum(self.grid[1,:]) ### Sum total player 2 remaining

    ### called when a player scores a point
    def _score(self):
        if self.player == 1:
            self.p1_score += 1
            return self.p1_score
        elif self.player == 2:
            self.p2_score += 1
            return self.p2_score
        self.count = self.count - 1 ### Calculates for stone placed in end hole
        return

    ### Called to calculate moves
    def move(self, x, y):
        # print(x)

        ### defines player variable
        if x == 0:
            self.player = 1
        elif x == 1:
            self.player = 2
        # print('player: ', player)

        ### Calculate stones in chosen hole
        self.count = self.grid[x,y]

        # grid[x,y] = 0

        ### While still stones to move
        while self.count > 0:
            if x == 0:
                y -= 1 ### Player one moves right to left

                if y == -1: ### Switch direction when y goes negative
                    x = 1
                    # if player == 1:
                    #    p1_score += 1
                else:
                    self.grid[x,y] += 1

            elif x == 1:
                y += 1 ### Player two moves left to right

                if y == 6: ### Switch directions when y gets to end of board
                    x = 0
                    # if player == 2:
                    #    p2_score +=1
                else:
                    self.grid[x,y] += 1

            self.count -= 1 ### one less stone to move

            # print(count)
            # print(grid)
            # print(p1_score)
            # print(p2_score)
        return self.score()
