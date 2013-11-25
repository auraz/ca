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




class Model3(MCA):
    """Модель 3.

        Изначально зародышей забрасывается много, с запасом. Так, чтобы около
        каждого или почти каждого из них были другие зародыши на расстоянии
        менее 5 клеток. Число забрасываемых зародышей регулируется параметром
        ratio - это доля от общего числа клеток.

        Далее, на каждой итерации делаем следующее:
        1.  Выбираем случайный зародыш или волокно из тех, что ещё не доросли
            до размера 4х4.
        2.  Если у него есть соседи (другие зародыши или волокна на расстоянии
            менее 5 клеток), то он умирает.
        3.  Определяем, в каких направлениях он может расти:
            a)  он не может расти в некотором направлении, если в результате
                расстояние до соседнего волокна станет меньше 5;
            b)  если по какой-то оси он уже достиг размера в 4 клетки, больше он
                по этой оси не растёт;
            c)  и, понятное дело, он не может расти в стенку.
        4.  В зависимости от результата п. 3:
            a)  если зародыш может расти, он растёт на 1 клетку, направление
                выбирается случайно из доступных ему направлений;
            b)  если зародыш не может расти потому, что уже достиг размера 4х4,
                он объявляется сформировавшимся волокном и далее
                никак не меняется;
            c)  если зародыш не может расти, но ещё не достиг размера 4х4,
                он умирает вместе с волокном.
        Так продолжаем до тех пор, пока все зародыши не умрут или вырастут.

        О полученных таким образом зародышах можно сказать, что для них
        существует такое правило роста, при котором они вырастут до размера 4х4
        и при этом между ними будет расстояние не менее 5.
        """

    def __init__(self, field_size, fiber_size, gap, ratio):
        """Создаёт новую модель.

            ratio - это отношение числа забрасываемых зародышей
                    к общему числу клеток.
            """
        MCA.__init__(self, field_size, fiber_size, gap)
        self.ratio = ratio
    
    def run(self):
        """Запуск модели."""

        self.spawn_many_nuclei()

        while len(self.nuclei) > 0:
            # Выбираем случайный зародыш
            nuc = self.nuclei[random.randrange(len(self.nuclei))]
            info("A random nucleus is chosen. x = %s, y = %s, status = %s.", nuc.x, nuc.y, nuc.status)

            # Проверяем его мёртвую зону. Если там что-нибудь есть - зародыш умирает.
            if nuc.status == 'n' and nuc.is_anything_near():
                nuc.die()
                self.report()
                continue
            
            nuc.look_around()
            nuc.try_to_grow()

        print "The field looks like this:"
        print self.field
        print "{} nuclei have grown to fibers.".format(len(self.fibers))



    def spawn_many_nuclei(self):
        """Забросить зародышей в количестве self.ratio от общего числа клеток."""

        n = self.field_size
        while len(self.nuclei) < self.ratio * n**2:
            x, y = random.randrange(n), random.randrange(n)
            if self.field[y][x] == 0:
                nuc = Nucleus(x, y, self)
        info("%s nuclei are spawned. Now the field looks like this:", len(self.nuclei))
        info(self.field)



if __name__ == '__main__':
    Model3(
        field_size = 100,
        fiber_size =   4,
        gap        =   5,
        ratio      =   0.1).run()
    print