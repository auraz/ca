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



def run_once():
    n = 1000
    m = Model6(
        n  = n,
        a  = 0.02,
        f  = 5,
        g1 = 7,
        g2 = 3
    )
    m.run(step = 0.01, plot = True)

    for d in range(n / 2):
        print "{}\t{}\t{}".format(
            d, non_blank_cells(m.field, d), non_blank_concentration(m.field, d))



def run_many_times():
    general_results = []
    n = 200
    for i in range(50):
        print
        print "~~~~~~~~~~~~~~ Launch No.", i+1, "~~~~~~~~~~~~~~"
        print

        results = []
        m = Model6(
            n  = n,
            a  = 1.0,
            f  = 4,
            g1 = 7,
            g2 = 3
        )
        m.run(step = 0.1, plot = False)

        for d in range(n / 2):
            results.append(non_blank_concentration(m.field, d))

        general_results.append(results)

    print
    print "General results:"
    print
    for results in general_results:
        for i in results:
            print str(i) + '\t',
        print '\n',




if __name__ == '__main__':
    run_many_times()
