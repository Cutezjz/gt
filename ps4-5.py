# --------------
# USER INSTRUCTIONS
#
# Write a function called stochastic_value that
# returns two grids. The first grid, value, should
# contain the computed value of each cell as shown
# in the video. The second grid, policy, should
# contain the optimum policy for each cell.
#
# --------------
# GRADING NOTES
#
# We will be calling your stochastic_value function
# with several different grids and different values
# of success_prob, collision_cost, and cost_step.
# In order to be marked correct, your function must
# RETURN (it does not have to print) two grids,
# value and policy.
#
# When grading your value grid, we will compare the
# value of each cell with the true value according
# to this model. If your answer for each cell
# is sufficiently close to the correct answer
# (within 0.001), you will be marked as correct.

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

delta_name = ['^', '<', 'v', '>'] # Use these when creating your policy grid.

# ---------------------------------------------
#  Modify the function stochastic_value below
# ---------------------------------------------

def stochastic_value(grid,goal,step_cost,collision_cost,success_prob):
    failure_prob = (1.0 - success_prob)/2.0  # Probability(stepping left) = prob(stepping right) = failure_prob
    value = [[1000 for row in range(len(grid[0]))] for col in range(len(grid))]
    policy = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]

#######################################################################################################################
    change = True
    while change:
        change = False

        for x in range(len(grid)):
            for y in range(len(grid[0])):
                if goal[0] == x and goal[1] == y:
                    if value[x][y] > 0:
                        value[x][y] = 0
                        policy[x][y] = '*'

                        change = True

                elif grid[x][y] == 0:
                    for a in range(len(delta)):

                        xf = x + delta[a][0]
                        yf = y + delta[a][1]

                        xr = x + delta[(a + 1) % len(delta)][0]
                        yr = y + delta[(a + 1) % len(delta)][1]

                        xl = x + delta[(a + 3) % len(delta)][0]
                        yl = y + delta[(a + 3) % len(delta)][1]

                        v2 = 0

                        if 0 <= xf < len(grid) and 0 <= yf < len(grid[0]) and grid[xf][yf] == 0:
                            v2 += value[xf][yf] * success_prob
                        else:
                            v2 += collision_cost * success_prob

                        if 0 <= xr < len(grid) and 0 <= yr < len(grid[0]) and grid[xr][yr] == 0:
                            v2 += value[xr][yr] * failure_prob
                        else:
                            v2 += collision_cost * failure_prob

                        if 0 <= xl < len(grid) and 0 <= yl < len(grid[0]) and grid[xl][yl] == 0:
                            v2 += value[xl][yl] * failure_prob
                        else:
                            v2 += collision_cost * failure_prob

                        v2 += step_cost

                        if v2 < value[x][y]:
                                change = True
                                value[x][y] = v2
                                policy[x][y] = delta_name[a]

# #######################################################################################################################

    return value, policy

# ---------------------------------------------
#  Use the code below to test your solution
# ---------------------------------------------

grid = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 1, 1, 0]]
goal = [0, len(grid[0])-1]  # Goal is in top right corner
step_cost = 1
collision_cost = 100
success_prob = 0.5

value, policy = stochastic_value(grid, goal, step_cost, collision_cost, success_prob)
for row in value:
    print row
for row in policy:
    print row

# Expected outputs:
#
# [57.9029, 40.2784, 26.0665,  0.0000]
# [47.0547, 36.5722, 29.9937, 27.2698]
# [53.1715, 42.0228, 37.7755, 45.0916]
# [77.5858, 1000.00, 1000.00, 73.5458]
#
# ['>', 'v', 'v', '*']
# ['>', '>', '^', '<']
# ['>', '^', '^', '<']
# ['^', ' ', ' ', '^']