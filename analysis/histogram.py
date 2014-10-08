import sys
sys.path.append("..")
from mca.mca import *


def run_many_times(loops):
    for i in range(loops):
        print i + 1,
        m = MCA(
                n  = 100,
                a  = 1.0,
                f  = 4,
                g1 = 7,
                g2 = 3)
        m.spawn_nuclei(
                step = 1.0)



if __name__ == '__main__':
    run_many_times(3238)
