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


# n = 10
# m = Model6(
#     n  = n,
#     a  = 1.0,
#     f  = 3,
#     g1 = 2,
#     g2 = 1
# )
# m.run(step = 0.1, plot = False)
# print m.field

# print non_blank_cells(m.field, 2)

# non_blank_cells = 0
# for i in range(n - 1):
#     non_blank_cells += (m.field[0][i] != 0) \
#                     +  (m.field[i][n - 1] != 0) \
#                     +  (m.field[n - 1][n - 1 - i] != 0) \
#                     +  (m.field[n - 1 - i][0] != 0)
# j=1
# for i in range(n - 1 - j * 2):
#     print m.field[j][i + j],
#     print m.field[i][n - 1],
#     print m.field[n - 1][n - 1 - i],
#     print m.field[n - 1 - i][0]

# print non_blank_cells
