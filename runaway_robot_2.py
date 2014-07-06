# ----------
# Part Two
#
# Now we'll make the scenario a bit more realistic. Now Traxbot's
# sensor measurements are a bit noisy (though its motions are still
# completetly noise-free and it still moves in an almost-circle).
# You'll have to write a function that takes as input the next
# noisy (x, y) sensor measurement and outputs the best guess
# for the robot's next position.
#
# ----------
# YOUR JOB
#
# Complete the function estimate_next_pos. You will be considered
# correct if your estimate is within 0.01 stepsizes of Traxbot's next
# true position.
#
# ----------
# GRADING
#
# We will make repeated calls to your estimate_next_pos function. After
# each call, we will compare your estimated position to the robot's true
# position. As soon as you are within 0.01 stepsizes of the true position,
# you will be marked correct and we will tell you how many steps it took
# before your function successfully located the target bot.

# These import steps give you access to libraries which you may (or may
# not) want to use.
from robot.robot import *  # Check the robot.py tab to see how this works.
from math import *
from matrix import * # Check the matrix.py tab to see how this works.
import random

# This is the function you have to write. Note that measurement is a
# single (x, y) point. This function will have to be called multiple
# times before you have enough information to accurately predict the
# next position. The OTHER variable that your function returns will be
# passed back to your function the next time it is called. You can use
# this to keep track of important information over time.
test = []
from Tkinter import *


def estimate_next_pos(measurement, OTHER = None):
    """
    I started with a Gaussian distribution over a region around the third measurement of the target with a Gaussian
        distribution on speed, bearing, and steering angle based on those three measurements.
    Then, every step, I evolved the particles according to their bearing and steering
    resampled the particles using the wheel resampling method based on their likelihood given
        the robot's position measurements.
    I also threw out ~10% of the particles at every step and regenerated them based on the last three measurements like
        at the beginning of the procedure (this is what I mentioned in talking about the project in one of
        the office hours...either 2nd or 3rd, can't remember right now). This was to try to make sure I didn't
        get stuck with a particle that beat all the other particles but still wasn't very close to the robot's
        actual position.
    After some fiddling (not twiddling, though :P) with parameters, it ended up working reasonably well for localizing
        the robot. It works up to a measurement noise factor of about 0.2 (in Parts 2-4, the noise factor is just 0.05).
        Didn't work so well for Part 5, though!
    """
    xy_estimate = 0, 0
    if OTHER is None:
        OTHER = []
        OTHER.append(measurement)
    elif len(OTHER) < 3:
        OTHER.append(measurement)
    elif len(OTHER) >= 3:
        OTHER.append(measurement)
        turning = 0
        distance = 0
        for i in range(len(OTHER)-2):
            p0 = OTHER[i]
            p1 = OTHER[i + 1]
            p2 = OTHER[i + 2]

            vx1 = p1[0] - p0[0]
            vy1 = p1[1] - p0[1]
            mag_v1 = distance_between(p0, p1)

            vx2 = p2[0] - p1[0]
            vy2 = p2[1] - p1[1]
            mag_v2 = distance_between(p1, p2)

            turning += acos((vx1 * vx2 + vy1 * vy2)/(mag_v1 * mag_v2))
        turning = turning/(len(OTHER) - 2)
        print 'turning--->', turning * 34 / 2 / pi

        for i in range(len(OTHER)-1):
            p0 = OTHER[i]
            p1 = OTHER[i + 1]
            distance += distance_between(p0, p1)
        distance = distance/(len(OTHER[0]) - 1)
        print 'distance--->', distance

        p2 = OTHER[-1]
        p1 = OTHER[-2]
        heading = atan2((p2[1] - p1[1]), (p2[0] - p1[0]))

        r = robot(measurement[0], measurement[1], heading, 2*pi / 34.0, 1.5)
        print 'robot--->', r
        r.set_noise(0.01, 0.01, 0)
        r.move_in_circle()
        xy_estimate = r.x, r.y

    return xy_estimate, OTHER

# A helper function you may find useful.
def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# This is here to give you a sense for how we will be running and grading
# your code. Note that the OTHER variable allows you to store any
# information that you want.
# def demo_grading(estimate_next_pos_fcn, target_bot, OTHER = None):
#     localized = False
#     distance_tolerance = 0.01 * target_bot.distance
#     ctr = 0
#     # if you haven't localized the target bot, make a guess about the next
#     # position, then we move the bot and compare your guess to the true
#     # next position. When you are close enough, we stop checking.
#     while not localized and ctr <= 1000:
#         print 'ctr--->', ctr
#         ctr += 1
#         measurement = target_bot.sense()
#         position_guess, OTHER = estimate_next_pos_fcn(measurement, OTHER)
#         target_bot.move_in_circle()
#         true_position = (target_bot.x, target_bot.y)
#         print 'true position--->', true_position
#         error = distance_between(position_guess, true_position)
#         print 'error--->', error
#         if error <= distance_tolerance:
#             print "You got it right! It took you ", ctr, " steps to localize."
#             localized = True
#         if ctr == 1000:
#             print 'X' * 100
#             print "Sorry, it took you too many steps to localize the target."
#     return localized

def demo_grading(estimate_next_pos_fcn, target_bot, OTHER = None):
    localized = False
    distance_tolerance = 0.01 * target_bot.distance
    ctr = 0
    # if you haven't localized the target bot, make a guess about the next
    # position, then we move the bot and compare your guess to the true
    # next position. When you are close enough, we stop checking.
    #For Visualization
    import turtle    #You need to run this locally to use the turtle module
    window = turtle.Screen()
    window.bgcolor('white')
    size_multiplier= 25.0  #change Size of animation
    broken_robot = turtle.Turtle()
    broken_robot.shape('turtle')
    broken_robot.color('green')
    broken_robot.resizemode('user')
    broken_robot.shapesize(0.5, 0.5, 0.5)
    measured_broken_robot = turtle.Turtle()
    measured_broken_robot.shape('circle')
    measured_broken_robot.color('red')
    measured_broken_robot.resizemode('user')
    measured_broken_robot.shapesize(0.1, 0.1, 0.1)
    prediction = turtle.Turtle()
    prediction.shape('arrow')
    prediction.color('blue')
    prediction.resizemode('user')
    prediction.shapesize(1, 1, 1)
    prediction.penup()
    broken_robot.penup()
    measured_broken_robot.penup()
    #End of Visualization
    while not localized and ctr <= 1000:
        ctr += 1
        measurement = target_bot.sense()
        position_guess, OTHER = estimate_next_pos_fcn(measurement, OTHER)
        target_bot.move_in_circle()
        true_position = (target_bot.x, target_bot.y)
        error = distance_between(position_guess, true_position)
        print 'error--->', error
        if error <= distance_tolerance:
            print "You got it right! It took you ", ctr, " steps to localize."
            localized = True
        if ctr == 1000:
            print "Sorry, it took you too many steps to localize the target."
        #More Visualization
        measured_broken_robot.setheading(target_bot.heading*180/pi)
        measured_broken_robot.goto(measurement[0]*size_multiplier, measurement[1]*size_multiplier-200)
        measured_broken_robot.stamp()
        broken_robot.setheading(target_bot.heading*180/pi)
        broken_robot.goto(target_bot.x*size_multiplier, target_bot.y*size_multiplier-200)
        broken_robot.stamp()
        prediction.setheading(target_bot.heading*180/pi)
        prediction.goto(position_guess[0]*size_multiplier, position_guess[1]*size_multiplier-200)
        prediction.stamp()
        #End of Visualization
    return localized

# This is a demo for what a strategy could look like. This one isn't very good.
def naive_next_pos(measurement, OTHER = None):
    """This strategy records the first reported position of the target and
    assumes that eventually the target bot will eventually return to that
    position, so it always guesses that the first position will be the next."""
    if not OTHER: # this is the first measurement
        OTHER = measurement
    xy_estimate = OTHER
    return xy_estimate, OTHER

# This is how we create a target bot. Check the robot.py file to understand
# How the robot class behaves.


test_target = robot(2.1, 4.3, 0.5, 2*pi / 34.0, 1.5)
measurement_noise = 0.05 * test_target.distance
test_target.set_noise(0.0, 0.0, measurement_noise)

demo_grading(estimate_next_pos, test_target)















































########################################################################################################################
# this was kinda working
#     num_particles = 5000
#     heading = 0
#     turning = 0
#     distance = 0
#     xy_estimate = 0, 0
#
#     landmarks = [(random.randint(1, 100), random.randint(1, 100)),
#                  (random.randint(1, 100), random.randint(1, 100)),
#                  (random.randint(1, 100), random.randint(1, 100)),
#                  (random.randint(1, 100), random.randint(1, 100)), ]
#
#     if OTHER is None:
#         OTHER = []
#         OTHER.append([measurement])
#         OTHER.append([])
#     elif len(OTHER[0]) < 3:
#         OTHER[0].append(measurement)
#     elif len(OTHER[0]) == 3:
#         p0 = OTHER[0][0]
#         p1 = OTHER[0][1]
#         p2 = OTHER[0][2]
#
#         vx1 = p1[0] - p0[0]
#         vy1 = p1[1] - p0[1]
#         mag_v1 = distance_between(p0, p1)
#
#         vx2 = p2[0] - p1[0]
#         vy2 = p2[1] - p1[1]
#         mag_v2 = distance_between(p1, p2)
#
#         heading = atan2((p2[1] - p1[1]), (p2[0] - p1[0]))
#         turning = acos((vx1 * vx2 + vy1 * vy2)/(mag_v1 * mag_v2))
#         distance = mag_v1
#
#         OTHER[0].append(measurement)
#         # step 1: create particles, store them in OTHER
#         for i in range(num_particles):
#             x = random.gauss(measurement[0], .01)
#             y = random.gauss(measurement[1], .01)
#             p_heading = random.gauss(heading, 2 * pi / 3600)
#             p_turning = random.gauss(turning, 2 * pi / 3600)
#             p_distance = random.gauss(distance, .005)
#             p = robot(x, y, p_heading, p_turning, p_distance)
#             p.move_in_circle()
#             OTHER[1].append(p)
#     elif len(OTHER[0]) > 3:
#         OTHER[0].append(measurement)
#         turning = 0
#         distance = 0
#
#         for i in range(len(OTHER[0])-2):
#             p0 = OTHER[0][i]
#             p1 = OTHER[0][i + 1]
#             p2 = OTHER[0][i + 2]
#
#             vx1 = p1[0] - p0[0]
#             vy1 = p1[1] - p0[1]
#             mag_v1 = distance_between(p0, p1)
#
#             vx2 = p2[0] - p1[0]
#             vy2 = p2[1] - p1[1]
#             mag_v2 = distance_between(p1, p2)
#
#             turning += acos((vx1 * vx2 + vy1 * vy2)/(mag_v1 * mag_v2))
#         turning = turning/(len(OTHER[0]) - 2)
#         print 'turning--->', turning * 34 / 2 / pi
#
#         for i in range(len(OTHER[0])-1):
#             p0 = OTHER[0][i]
#             p1 = OTHER[0][i + 1]
#
#             distance += distance_between(p0, p1)
#         distance = distance/(len(OTHER[0]) - 1)
#         print 'distance--->', distance
#
#         p2 = OTHER[0][-1]
#         p1 = OTHER[0][-2]
#         heading = atan2((p2[1] - p1[1]), (p2[0] - p1[0]))
#         # print 'heading--->', heading
#
#         # sample particles
#
#         # Update particles
#         def measurement_prob(particle):
#             # d = distance_between((particle.x, particle.y), measurement)
#             # mu = 0
#             # sigma = .1
#
#             d1 = abs(particle.heading - heading)
#             mu1 = 0
#             sigma1 = .1
#
#             d2 = abs(particle.turning - turning)
#             mu2 = 0
#             sigma2 = .1
#
#             d3 = abs(particle.distance - distance)
#             mu3 = 0
#             sigma3 = .1
#
#             return g(d1, mu1, sigma1) * g(d2, mu2, sigma2) * g(d3, mu3, sigma3)
#
#         def g(x, mu, sigma):
#             return 1/(sigma*sqrt(2*pi))*exp(-0.5*(x-mu)**2/sigma**2)
#
#         for p in OTHER[1]:
#             p.x = measurement[0]
#             p.y = measurement[1]
#
#         # measurement update
#         w = []
#         for i in range(num_particles):
#             w.append(measurement_prob(OTHER[1][i]))
#
#         # resampling
#         p3 = []
#         index = int(random.random() * num_particles)
#         beta = 0.0
#         mw = max(w)
#         for i in range(num_particles):
#             beta += random.random() * 2.0 * mw
#             while beta > w[index]:
#                 beta -= w[index]
#                 index = (index + 1) % num_particles
#             p3.append(OTHER[1][index])
#         OTHER[1] = p3
#         for p in OTHER[1]:
#             p.move_in_circle()
#         x = 0
#         y = 0
#         for p in OTHER[1]:
#             x += p.x
#             y += p.y
#         avg_x = x/len(OTHER[1])
#         avg_y = y/len(OTHER[1])
#         print 'prediction--->', avg_x, avg_y
#         xy_estimate = avg_x, avg_y