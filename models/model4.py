# -*- coding: UTF-8 -*-

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




class Model4(MCA):
    """Модель 4.

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

        counter = 0
        while True:
            counter += 1

            self.spawn_a_nucleus()

            nuc = self.nuclei[random.randrange(len(self.nuclei))]
            info("A random nucleus is chosen. x = %s, y = %s, status = %s.", nuc.x, nuc.y, nuc.status)

            nuc.look_around()
            nuc.try_to_grow()

            if len(self.nuclei) == 0:
                info("There are no more nuclei. Stopping the model.")
                info("%s iterations have been carried out.", counter)
                print counter, "iterations have been carried out."
                break

        print "{} nuclei have grown to fibers.".format(len(self.fibers))


    def spawn_a_nucleus(self):
        """Засевает случайный зародыш.

            Случайным образом засевает новый зародыш. Если в его мёртвой зоне
            оказался другой зародыш или волокно, то новый зародыш сразу умирает.
            """
        n = self.field_size
        x, y = random.randrange(n), random.randrange(n)
        if self.field[y][x] == 0:
            nuc = Nucleus(x, y, self)
            if nuc.is_anything_near():
                nuc.die()
            else:
                info("A random nucleus is spawned. x = %s, y = %s.", x, y)
                self.report()



if __name__ == '__main__':
    for i in range(10):
        Model4(
            field_size = 100,
            fiber_size =   4,
            gap        =   5).run()
        print