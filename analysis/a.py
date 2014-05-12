import sys
sys.path.append("..")
from models.model6 import *

class Model6_adjusted(Model6):
    """Model 6, adjusted for an investigation"""
    # def __init__(self, arg):
    #   super(Model6_adjusted, self).__init__()
    #   self.arg = arg
    
    def spawn_nuclei(self, stops):
        random_list = range(self.field_size**2)
        random.shuffle(random_list)
        results = []

        for i in range(self.attempts):
            x = random_list[i] % self.field_size
            y = random_list[i] / self.field_size
            nuc = Nucleus(x, y, self)
            if nuc.is_anything_near():
                nuc.die()
            if i+1 in stops:
                results.append(len(self.nuclei))
                print i+1, len(self.nuclei)

        return results


def run_once():
    print Model6_adjusted(
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




def run_many_times():
    general_results = []
    for i in range(100):
        print
        print "~~~~~~~~~~~~~~ Launch No.", i+1, "~~~~~~~~~~~~~~"
        print

        general_results.append(Model6_adjusted(
            n  = 100,
            a  = 10000,
            f  = 4,
            g1 = 7,
            g2 = 1
        ).spawn_nuclei(stops = [10,   15,   20,   30,   50,   70,
                                100,  150,  200,  300,  500,  700,
                                1000, 1500, 2000, 3000, 5000, 7000,
                                10000]))

    print
    print "General results:"
    print
    for results in general_results:
        for i in results:
            print str(i) + '\t',
        print '\n',




if __name__ == '__main__':
    # run_once()
    run_many_times()
