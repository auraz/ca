﻿# -*- coding: UTF-8 -*-

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



class Model6(Model4):
    """Модель 6.

        Заполняем поле нулями.
        Далее, на каждой итерации:
        1.  Случайным образом засеваем новый зародыш, при этом в его мёртвой
            зоне не должно быть других зародышей и волокон.
            Происходит только одна попытка забросить зародыш. Если она была
            неудачной (в его мёртвой зоне что-то есть), сразу переходим к 2.
        2.  Выбираем случайный зародыш или волокно и делаем всё аналогично
            Модели 3: оно растёт, объявляется выросшим или умирает.
        Так происходит до тех пор, пока все засеянные зародыши не вырастут
        или умрут.
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

        nuclei_spawned = self.spawn_nuclei(step)
        # self.spawn_nuclei_in_old_way(step)
        nuclei_grown, concentration = self.grow_nuclei(plot)
        # return nuclei_spawned, nuclei_grown, concentration
        return concentration



    def spawn_nuclei(self, step):
        random_list = range(self.field_size**2)
        random.shuffle(random_list)

        for i in range(self.attempts / step):
            for r in random_list[i * step : (i + 1) * step]:
                x = r % self.field_size
                y = r / self.field_size
                nuc = Nucleus(x, y, self)
                if nuc.is_anything_near():
                    nuc.die()
                # else:
                #     info("A random nucleus is spawned. x = %s, y = %s.", x, y)
                #     self.report()
            # print i * step, "-", (i + 1) * step, ":",
            print (i + 1) * step, len(self.nuclei)
        
        return len(self.nuclei)



    def spawn_nuclei_in_old_way(self, step):
        # Needs Model4! Don't use if the base class isn't Model4.

        results = [0]
        attempts = 0
        print "0000 0"
        while attempts < self.attempts:
            for i in range(step):
                attempts += 1
                self.spawn_a_nucleus()  # method of Model4
            print attempts, len(self.nuclei)
            results.append(len(self.nuclei))

        print len(self.nuclei), "nuclei,",  attempts, "attempts.  ",
        print results
        return results

    
    def grow_nuclei(self, plot):
        # print "Growing:"
        self.gap = self.g2

        for i in range((self.fiber_size - 1) * 2):

            if plot == "each step":
                field_of_numbers = [[2 if isinstance(i, Nucleus) else i for i in j] for j in self.field]
                im = plt.imshow(field_of_numbers, cmap=cm.gray, interpolation='nearest')
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
            field_of_numbers = [[2 if isinstance(i, Nucleus) else i for i in j] for j in self.field]
            im = plt.imshow(field_of_numbers, cmap=cm.gray, interpolation='nearest')
            plt.show()

        return len(self.nuclei), concentration

#     if len(self.nuclei) == 0:
        #         info("There are no more nuclei. Stopping the model.")
        #         info("%s iterations have been carried out.", counter)
        #         print counter, "iterations have been carried out."
        #         break

        # print "{} nuclei have grown to fibers.".format(len(self.fibers))
        




if __name__ == '__main__':
    # Model6(
    #     n  = 100,
    #     a  = 0.5,
    #     f  = 4,
    #     g1 = 7,
    #     g2 = 3
    # ).run(step = 0.2, plot = True)

    general_results = []
    range_i, range_f = 30, 20
    for i in range(range_i):
        print
        print "~~~~~~~~~~~~~~ Loop No.", i, "~~~~~~~~~~~~~~"
        results = []
        for f in range(range_f):
            print
            print "f =", f, '                        loop no.', i
            print
            results.append(
                Model6(
                    n  = 100,
                    a  = 1.0,
                    f  = f,
                    g1 = 7,
                    g2 = 1
                ).run(step = 0.2, plot = False))
        general_results.append(results)

    print
    print "General results:"
    print
    for i in general_results:
        print i
    print

