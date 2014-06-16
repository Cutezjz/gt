__author__ = 'Hayssam'

# ----------
# User Instructions:
#
# Write a function optimum_policy() that returns
# a grid which shows the optimum policy for robot
# motion. This means there should be an optimum
# direction associated with each navigable cell from
# which the goal can be reached.
#
# Unnavigable cells as well as cells from which
# the goal cannot be reached should have a string
# containing a single space (' '), as shown in the
# previous video. The goal cell should have '*'.
# ----------

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0]]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

cost = 1 # the cost associated with moving from a cell to an adjacent one

# ----------------------------------------
# modify code below
# ----------------------------------------

def optimum_policy(grid,goal,cost):
    value = [[99 for row in range(len(grid[0]))] for col in range(len(grid))]
    policy = [[99 for row in range(len(grid[0]))] for col in range(len(grid))]
    change = True

    while change:
        change = False

        for x in range(len(grid)):
            for y in range(len(grid[0])):
                if goal[0] == x and goal[1] == y:
                    if value[x][y] > 0:
                        value[x][y] = 0

                        change = True

                elif grid[x][y] == 0:
                    for a in range(len(delta)):
                        x2 = x + delta[a][0]
                        y2 = y + delta[a][1]

                        if x2 >= 0 and x2 < len(grid) and y2 >= 0 and y2 < len(grid[0]) and grid[x2][y2] == 0:
                            v2 = value[x2][y2] + cost

                            if v2 < value[x][y]:
                                change = True
                                value[x][y] = v2

    def find_neighbors(cell):
        neighbors = []
        for i in range(len(delta)):
            r2 = cell[0] + delta[i][0]
            c2 = cell[1] + delta[i][1]
            if 0 <= r2 <= len(grid) - 1 and 0 <= c2 <= len(grid[0]) - 1:
                if grid[r2][c2] == 0:  # and value != 99:
                    neighbors.append([r2, c2])
        return neighbors

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if row == goal[0] and col == goal[1]:
                policy[row][col] = ' '
            elif grid[row][col] == 0:
                index = [row, col]
                neighbors = find_neighbors([row, col])
                minimum = min([value[n[0]][n[1]] for n in neighbors])
                best_neighbor = [n for n in neighbors if value[n[0]][n[1]] == minimum][0]
                for m in range(len(delta)):
                    if best_neighbor[0] == index[0] + delta[m][0] and best_neighbor[1] == index[1] + delta[m][1]:
                        policy[row][col] = delta_name[m]
            else:
                policy[row][col] = ' '

    for row in value:
        print row

    for row in policy:
        print row

    return policy

optimum_policy(grid,goal,cost)

