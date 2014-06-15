__author__ = 'Hayssam'

# -----------
# User Instructions:
#
# Modify the the search function so that it returns
# a shortest path as follows:
#
# [['>', 'v', ' ', ' ', ' ', ' '],
#  [' ', '>', '>', '>', '>', 'v'],
#  [' ', ' ', ' ', ' ', ' ', 'v'],
#  [' ', ' ', ' ', ' ', ' ', 'v'],
#  [' ', ' ', ' ', ' ', ' ', '*']]
#
# Where '>', '<', '^', and 'v' refer to right, left,
# up, and down motions. NOTE: the 'v' should be
# lowercase.
#
# Your function should be able to do this for any
# provided grid, not just the sample grid below.
# ----------


# Sample Test case
grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0]]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

cost = 1

# ----------------------------------------
# modify code below
# ----------------------------------------

def search(grid, init, goal, cost):
    path = []

    expand = [[-1 for row in range(len(grid[0]))] for col in range(len(grid))]
    expand[init[0]][init[1]] = 0

    closed = [[0 for row in range(len(grid[0]))] for col in range(len(grid))]
    closed[init[0]][init[1]] = 1

    x = init[0]
    y = init[1]
    g = 0
    step = 1

    open = [[g, x, y]]

    found = False  # flag that is set when search is complet
    resign = False # flag set if we can't find expand

    while not found and not resign:
        if len(open) == 0:
            resign = True
            return 'fail'
        else:
            open.sort()
            open.reverse()
            next = open.pop()
            x = next[1]
            y = next[2]
            g = next[0]

            if x == goal[0] and y == goal[1]:
                found = True
            else:
                for i in range(len(delta)):
                    x2 = x + delta[i][0]
                    y2 = y + delta[i][1]
                    if 0 <= x2 < len(grid) and 0 <= y2 < len(grid[0]):
                        if closed[x2][y2] == 0 and grid[x2][y2] == 0:
                            path.append([[x, y], [x2, y2]])

                            g2 = g + cost
                            open.append([g2, x2, y2])
                            closed[x2][y2] = 1

                            expand[x2][y2] = step
                            step += 1

    success = False
    path1 = [[p] for p in path if p[0] == init]
    while not success:
        for p1 in path1:
            potentials = [p for p in path if p1[-1][1] == p[0]]
            if not potentials:
                path1.remove(p1)
            else:
                for l in potentials:
                    branches = [[p1] for count in range(len(l))]
                    for branch in branches:
                        branch.append(l)
                        path1.append(branch)
            if p1[-1][1] == goal:
                success = True

    route_prelim = path1[-1]

    path_grid = [[' ' for columns in range(len(grid[0]))] for rows in range(len(grid))]

    route = []
    done = False
    while not done:
        try:
            next = route_prelim[-1]
            route.append(next)
            route_prelim = route_prelim[0]
        except TypeError:
            route = route[:len(route) - 2]
            done = True
    route.reverse()

    for r in route:
        for m in range(len(delta)):
            if r[1][0] == r[0][0] + delta[m][0] and r[1][1] == r[0][1] + delta[m][1]:
                path_grid[r[0][0]][r[0][1]] = delta_name[m]
    path_grid[goal[0]][goal[1]] = '*'

    for g in path_grid:
        print g

    return path_grid

search(grid, init, goal, cost)