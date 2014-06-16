__author__ = 'Hayssam'

# ----------
# User Instructions:
#
# Create a function compute_value() which returns
# a grid of values. Value is defined as the minimum
# number of moves required to get from a cell to the
# goal.
#
# If it is impossible to reach the goal from a cell
# you should assign that cell a value of 99.

# ----------

grid = [[0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0]]

rows = len(grid) - 1
cols = len(grid[0]) - 1

goal = [len(grid)-1, len(grid[0])-1]


delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

# print 'up--->', [goal[0] + delta[0][0], goal[1] + delta[0][1]]
# print 'down--->', [goal[0] + delta[2][0], goal[1] + delta[2][1]]


delta_name = ['^', '<', 'v', '>']

cost = 1 # the cost associated with moving from a cell to an adjacent one.

# ----------------------------------------
# insert code below
# ----------------------------------------
def compute_value(grid, goal, cost):
    value = [[99 for columns in range(len(grid[0]))] for rows in range(len(grid))]

    # start at goal
    row = goal[0]
    col = goal[1]
    value[row][col] = 0

    def find_neighbors(cell):
        neighbors = []
        for i in range(len(delta)):
            r2 = cell[0] + delta[i][0]
            c2 = cell[1] + delta[i][1]
            if 0 <= r2 <= rows and 0 <= c2 <= cols:
                if grid[r2][c2] == 0 and value[r2][c2] == 99:
                    neighbors.append([r2, c2])
        return neighbors

    def find_next_cells(v):
        l = []
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if value[row][col] == v:
                    l.append([row, col])
        return l

    def update(cell, v):
        value[cell[0]][cell[1]] = v + 1

    cv = 0
    done = False
    while not done:
        if not find_next_cells(cv):
            done = True
        else:
            list1 = find_next_cells(cv)
            for e in list1:
                for d in find_neighbors(e):
                    update(d, cv)
            cv += 1

    for row in value:
        print row
    return value #make sure your function returns a grid of values as demonstrated in the previous video.

compute_value(grid, goal, cost)