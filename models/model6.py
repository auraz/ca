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



class Model6(MCA):
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

    def run(self):
        """Запуск модели."""

        k  = 10.0
        g1 = 7
        g2 = 1
        f  = 4
        step = 1000
        plot = False
        results = [0]

        self.fiber_size = f
        self.gap        = g1

        n = self.field_size
        max_attempts = self.field_size**2
        random_list = range(max_attempts)
        random.shuffle(random_list)
        debug(random_list)

        for r in random_list:
            x = r % 100
            y = r / 100
            debug(r)
            debug(x)
            debug(y)
            nuc = Nucleus(x, y, self)
            if nuc.is_anything_near():
                nuc.die()
            else:
                info("A random nucleus is spawned. x = %s, y = %s.", x, y)
                self.report()

        print len(self.nuclei), "nuclei,"

        # attempts = 0
        # print "0000 0"
        # while attempts < k*self.field_size**2:
        #     for i in range(step):
        #         attempts += 1
        #         self.spawn_a_nucleus()
        #     print attempts, len(self.nuclei)
        #     results.append(len(self.nuclei))

        # print len(self.nuclei), "nuclei,",  attempts, "attempts.  ",
        # print results
        # return results

        self.gap = g2

        # while len(self.nuclei) > 0:
        for i in range((self.fiber_size - 1) * 2):

            # reporting:
            print "growing... {} nuclei and {} fibers.".format(
                len(self.nuclei), len(self.fibers))
            # self.report()
            # field_of_numbers = [[2 if isinstance(i, Nucleus) else i for i in j] for j in self.field]
            # im = plt.imshow(field_of_numbers, cmap=cm.gray, interpolation='nearest')
            # plt.show()

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

        print "100.0 * {} * {} / {}".format(
            len(self.nuclei), self.fiber_size**2, self.field_size**2)
        print "Fibers take {}%.".format(
            100.0 * len(self.nuclei) * self.fiber_size**2 / self.field_size**2)

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
            field_size = 100,
            fiber_size =   4,
            gap        =   7).run()
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