# -*- coding: UTF-8 -*-


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

        self.spawn_nuclei(step)
        self.grow_fibers(plot)



    def spawn_nuclei(self, step = 0.1, plot = False, nucleus_cell_value = 7):

        if isinstance(step, int):
            pass
        elif isinstance(step, float):
            step = int(step * self.attempts)
        else:
            raise TypeError("'step' must be an int or a float.")

        self.nucleus_cell_value = nucleus_cell_value

        # Make a list of random numbers without repetitions:
        random_list = range(self.field_size**2)
        random.shuffle(random_list)

        for i in range(self.attempts / step):
            for r in random_list[i * step : (i + 1) * step]:
                x = r % self.field_size
                y = r / self.field_size
                if self.field[y, x] == 0:
                    nuc = Nucleus(x, y, self)
            print (i + 1) * step, len(self.nuclei)
        
        if plot:
            self.plot()


    
    def grow_fibers(self, plot = False):

        self.gap = self.g2

        self.field *= 0

        for nuc in self.nuclei:
            self.field[nuc.y, nuc.x] = 1

        for i in range((self.fiber_size - 1) * 2):

            if plot == "each step":
                self.plot()

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

        concentration = 100.0 * len(self.nuclei) * self.fiber_size**2 / self.field_size**2
        print "{} * {} / {} * 100% = {}%".format(
            len(self.nuclei), self.fiber_size**2, self.field_size**2, concentration)
        print "Fibers take {}%.".format(concentration)
        self.concentration = concentration

        if plot or (plot == "each step"):
            self.plot()


        





if __name__ == '__main__':
    m = Model6(
        n  = 300,
        a  = 1.0,
        f  = 8,
        g1 = 14,
        g2 = 7
    )
    m.spawn_nuclei(plot = True)
    m.grow_fibers(plot = True)
