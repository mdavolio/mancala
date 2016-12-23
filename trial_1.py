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
    grid[x,y] = 0

    while count > 0:
        if x == 0:
            y -= 1

            if y == -1:
                score()
                x == 1
            else:
                grid[x,y] += 1

        if x == 1:
            y += 1

            if y == 6:
                score()
                x == 0
            else:
                grid[x,y] += 1

        count -= 1
        print(count)
        print(grid)
    return
    
move(0,3)
