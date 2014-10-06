import sys
sys.path.append("..")
from mca.mca import *
# from visualization.circles import *

from math import pi
import pickle

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

mpl.rcParams['figure.figsize' ] = 6, 6    # figure size in inches
mpl.rcParams[ 'axes.facecolor'] = 'black'
mpl.rcParams['patch.facecolor'] = 'white'

def fibers_centers(mca):
    centers = []
    for nuc in mca.nuclei:
        # explain why you add 0.5!
        xc = 0.5 + nuc.x - nuc.left * 0.5 + nuc.right * 0.5
        yc = 0.5 + nuc.y - nuc.up   * 0.5 + nuc.down  * 0.5
        # print xc, yc
        centers.append((xc, yc))
    # print
    return centers


def shift_centers(centers, n, r):
    # n = mca.field_size
    new_centers = []
    for xc, yc in centers:
        xc = xc if xc - r > 0 else r
        xc = xc if xc + r < n else n - r
        yc = yc if yc - r > 0 else r
        yc = yc if yc + r < n else n - r
        # print xc, yc
        new_centers.append((xc, yc))
    return new_centers


def draw_circles(centers, n, r):
    fig, ax = plt.subplots()
    ax.set_xlim(0, n)
    ax.set_ylim(n, 0)
    ax.set_aspect('equal')
    for c in centers:
        circle = mpl.patches.Circle(c, r)
        ax.add_patch(circle)
    return fig


if __name__ == '__main__':
    f = open("mca.pickle", 'rb')
    mca = pickle.load(f)
    f.close()

    plt.imshow(mca.field, cmap=cm.gray, interpolation='nearest')

    n = mca.field_size
    r = mca.fiber_size / pi**0.5
    centers = fibers_centers(mca)
    shifted_centers = shift_centers(centers, n, r)
    draw_circles(centers, n, r)
    draw_circles(shifted_centers, n, r)
    plt.show()