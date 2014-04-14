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
        self.attempts = a
        self.g2 = g2


    def run(self, plot = False, plot_each_step = False):
        """Запуск модели."""

        self.spawn_nuclei()
        # self.spawn_nuclei_in_old_way(step = 1000)
        self.grow_nuclei(plot, plot_each_step)


    def spawn_nuclei(self):
        random_list = range(self.field_size**2)
        random.shuffle(random_list)

        print random_list[:self.attempts]
        for r in random_list[:self.attempts]:
            x = r % 100
            y = r / 100
            nuc = Nucleus(x, y, self)
            if nuc.is_anything_near():
                nuc.die()
            else:
                info("A random nucleus is spawned. x = %s, y = %s.", x, y)
                self.report()

        print len(self.nuclei), "nuclei,"


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

    
    def grow_nuclei(self, plot, plot_each_step):
        self.gap = self.g2

        for i in range((self.fiber_size - 1) * 2):

            # reporting:
            print "growing... {} nuclei and {} fibers.".format(
                len(self.nuclei), len(self.fibers))
            # self.report()
            if plot_each_step:
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

        # self.report()
        # print  "The field now looks like this:"
        # print self.field
        print "There are now {} nuclei and {} fibers.".format(
            len(self.nuclei), len(self.fibers))

        concentration = 100.0 * len(self.nuclei) * self.fiber_size**2 / self.field_size**2
        print "{} * {} / {} * 100% = {}%".format(
            len(self.nuclei), self.fiber_size**2, self.field_size**2, concentration)
        print "Fibers take {}%.".format(concentration)

        if plot:
            field_of_numbers = [[2 if isinstance(i, Nucleus) else i for i in j] for j in self.field]
            im = plt.imshow(field_of_numbers, cmap=cm.gray, interpolation='nearest')
            plt.show()

#     if len(self.nuclei) == 0:
        #         info("There are no more nuclei. Stopping the model.")
        #         info("%s iterations have been carried out.", counter)
        #         print counter, "iterations have been carried out."
        #         break

        # print "{} nuclei have grown to fibers.".format(len(self.fibers))
        




if __name__ == '__main__':
    Model6(
            n  = 100,
            a  = 200,
            f  = 9,
            g1 = 7,
            g2 = 7).run(plot = True)
    # general_results = []
    # for i in range(100):
    #     print
    #     print "Запуск №", i+1
    #     print
    #     general_results.append(Model6(
    #         field_size = 100,
    #         fiber_size =   4,
    #         gap        =   7).run())
    # general_results = Grid(general_results)
    # print
    # print "Results:"
    # print general_results