import sys
sys.path.append("..")
from mca.mca import *
from visualization.circles import *

import pickle

f = open("mca.pickle", 'rb')
m = pickle.load(f)
f.close()

m.plot()


draw_circles(m)
shift_and_draw_circles(m,6)