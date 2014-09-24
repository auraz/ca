# -*- coding: UTF-8 -*-

import numpy as np
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

import random

import logging
from logging import debug, info
logging.basicConfig(
    level    = logging.WARNING,
    filename = 'model.log',
    filemode = 'w',
    format   = '%(message)s')


import sys
sys.path.append("..")

from mca.mca import *
from models.model4 import Model4



class Model6(MCA):
    """Модель 6.
        """

    def __init__(self, n, a, f, g1, g2):
        MCA.__init__(self, n, f, g1)
        self.g2 = g2

        if isinstance(a, int):
            self.attempts = a
        elif isinstance(a, float):
            self.attempts = int(a * n**2)
        else:
            raise TypeError("'a' must be an int or a float.")



    def run(self, step, plot = False):
        """Запуск модели."""

        if isinstance(step, int):
            pass
        elif isinstance(step, float):
            step = int(step * self.attempts)
        else:
            raise TypeError("'step' must be an int or a float.")

        # nuclei_spawned = self.spawn_nuclei(step)
        # nuclei_grown, concentration = self.grow_nuclei(plot)
        # return concentration

        self.spawn_nuclei(step)
        self.grow_nuclei(plot)



    def spawn_nuclei(self, step):
        # Make a list of random numbers without repetitions:
        random_list = range(self.field_size**2)
        random.shuffle(random_list)

        for i in range(self.attempts / step):
            for r in random_list[i * step : (i + 1) * step]:
                x = r % self.field_size
                y = r / self.field_size
                if self.field[y, x] == 0:
                    nuc = Nucleus(x, y, self)
                # if nuc.is_anything_near():
                #     nuc.die()
                # else:
                #     info("A random nucleus is spawned. x = %s, y = %s.", x, y)
                #     self.report()
            # print i * step, "-", (i + 1) * step, ":",
            print (i + 1) * step, len(self.nuclei)
        
        # return len(self.nuclei)

        self.plot()

        self.field *= 0 # numpy.zeros((field_size, field_size), dtype = numpy.int64)
        for nuc in self.nuclei:
            self.field[nuc.y, nuc.x] = 2
        # self.plot()


    # def spawn_nuclei_in_old_way(self, step):
    #     # Needs Model4! Don't use if the base class isn't Model4.

    #     results = [0]
    #     attempts = 0
    #     print "0000 0"
    #     while attempts < self.attempts:
    #         for i in range(step):
    #             attempts += 1
    #             self.spawn_a_nucleus()  # method of Model4
    #         print attempts, len(self.nuclei)
    #         results.append(len(self.nuclei))

    #     print len(self.nuclei), "nuclei,",  attempts, "attempts.  ",
    #     print results
    #     return results

    
    def grow_nuclei(self, plot):
        # print "Growing:"
        self.gap = self.g2

        for i in range((self.fiber_size - 1) * 2):

            if plot == "each step":
                # field_of_numbers = [[2 if isinstance(i, Nucleus) else i for i in j] for j in self.field]
                im = plt.imshow(self.field, cmap=cm.gray, interpolation='nearest')
                plt.show()

            # growing:
            for nuc in self.nuclei:
                nuc.look_around()
                nuc.try_to_grow(die_safely = True)
            # killing nuclei safely:
            for nuc in self.condemned:
                nuc.die()
            self.condemned = []

            # reporting:
            print i + 1, len(self.nuclei)
            # self.report()

        # self.report()
        # print  "The field now looks like this:"
        # print self.field
        # print "There are now {} nuclei and {} fibers.".format(
        #     len(self.nuclei), len(self.fibers))

        concentration = 100.0 * len(self.nuclei) * self.fiber_size**2 / self.field_size**2
        print "{} * {} / {} * 100% = {}%".format(
            len(self.nuclei), self.fiber_size**2, self.field_size**2, concentration)
        print "Fibers take {}%.".format(concentration)

        if plot or (plot == "each step"):
            field_to_plot = [[1 if i == 2 else i * 1
                for i in j] for j in self.field]
            im = plt.imshow(field_to_plot, cmap=cm.gray, interpolation='nearest')
            plt.show()

            # field_of_numbers = [[0.5 if isinstance(i, Nucleus) else -i for i in j]
            #     for j in self.field.get_subgrid(200, 200, 500, 500)]
            # im = plt.imshow(field_of_numbers, cmap=cm.gray, interpolation='nearest')
            # plt.show()

        # return len(self.nuclei), concentration
        self.concentration = concentration

#     if len(self.nuclei) == 0:
        #         info("There are no more nuclei. Stopping the model.")
        #         info("%s iterations have been carried out.", counter)
        #         print counter, "iterations have been carried out."
        #         break

        # print "{} nuclei have grown to fibers.".format(len(self.fibers))
        

    def plot(self):
        im = plt.imshow(self.field, cmap=cm.gray, interpolation='nearest')
        plt.show()




def run_many_times():
    # general_results = []
    # try:
    for i in range(1):
        print
        print "~~~~~~~~~~~~~~ Loop No.", i+1, "~~~~~~~~~~~~~~"
        print
        Model6(
            n  = 400,
            a  = 0,
            f  = 8,
            g1 = 15,
            g2 = 7
        ).run(step = 1, plot = False)
        # results = []
        # for n in [700, 1000]:
        #     print
        #     print "n =", n, '                        loop no.', i+1
        #     print
            # results.append(
        # general_results.append(results)

        
    # except KeyboardInterrupt:
    #     print "\nKeyboard interrupt."
    # finally:
    #     print
    #     print "General results:"
    #     print
    #     for i in general_results:
    #         print i
    #     print



def run_once():
    Model6(
        n  = 100,
        a  = 1.0,
        f  = 4,
        g1 = 7,
        g2 = 3
    ).run(step = 0.1, plot = False)


if __name__ == '__main__':
    run_once()
    # run_many_times()