import sys
sys.path.append("..")
from mca.mca import *

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
    n = 600
    m = MCA(
        n  = n,
        a  = 0.04,
        f  = 17,
        g1 = 30,
        g2 = 15
    )
    m.run(step = 0.1, plot = True)

    for d in range(n / 2):
        print "{}\t{}\t{}".format(
            d, non_blank_cells(m.field, d), non_blank_concentration(m.field, d))



def run_many_times(loops):
    general_results = []
    n = 600
    for i in range(loops):
        print
        print "~~~~~~~~~~~~~~ Launch No.", i+1, "~~~~~~~~~~~~~~"
        print

        results = []
        m = MCA(
            n  = n,
            a  = 0.04,
            f  = 17,
            g1 = 30,
            g2 = 15
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
    # run_once()
    run_many_times(10)
