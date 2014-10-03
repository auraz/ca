# -*- coding: UTF-8 -*-

import sys
sys.path.append("..")
from math import *
from mca.mca import *

def draw_circles(m, zoom = 5):

    n = m.field_size
    canvas = numpy.zeros((n * zoom, ) * 2, dtype = numpy.int64)

    fibers_centens = []
    for nuc in m.nuclei:
        xc = nuc.x - nuc.left * 0.5 + nuc.right * 0.5
        yc = nuc.y - nuc.up   * 0.5 + nuc.down  * 0.5
        new_xc = zoom * (xc + 0.5) - 0.5
        new_yc = zoom * (yc + 0.5) - 0.5
        fibers_centens.append((new_xc, new_yc))

    r = m.fiber_size / pi**0.5 * zoom

    ci_dots = 0
    for center in fibers_centens:
        xc, yc = center
        left_side   = int(max( ceil(xc - r), 0           ))
        right_side  = int(min(floor(xc + r), n * zoom - 1))
        top_side    = int(max( ceil(yc - r), 0           ))
        bottom_side = int(min(floor(yc + r), n * zoom - 1))

        for y in range(top_side, bottom_side + 1):
            for x in range(left_side, right_side + 1):
                if (x - xc)**2 + (y - yc)**2 <= r**2:
                    canvas[y, x] = 1
                    ci_dots += 1

    sq_dots = m.fiber_size**2 * len(m.nuclei) * zoom**2
    print "Circles take", ci_dots * 100. / n**2 / zoom**2, "%."
    print "Squares:", sq_dots, "dots."
    print "Circles:", ci_dots, "dots."
    print "Difference:", 100. * (ci_dots - sq_dots) / sq_dots, "%."

    im2 = plt.imshow(canvas, cmap=cm.gray, interpolation='nearest')
    plt.show()



def shift_and_draw_circles(m, zoom = 5):

    n = m.field_size
    canvas = numpy.zeros((n * zoom, ) * 2, dtype = numpy.int64)
    r = m.fiber_size / pi**0.5

    fibers_centens = []
    for nuc in m.nuclei:
        xc = nuc.x - nuc.left * 0.5 + nuc.right * 0.5
        yc = nuc.y - nuc.up   * 0.5 + nuc.down  * 0.5

        xc = xc if xc - r > 0.5     else r-0.5
        xc = xc if xc + r < n - 0.5 else n - 0.5 - r
        yc = yc if yc - r > 0.5     else r-0.5
        yc = yc if yc + r < n - 0.5 else n - 0.5 - r
        # if xc + r > n:
        #     print "xc + r > n! xc =", xc, ", r =", r, ", n =", n, ". New value of xc =", n - r
        #     xc = n - r

        xc = zoom * (xc + 0.5) - 0.5
        yc = zoom * (yc + 0.5) - 0.5
        fibers_centens.append((xc, yc))

    r *= zoom
    
    ci_dots = 0
    for center in fibers_centens:
        xc, yc = center
        left_side   = int(floor(xc - r))
        right_side  = int(ceil(xc + r))
        top_side    = int(floor(yc - r))
        bottom_side = int(ceil(yc + r))
        # if xc > 470:
        #     print xc, yc, left_side, right_side, top_side, bottom_side, r
        #     for y in range(top_side, bottom_side + 1):
        #         for x in range(left_side, right_side + 1):
        #             if (x - xc)**2 + (y - yc)**2 <= r**2:
        #                 canvas[y, x] = 1
        #                 ci_dots += 1
        #                 print '*',
        #             else:
        #                 print ' ',
        #         print
        # else:
        for y in range(top_side, bottom_side + 1):
            for x in range(left_side, right_side + 1):
                if (x - xc)**2 + (y - yc)**2 <= r**2:
                    canvas[y, x] = 1
                    ci_dots += 1

    sq_dots = m.fiber_size**2 * len(m.nuclei) * zoom**2
    print "Circles take", ci_dots * 100. / n**2 / zoom**2, "%."
    print "Squares:", sq_dots, "dots."
    print "Circles:", ci_dots, "dots."
    print "Difference:", 100. * (ci_dots - sq_dots) / sq_dots, "%."

    im2 = plt.imshow(canvas, cmap=cm.gray, interpolation='nearest')
    plt.show()

