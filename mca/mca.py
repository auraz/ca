# -*- coding: UTF-8 -*-

"""МКА - Модифицированный клеточный автомат.

    Модель образования и роста зародышей, представляющая собой
    модифицированный клеточный автомат (МКА).

    Отличия этой модели от клеточного автомата:

        1.  В обычном клеточном автомате правила перехода формулируются
            для клетки, а в модифицированном - для зародыша.
        2.  В обычном клеточном автомате правила перехода применяются
            ко всем клеткам одновременно. В МКА такого требования нет.
            Чаще всего изменения затрагивают один зародыш. Можно реализовать
            и одновременный обход всех зародышей, но это уже не является
            неотъемлемым свойством автомата.
        3.  В обычном клеточном автомате правила перехода для данной клетки
            основаны на соседних клетках, множество которых чётко определено.
            В МКА этого требования тоже нет. Можно как угодно задавать правила,
            по которым будет изменяться состояние зародыша. Можно при этом
            учитывать как угодно далеко расположенные клетки.

    Основные параметры модели:

      * field_size или n - размер поля;
      * fiber_size или d - конечный размер волокна;
      * gap        или g - минимальная толщина пустого пространства
                           между волокнами.

    Как и обычный клеточный автомат, МКА имеет поле.
    Это квадратная таблица n x n, состоящая из клеток.
    В этом поле образуются зародыши, и из них растут волокна.
    Кроме этого, МКА содержит списки зародышей и уже сформировавшихся волокон.

    Каждый зародыш стремится вырасти до волокна размером d x d клеток.
    При этом между волокнами должно быть не менее g свободных клеток
    по вертикали, горизонтали и диагонали.

    Клетки могут содержать любые данные, но только некоторые имеют смысл.
    Следующие значения имеют смысл:

      * 0 - пустая (свободная) клетка;
      * 1 - клетка волокна;
      * Nucleus - зародыш.

    Изначально поле заполнено нулями. Это значит, что оно пустое.
    Когда образуется зародыш, он занимает одну клетку. В этой клетке содержится
    объект класса Nucleus, который содержит основную информацию о зародыше.
    Когда зародыш растёт, соседние клетки заполняются единичками. Эти клетки
    интерпретируются как клетки волокна.
    В конце-концов зародыш либо вырастает до волокна размером d x d клеток,
    после чего объявляется сформировавшимся волокном и уже никак не изменяется,
    либо, если ему некуда расти, умирает вместе со своим волокном.

    Промежуточные состояния модели и происходящие изменения записываются в лог.
    В дальнейшем будет добавлена и визуализация.

    Чтобы создать свою модель, надо унаследовать от класса MCA
    (или от его потомка) и реализовать метод run(). После этого создать объект
    этого нового класса и вызвать его метод run(). (При желании его можно
    назвать иначе.) Поле, заполненное нулями, и пустые списки зародышей
    и волокон будут созданы автоматически.
    Также нужно задать конфигурацию для модуля logging.

    """

import random

import logging
from logging import debug, info

import sys
sys.path.append("..")

import numpy
# import numpy as np
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


# class Field(numpy.ndarray):
#     """Этот класс создан только для того, чтобы переопределить метод __str__()."""
#     def __str__(self):
#         """Возвращает поле в виде строки.

#             # - зародыш
#             o - волокно
#             . - пустая клетка
#             В начале и в конце - пустая строка.
#             Например:

#             ..........
#             ...oooo...
#             ...o#oo...
#             ...oooo...
#             ..........

#             """
#         s = ""
#         for y in range(self.shape[1]):
#             for x in range(self.shape[0]):
#                 if self[y, x] == 0:
#                     s += '.'
#                 elif self[y, x] == 1:
#                     s += 'o'
#                 else:
#                     s += '#'
#             s += '\n'
#         return s
        


class Nucleus:
    """Зародыш.

        Зародыш содержит следующие данные:

        * x, y - координаты зародыша в поле
        * mca - МКА, в котором находится зародыш
        * status - состояние зародыша, может иметь три значения:

          * 'n' - зародыш (nucleus) - значение по умолчанию
          * 'g' - растущее (growing) волокно
          * 'f' - волокно (fiber), которое уже выросло

        * left, right, up, down - на сколько клеток этот зародыш вырос
                                  в каждом из этих направлений
        
        Зародыш не может существовать сам по себе. Он привязан к МКА. Он
        содержит ссылку на свой МКА, и через эту ссылку получает доступ к
        полю и списку зародышей, в которых он находится. Например, так:
        ``self.mca.field``

        Зародыш имеет мёртвую зону - это все клетки, расстояние до которых
        не превышает gap по каждой координате. В этой зоне должны быть одни
        нули, иначе зародыш умрёт.
        Если зародыш уже начал расти, и у него появились клетки волокна, то
        мёртвая зона будет шире: расстояние считается до ближайшей клетки
        волокна.

        Зародыш умеет зарождаться, проверять свою мёртвую зону, расти, умирать.
        Также он умеет определять, в каких направлениях можно расти.
        """

    def __init__(self, x, y, mca, status = 'n', left = 0, right = 0, up = 0, down = 0):
        """Создаёт новый зародыш.

            Помимо заполнения данных, также прописывает зародыш в поле и
            в списке зародышей.
            """
        self.x = x
        self.y = y
        self.mca = mca
        self.status = status
        self.left = left
        self.right = right
        self.up = up
        self.down = down

        # Прописываем зародыш в списке зародышей.
        mca.nuclei.append(self)

        # Увеличиваем значение всех клеток "мёртвой зоны" на 1.
        f = self.mca.field
        n = self.mca.field_size
        gap = self.mca.gap
        x1 = max(self.x - gap, 0)
        y1 = max(self.y - gap, 0)
        x2 = min(self.x + gap + 1, n)
        y2 = min(self.y + gap + 1, n)
        for j in range(y1, y2):
            for i in range(x1, x2):
                f[j, i] += 1
        
        # В самой клетке зародыша прописываем фиксированное значение (переда)
        f[y, x] = self.mca.nucleus_cell_value


    def __str__(self):
        """Возвращает '#'."""
        return '#'

    def is_anything_near(self):
        """Проверяет, есть ли у зародыша соседи.

            Исследует окрестность зародыша: все клетки на расстоянии gap
            или меньше. Возвращает False, если все эти клетки (кроме самого
            зародыша) содержат нули. Иначе возвращает True.

            В настоящее время этот метод имеет смысл применять только для голых
            зародышей (у которых status == 'n').
            """
        if self.status != 'n':
            raise DeprecationWarning ("For now, this method is intended for use with 'n' nuclei only.")
        f = self.mca.field
        n = self.mca.field_size
        gap = self.mca.gap
        x1 = max(self.x - gap, 0)
        y1 = max(self.y - gap, 0)
        x2 = min(self.x + gap + 1, n)
        y2 = min(self.y + gap + 1, n)
        for j in range(y1, y2):
            for i in range(x1, x2):
                if f[j, i] != 0 and (i != self.x or j != self.y):
                    debug("Something found at x = %s and y = %s!", i, j)
                    return True
        debug("Nothing found near.")
        return False

    def look_around(self):
        """Определяет, в каких направлениях зародыш может расти.

            Проверяет полоски слева, справа, сверху и снизу от зародыша.
            Например, если gap == 2, то проверяет следующие клетки
            (отмечены звёздочками)::
            
                . * * * * *
                *           *
                *           *
                *     #     *
                *           *
                *           *
                . * * * * *
            
            Если в одной из этих полосок найдено что-либо, кроме нуля,
            то зародыш не может расти в соответствующем направлении.

            Также учитывает приграничные случаи.

            Результаты записывает в поля данных зародыша
            для последующего использования:
            
            * self.can_grow_left
            * self.can_grow_right
            * self.can_grow_up
            * self.can_grow_down
            * self.dims - число измерений, по которым зародыш
                          уже достиг размера fiber_size
            """

        gap = self.mca.gap
        n   = self.mca.field_size
        xl  = self.x - self.left - gap - 1
        xr  = self.x + self.right + gap + 1
        yu  = self.y - self.up - gap - 1
        yd  = self.y + self.down + gap + 1
        self.dims = 0
        debug("xl = %s, xr = %s, yu = %s, yd = %s", xl, xr, yu, yd)

        # left & rigth:
        if self.left + self.right + 1 == self.mca.fiber_size:
            self.can_grow_left = False
            self.can_grow_right = False
            self.dims += 1
            debug("The width already reached the fiber size. Can't grow left or right.")
        else:
            if xl < 0:
                info("Near the left border.")
                if self.x - self.left == 0:
                    self.can_grow_left = False
                else:
                    self.can_grow_left = True
            else:
                self.can_grow_left = True
                for y in range(max(yu + 1, 0), min(yd, n)):
                    if self.mca.field[y, xl] != 0:
                        self.can_grow_left = False
                        debug("Something found on the left. Can't grow left.")
                        break
            if xr > n - 1:
                info("Near the right border.")
                if self.x + self.right == n - 1:
                    self.can_grow_right = False
                else:
                    self.can_grow_right = True
            else:
                self.can_grow_right = True
                for y in range(max(yu + 1, 0), min(yd, n)):
                    if self.mca.field[y, xr] != 0:
                        self.can_grow_right = False
                        debug("Something found on the right. Can't grow right.")
                        break

        # up & down
        if self.up + self.down + 1 == self.mca.fiber_size:
            self.can_grow_up = False
            self.can_grow_down = False
            self.dims += 1
            debug("The height already reached the fiber size. Can't grow up or down.")
        else:
            if yu < 0:
                info("Near the top border.")
                if self.y - self.up == 0:
                    self.can_grow_up = False
                else:
                    self.can_grow_up = True
            else:
                self.can_grow_up = True
                for x in range(max(xl + 1, 0), min(xr, n)):
                    if self.mca.field[yu, x] != 0:
                        self.can_grow_up = False
                        debug("Something found on the up. Can't grow up.")
                        break
            if yd > n - 1:
                info("Near the bottom border.")
                if self.y + self.down == n - 1:
                    self.can_grow_down = False
                else:
                    self.can_grow_down = True
            else:
                self.can_grow_down = True
                for x in range(max(xl + 1, 0), min(xr, n)):
                    if self.mca.field[yd, x] != 0:
                        self.can_grow_down = False
                        debug("Something found on the down. Can't grow down.")
                        break


    def try_to_grow(self, die_safely = False):
        """Зародыш растёт, объявляется готовым волокном или умирает.
            
            Зародыш растёт в случайном направлении из доступных,
            объявляется сформировавшимся волокном или умирает.
            """
        if self.dims == 2:
            self.mca.nuclei.remove(self)
            self.mca.fibers.append(self)
            self.status = 'f'
            info("The nucleus has reached the fiber size in both dimentions. It will not grow anymore.")
            info("There are now %s nuclei and %s fibers.", len(self.mca.nuclei), len(self.mca.fibers))
            info("Now the field looks now like this:")
            info(self.mca.field)
        elif not (self.can_grow_left or self.can_grow_right or self.can_grow_up or self.can_grow_down):
            info("The nucleus can't grow so it will die.")
            if die_safely:
                self.mca.condemned.append(self)
            else:
                self.die()
        else:
            choices = [self.can_grow_left, self.can_grow_right, self.can_grow_up, self.can_grow_down]   # boolean values
            directions = [self.grow_to_left, self.grow_to_right, self.grow_to_up, self.grow_to_down]    # methods
            can_grow = [directions[i] for i in range(4) if choices[i]]               # list of allowed directions
            grow_to = random.choice(can_grow)
            debug("choices = %s, grow_to = %s, let's grow.", choices, grow_to)
            grow_to()
            self.status = 'g'
            info("Now the field looks now like this:")
            info(self.mca.field)


    def grow_to_left(self):
        """Зародыш растёт налево.

            self.left увеличивается на 1.
            Клетки слева от существующего волокна заполняются волокном.
            """
        info("Growing left.")
        self.left += 1
        for y in range(self.y - self.up, self.y + self.down + 1):
            self.mca.field[y, self.x - self.left] = 1

    def grow_to_right(self):
        """Зародыш растёт направо.

            self.left увеличивается на 1.
            Клетки слева от существующего волокна заполняются волокном.
            """
        info("Growing right.")
        self.right += 1
        for y in range(self.y - self.up, self.y + self.down + 1):
            self.mca.field[y, self.x + self.right] = 1

    def grow_to_up(self):
        """Зародыш растёт вверх.

            self.left увеличивается на 1.
            Клетки слева от существующего волокна заполняются волокном.
            """
        info("Growing up.")
        self.up += 1
        for x in range(self.x - self.left, self.x + self.right + 1):
            self.mca.field[self.y - self.up, x] = 1

    def grow_to_down(self):
        """Зародыш растёт вниз.

            self.left увеличивается на 1.
            Клетки слева от существующего волокна заполняются волокном.
            """
        info("Growing down.")
        self.down += 1
        for x in range(self.x - self.left, self.x + self.right + 1):
            self.mca.field[self.y + self.down, x] = 1


    def die(self):
        """Зародыш умирает.
            
            Вместе с зародышем умирает и его волокно.
            Место в поле, где находился зародыш и волокно, заполяется нулями.
            Зародыш выписывается из списка зародышей.
            """
        
        # Выписываем зародыш из списка зародышей:
        self.mca.nuclei.remove(self)

        # Заполняем место, где находится зародыш и волокно, нулями
        if self.status == 'n':
            self.mca.field[self.y][self.x] = 0
        else:
            for i in range(self.x - self.left, self.x + self.right + 1):
                for j in range(self.y - self.up, self.y + self.down + 1):
                    self.mca.field[j, i] = 0

        info("The nucleus died.")




class MCA:
    """Базовый класс для МКА.

        МКА содержит:
          * field - поле
          * nuclei - список зародышей, которые ещё не выросли до нужного размера
          * fibers - список зародышей, которые уже выросли
                     и получили статус волокна (f)

        А также параметры field_size, fiber_size, gap.

        Каждый зародыш содержит ссылку на МКА. Через эту ссылку он получает
        доступ к полю и спискам зародышей, в которых находится.

        Чтобы создать свою модель, нужно унаследовать от этого класса
        и реализовать метод run().
        """

    def __init__(self, field_size, fiber_size, gap):
        """Создаёт новый МКА.

            Помимо заполнения данных, создаёт поле и заполняет его нулями.
            А также создаёт пустые списки зародышей и волокон.
            """
        self.field_size = field_size
        self.fiber_size = fiber_size
        self.gap = gap

        # Create a field, initialize it with zeros
        # Create an empty list of nuclei and fibers
        self.field = numpy.zeros((field_size, field_size), dtype = numpy.int64)
        # Field([[0 for i in range(field_size)] for i in range(field_size)])
        self.nuclei = []
        self.fibers = []
        self.condemned = []


    def report(self):
        """Выводит в лог текущее состояние МКА."""

        info("There are now %s nuclei and %s fibers. The field now looks like this:", 
            len(self.nuclei), len(self.fibers))
        info(self.field)


    def plot(self):
        im = plt.imshow(self.field, cmap=cm.gray, interpolation='nearest')
        plt.show()


        

