__author__ = 'Hayssam'

# -----------
# User Instructions
#
# Define a function smooth that takes a path as its input
# (with optional parameters for weight_data, weight_smooth,
# and tolerance) and returns a smooth path. The first and
# last points should remain unchanged.
#
# Smoothing should be implemented by iteratively updating
# each entry in newpath until some desired level of accuracy
# is reached. The update should be done according to the
# gradient descent equations given in the previous video.
# -----------

from copy import deepcopy

# thank you to EnTerr for posting this on our discussion forum
def printpaths(path,newpath):
    for old,new in zip(path,newpath):
        print '['+ ', '.join('%.3f'%x for x in old) + \
               '] -> ['+ ', '.join('%.3f'%x for x in new) +']'

# Don't modify path inside your function.
path = [[0, 0],
        [0, 1],
        [0, 2],
        [1, 2],
        [2, 2],
        [3, 2],
        [4, 2],
        [4, 3],
        [4, 4]]

def smooth(path, weight_data=0.5, weight_smooth=0.1, tolerance=0.000001):

    #######################
    ### ENTER CODE HERE ###
    #######################

    # Make a deep copy of path into newpath
    newpath = deepcopy(path)

    alpha = weight_data
    beta = weight_smooth
    diff = 1

    while diff > tolerance:  # keep going until the difference is less than tolerance
        diff = 0  # reset to zero to capture this cycle's diff
        for i in range(len(path) - 1):  # through each row
            for j in range(len(path[0])):  # through each column [a,b]
                if i != 0:  # skip first row (find a way to skip first row) - use look back calc
                    data_change = alpha * (path[i][j] - newpath[i][j])
                    smooth_change = beta * (newpath[i + 1][j] + newpath[i - 1][j] - 2 * newpath[i][j])
                    newpath[i][j] += data_change
                    newpath[i][j] += smooth_change
                    diff += abs(data_change + smooth_change)

    return newpath  # Leave this line for the grader!

smooth(path, weight_data=0.5, weight_smooth=0.1, tolerance=0.000001)
printpaths(path, smooth(path))
