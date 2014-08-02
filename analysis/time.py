import sys
sys.path.append("..")
from models.model6 import *
from time import time, clock


def run_many_times(loops):
    print "clock() =", clock(), ", time() =", time()
    clock_list = [[] for i in range(loops)]
    time_list  = [[] for i in range(loops)]
    for i in range(loops):
        for a in [j * 0.1 for j in range(0, 11)]:
            print
            print "~~~~~~~~~~~~~~ Loop No.", i+1, ", a =", a, "~~~~~~~~~~~~~~"
            print
            c = clock()
            t = time()
            Model6(
                n  = 250,
                a  = a,
                f  = 8,
                g1 = 15,
                g2 = 7
            ).run(step = 6250, plot = False)
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
    run_many_times(20)
