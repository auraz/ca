# -*- coding: UTF-8 -*-

import numpy as np
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


import logging
from logging import debug, info
logging.basicConfig(
    level    = logging.INFO,
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

    def run(self):
        """Запуск модели."""

        attempts = 0
        while attempts < 20000:
            print attempts, len(self.nuclei)
            for i in range(1000):
                attempts += 1
                self.spawn_a_nucleus()

        print len(self.nuclei), "nuclei,",  attempts, "attempts"

        self.gap = 3

        # while len(self.nuclei) > 0:
        for i in range(6):

            # reporting:
            print "growing... {} nuclei and {} fibers.".format(
                len(self.nuclei), len(self.fibers))
            self.report()
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

        self.report()
        print  "The field now looks like this:"
        print self.field
        print "There are now {} nuclei and {} fibers.".format(
            len(self.nuclei), len(self.fibers))


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
    for i in range(1):
        Model6(
            field_size = 100,
            fiber_size =   4,
            gap        =   7).run()
        print