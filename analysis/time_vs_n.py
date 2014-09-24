import sys
sys.path.append("..")
from models.model6 import *
from time import time, clock


def run_many_times(loops):
    print "clock() =", clock(), ", time() =", time()
    clock_list = [[] for i in range(loops)]
    time_list  = [[] for i in range(loops)]
    for i in range(loops):
        for n in [50, 63, 80, 100, 125, 160, 200, 250, 320, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3200, 4000, 5000]:
            print
            print "~~~~~~~~~~~~~~ Loop No.", i+1, ", n =", n, "~~~~~~~~~~~~~~"
            print
            c = clock()
            t = time()
            Model6(
                n  = n,
                a  = 1.0,
                f  = 8,
                g1 = 15,
                g2 = 7
            ).run(step = 1.0 if n < 1000 else 0.1, plot = False)
            clock_list[i].append(clock() - c)
            time_list[i] .append(time () - t)
        
        print
        print "~~~~~~~~~~~~~~ General results: ~~~~~~~~~~~~~~"
        print "Clock:"
        for results in clock_list:
            for one_result in results:
                print str(one_result) + '\t',
            print '\n',
        print
        print "Time:"
        for results in time_list:
            for one_result in results:
                print str(one_result) + '\t',
            print '\n',



def run_once():
    Model6(
        n  = 500,
        a  = 0.03,
        f  = 8,
        g1 = 15,
        g2 = 7
    ).run(step = 0.1, plot = True)


if __name__ == '__main__':
    # run_once()
    run_many_times(1)
