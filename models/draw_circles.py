# -*- coding: UTF-8 -*-

from math import *
from model6 import *

m = Model6(
    n  = 100,
    a  = 0.1,
    f  = 8,
    g1 = 14,
    g2 = 7)
m.run(step = 0.1, plot = False)

n = m.field_size

zoom = 5
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



from mayavi import mlab

h = 700
t = 90
dphi = 2*pi / t
phi = numpy.linspace(0, 2*pi, t + 1)

x, y, z = [], [], []
for center in fibers_centens:
    xc, yc = center
    x.append(numpy.array((xc + numpy.zeros(t + 1),
                          xc + r * numpy.cos(phi),
                          xc + r * numpy.cos(phi),
                          xc + numpy.zeros(t + 1))))

    y.append(numpy.array((yc + numpy.zeros(t + 1),
                          yc + r * numpy.sin(phi),
                          yc + r * numpy.sin(phi),
                          yc + numpy.zeros(t + 1))))

    z.append(numpy.array((numpy.zeros(t + 1),
                          numpy.zeros(t + 1),
                          numpy.ones(t + 1) * h,
                          numpy.ones(t + 1) * h)))


x = numpy.vstack(x)
y = numpy.vstack(y)
z = numpy.vstack(z)


mlab.mesh(x, y, z, colormap = 'winter')
mlab.show()

