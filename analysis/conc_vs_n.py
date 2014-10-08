import sys
sys.path.append("..")
from mca.mca import *


def run_many_times(loops):
    general_results  = [[] for i in range(loops)]
    for i in range(loops):
        for n in [50, 70, 100, 150, 200, 300, 500, 700, 1000]:
            print
            print "~~~~~~~~~~~~~~ Loop No.", i+1, ", n =", n, "~~~~~~~~~~~~~~"
            print
            m = MCA(
                    n  = n,
                    a  = 0.2,
                    f  = 8,
                    g1 = 14,
                    g2 = 7)
            m.run(
                    step = 1.0 if n < 500 else 0.1,
                    plot = False)
            general_results[i].append(m.concentration)
        
        print
        print "~~~~~~~~~~~~~~ General results: ~~~~~~~~~~~~~~"
        print
        for results in general_results:
            for one_result in results:
                print str(one_result) + '\t',
            # print '\n',
            print
        print



if __name__ == '__main__':
    run_many_times(10)
