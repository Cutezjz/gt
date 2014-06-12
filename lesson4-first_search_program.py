__author__ = 'Hayssam'

# ----------
# User Instructions:
#
# Define a function, search() that takes no input
# and returns a list
# in the form of [optimal path length, x, y]. For
# the grid shown below, your function should output
# [11, 4, 5].
#
# If there is no valid path from the start point
# to the goal, your function should return the string
# 'fail'
# ----------

# Grid format:
#   0 = Navigable space
#   1 = Occupied space

grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0]]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1] # Make sure that the goal definition stays in the function.
print 'goal:  ', goal

delta = [[-1, 0 ], # go up
        [ 0, -1], # go left
        [ 1, 0 ], # go down
        [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>']

cost = 1

def search():
    # ----------------------------------------
    # insert code here and make sure it returns the appropriate result
    # ----------------------------------------
    open_list = [[0, init[0], init[1]]]
    checked = []
    rows = len(grid) - 1
    columns = len(grid[0]) - 1
    path = []

    def expand(cell):
        g = cell[0]
        # print 'g:  ', g
        my_cell = [cell[1], cell[2]]
        neighbors = []
        for move in delta:
            new_row = my_cell[0] + move[0]
            new_column = my_cell[1] + move[1]
            if new_row <= rows and new_row >=0 and new_column <= columns and new_column>=0 and grid[new_row][new_column] != 1:
                neighbors.append([new_row, new_column])
        for item in neighbors:
            if item not in checked:
                open_list.append([g + 1, item[0], item[1]])
        return open_list

    success = False
    while not success:
        sorted_open_list = sorted(open_list, key=lambda s: s[0])
        if len(sorted_open_list) >= 1:
            index = sorted_open_list[0]
            if [index[1], index[2]] == goal:
                success = True
                print 'success'
                print index
            else:
                path.append(index)
                print 'path:  ', path
                checked.append([index[1], index[2]])
                print 'checked:  ', checked
                open_list.remove(index)
                print 'open list:  ', open_list
                expand(index)
        else:
            print 'fail'
            break

    return path # you should RETURN your result


search()

