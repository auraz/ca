import sys
sys.path.append("..")
from mca.mca import *

class MCA_adjusted(MCA):
    """MCA, adjusted for an investigation"""
    
    def spawn_nuclei(self, stops):
        random_list = range(self.field_size**2)
        random.shuffle(random_list)
        results = []

        for i in range(self.attempts):
            x = random_list[i] % self.field_size
            y = random_list[i] / self.field_size
            if self.field[y, x] == 0:
                nuc = Nucleus(x, y, self)
            if i+1 in stops:
                results.append(len(self.nuclei))
                print i+1, len(self.nuclei)

        return results





def run_once():
    print MCA_adjusted(
        n  = 100,
        a  = 10000,
        f  = 4,
        g1 = 7,
        g2 = 1
    ).spawn_nuclei(stops = [1,          2,    3,    5,    7,
                            10,   15,   20,   30,   50,   70,
                            100,  150,  200,  300,  500,  700,
                            1000, 1500, 2000, 3000, 5000, 7000,
                            10000])


def print_general_results(stops, general_results):
    print
    print "General results:"
    print
    for results in [stops] + general_results:
        for i in results:
            print str(i) + '\t',
        print '\n',


def run_many_times(loops):
    general_results = []
    stops = [1,          2,    3,    5,    7,
             10,   15,   20,   30,   50,   70,
             100,  150,  200,  300,  500,  700,
             1000, 1500, 2000, 3000, 5000, 7000,
             10000,15000,20000,21500,22000,22250,
             22400,22470,22490,22493,22499,22500]

    for i in range(loops):
        print
        print "~~~~~~~~~~~~~~ Launch No.", i+1, "~~~~~~~~~~~~~~"
        print

        general_results.append(MCA_adjusted(
            n  = 150,
            a  = 22500,
            f  = 4,
            g1 = 10,
            g2 = 1
        ).spawn_nuclei(stops))

        if (i + 1) % 10 == 0:
            print_general_results(stops, general_results)


if __name__ == '__main__':
    # run_once()
    run_many_times(20)
