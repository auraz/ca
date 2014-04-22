import sys
sys.path.append("..")
from models.model6 import *

def non_blank_cells(g, d):
    """g is grid, d is distance from the border."""
    n = len(g)
    count = 0
    for i in range(n - 1 - d * 2):
        #                 y               x
        count += (g[d]             [i + d]         != 0) \
              +  (g[i + d]         [n - 1 - d]     != 0) \
              +  (g[n - 1 - d]     [n - 1 - d - i] != 0) \
              +  (g[n - 1 - i - d] [d]             != 0)

    return count


def non_blank_concentration(g, d):
    n = len(g)
    return non_blank_cells(g, d) / 4.0 / (n - 1 - d * 2) * 100



if __name__ == '__main__':
    n = 10
    m = Model6(
        n  = n,
        a  = 1.0,
        f  = 3,
        g1 = 2,
        g2 = 1
    )
    m.run(step = 0.1, plot = False)
    print m.field

# print non_blank_cells(m.field, 2)

