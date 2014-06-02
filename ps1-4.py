__author__ = 'Hayssam'

#world
colors = [['red', 'green', 'green',   'red', 'red'],
          ['red',   'red', 'green',   'red', 'red'],
          ['red',   'red', 'green', 'green', 'red'],
          ['red',   'red',   'red',   'red', 'red']]

# colors = [['green', 'green', 'green'],
#           ['green',   'red', 'red'],
#           ['green', 'green', 'green']]

measurements = ['green', 'green', 'green', 'green', 'green']
# measurements = ['red', 'red']
p = [[1./20, 1./20, 1./20, 1./20, 1./20],
     [1./20, 1./20, 1./20, 1./20, 1./20],
     [1./20, 1./20, 1./20, 1./20, 1./20],
     [1./20, 1./20, 1./20, 1./20, 1./20]]

motions = [[0, 0], [0, 1], [1, 0], [1, 0], [0, 1]]
# motions = [[0, 0], [0, 1]]

#probability that sensor measurement is correct
sensor_right = 0.7
# sensor_right = 1.0

#probability that motion is executed correctly
p_move = 0.8
# p_move = 0.5

def show(p):
    for i in range(len(p)):
        print p[i]

#Do not delete this comment!
#Do not use any import statements.
#Adding or changing any code above may
#cause the assignment to be graded incorrectly.

#rows and columns are given.  this should allow for arbitrary size
rows = 4
columns = 5
# rows = 3
# columns = 3

# create p and initialize it to maximum doubt
p = []
for row in range(rows):
    p.append([1./(rows * columns) for column in range(columns)])



def move(p, p_move, motion):
    q = []
    for row in range(rows):
        q.append([None for column in range(columns)])

    if motion == [0, 0]:
        for row in range(len(p)):
            for column in range(columns):
                s = p_move * p[row][column]
                q[row][column] = s

    if motion == [0, 1]:  # move right
        for row in range(len(p)):
            for column in range(columns):
                s = (1 - p_move) * p[row][column]
                s += p_move * p[row][(column - 1) % columns]
                q[row][column] = s

    if motion == [0, -1]:  # move left
        for row in range(len(p)):
            for column in range(columns):
                s = (1 - p_move) * p[row][column]
                s += p_move * p[row][(column + 1) % columns]
                q[row][column] = s

    if motion == [1, 0]:  # move down
        for row in range(len(p)):
            for column in range(columns):
                s = (1 - p_move) * p[row][column]
                s += p_move * p[(row - 1) % rows][column]
                q[row][column] = s

    if motion == [-1, 0]:  # move up
        for row in range(len(p)):
            for column in range(columns):
                s = (1 - p_move) * p[row][column]
                s += p_move * p[(row + 1) % rows][column]
                q[row][column] = s
    return q


def sense(p, sensor_right, measurement):
    q = []
    for row in range(rows):
        q.append([None for column in range(columns)])

    for row in range(rows):
        for column in range(columns):
            if colors[row][column] == measurement:
                q[row][column] = sensor_right * p[row][column]
            else:
                q[row][column] = (1 - sensor_right) * p[row][column]

    s = sum([sum(row) for row in q])
    for row in range(rows):
        for column in range(columns):
            q[row][column] = q[row][column]/s

    return q

for step in range(len(measurements)):
    p = move(p, p_move, motions[step])
    p = sense(p, sensor_right, measurements[step])


s = 0
for row in p:
    s += sum(row)
print s

#Your probability array must be printed
#with the following code.

show(p)