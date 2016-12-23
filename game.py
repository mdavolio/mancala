import numpy as np

grid  = np.array([[4,4,4,4,4,4], [4,4,4,4,4,4]])
print(grid)

p1_score = 0
p2_score = 0
stones_1 = np.sum(grid[0,:])
stones_2 = np.sum(grid[1,:])

def score():
    global p1_score
    global p2_score
    if player == 1:
        p1_score += 1
        return p1_score
    elif player == 2:
        p2_score += 1
        return p2_score
    count = count - 1
    return

def move(x,y):
    global player
    global count

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
                x = 1
                score()
            else:
                grid[x,y] += 1

        elif x == 1:
            y += 1

            if y == 6:
                x = 0
                score()
            else:
                grid[x,y] += 1

        count -= 1

        stones_1 = np.sum(grid[0,:])
        stones_2 = np.sum(grid[1,:])

        # print(count)
        # print(grid)
        # print(p1_score)
        # print(p2_score)
    return
