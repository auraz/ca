import sys
sys.path.append("..")
from mca.mca import *

m = MCA(
    n  = 10,
    a  = 1.0,
    f  = 3,
    g1 = 2,
    g2 = 1
)
m.spawn_nuclei(plot = True)
m.grow_fibers(plot = True)




import pickle

f = open("mca.pickle", 'wb')
pickle.dump(m, f)
f.close()


# from visualization.circles import *

# draw_circles(m)
# shift_and_draw_circles(m)