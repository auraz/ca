import sys
sys.path.append("..")
from mca.mca import *

m = MCA(
    n  = 300,
    a  = 1.0,
    f  = 8,
    g1 = 14,
    g2 = 7
)
m.spawn_nuclei(plot = True)
m.grow_fibers(plot = True)




import pickle

f = open("mca.pickle", 'wb')
pickle.dump(m, f)
f.close()
