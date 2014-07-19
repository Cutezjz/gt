from numpy import *

def circular_regression():
    other = [[9, 34], [35, 10], [-13, 6], [10, -14], [23, 27], [0, -10]]
    xp = []
    yp = []
    for e in other:
        xp.append(e[0])
        yp.append(e[1])

    x = r_[xp]
    y = r_[yp]

    # coordinates of the barycenter
    x_m = mean(x)
    y_m = mean(y)

    #  == METHOD 2 ==
    # Basic usage of optimize.leastsq
    from scipy import optimize

    method_2 = "leastsq"

    def calc_R(xc, yc):
        """ calculate the distance of each 2D points from the center (xc, yc) """
        return sqrt((x-xc)**2 + (y-yc)**2)

    def f_2(c):
        """ calculate the algebraic distance between the 2D points and the mean circle centered at c=(xc, yc) """
        Ri = calc_R(*c)
        return Ri - Ri.mean()

    center_estimate = x_m, y_m
    center_2, ier = optimize.leastsq(f_2, center_estimate)

    xc_2, yc_2 = center_2
    Ri_2       = calc_R(xc_2, yc_2)
    R_2        = Ri_2.mean()

    print "leastsq                  10.50009    9.65995   23.33353"
    print center_2
    print R_2

circular_regression()