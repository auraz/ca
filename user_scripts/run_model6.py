import sys
sys.path.append("..")
from models.model6 import *

m = Model6(
    n  = 300,
    a  = 1.0,
    f  = 8,
    g1 = 14,
    g2 = 7
)
m.spawn_nuclei(plot = True)
m.grow_fibers(plot = True)
