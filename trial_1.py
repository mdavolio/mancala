import numpy as np

grid  = np.array([[0,1,2,3,4,5], [4,4,4,4,4,4]])
print(grid)


def score():
    if player == 1:
        p1_score += 1
        return p1_score
    elif player == 2:
        p2_score += 1
        return p2_score
    count = count - 1
    return count

def move(x,y):
    if x == 0:
        player = 1
    elif x == 1:
        player = 2

    count = grid[x,y]

    while count
    print(count)
    print(player)





move(1,2)
