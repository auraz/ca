# -*- coding: UTF-8 -*-

"""Модель образования и роста зародышей."""

import random

import logging
from logging import debug, info
logging.basicConfig(
    level    = logging.INFO,
    filename = 'model.log',
    filemode = 'w',
    format   = '%(message)s')

import ca.grid

class Field(ca.grid.Grid):
    """Этот класс создан исключительно для того, чтобы переопределить метод __str__()."""
    def __str__(self):
        """Возвращает поле в виде строки.

            # - зародыш
            o - волокно
            . - пустая клетка
            В начале и в конце - пустая строка.
            Например:

            ..........
            ...oooo...
            ...o#oo...
            ...oooo...
            ..........

            """
        s = ""
        for y in range(self.height()):
            for x in range(self.width()):
                if self[y][x] == 0:
                    s += '.'
                elif self[y][x] == 1:
                    s += 'o'
                else:
                    s += '#'
            s += '\n'
        return s
        


class Nucleus:
    """Зародыш.

        """

    def __init__(self, x, y, model, status = 'n', left = 0, right = 0, up = 0, down = 0):
        """Создаёт новый зародыш.

            Зародыш содержит следующие данные:

            x, y - координаты зародыша
            model - модель, к которой относится зародыш
            status - состояние зародыша, может иметь три значения:
                'n' - зародыш (nucleus) - значение по умолчанию
                'g' - растущее (growing) волокно
                'f' - волокно (fiber), которое уже выросло
            left, right, up, down - на сколько клеток этот зародыш вырос
            в каждом из этих направлений

            Помимо заполнения данных, также прописывает зародыш в поле и в списке.
            """
        self.x = x
        self.y = y
        self.model = model
        self.status = status
        self.left = left
        self.right = right
        self.up = up
        self.down = down

        # Прописываем зародыш в поле и в списке зародышей.
        model.field[y][x] = self
        model.nuclei.append(self)

    def __str__(self):
        return '#'
        # return str(self.__dict__)

    def is_anything_near(self):
        """Проверяет, есть ли у зародыша соседи.

            Исследует окрестность зародыша: все клетки на расстоянии gap или меньше.
            Возвращает False, если все эти клетки (кроме самого зародыша) содержат нули.
            Иначе возвращает True.

            В настоящее время этот метод имеет смысл применять только для голых зародышей
            (у которых status == 'n').
            """
        if self.status != 'n':
            raise DeprecationWarning ("For now, this method is intended for use with 'n' nuclei only.")
        f = self.model.field
        n = self.model.field_size
        gap = self.model.gap
        x1 = max(self.x - gap, 0)
        y1 = max(self.y - gap, 0)
        x2 = min(self.x + gap + 1, n)
        y2 = min(self.y + gap + 1, n)
        for j in range(y1, y2):
            for i in range(x1, x2):
                if f[j][i] != 0 and (i != self.x or j != self.y):
                    debug("Something found at x = %s and y = %s!", i, j)
                    return True
        debug("Nothing found near.")
        return False

    def look_around(self):
        """Определяет, в каких направлениях зародыш может расти.

            Проверяет полоски слева, справа, сверху и снизу от зародыша.
            Например, если gap == 2, то проверяет следующие клетки (отмечены звёздочками):
            
              * * * * *
            *           *
            *           *
            *     #     *
            *           *
            *           *
              * * * * *
            
            Если в одной из этих полосок найдено что-либо, кроме нуля,
            то зародыш не может расти в соответствующем направлении.

            Также учитывает приграничные случаи.

            Результаты записывает в поля данных зародыша для последующего использования:
            self.can_grow_left
            self.can_grow_right
            self.can_grow_up
            self.can_grow_down
            self.dims - число измерений, по которым зародыш уже достиг размера fiber_size
            """

        gap = self.model.gap
        n   = self.model.field_size
        xl  = self.x - self.left - gap - 1
        xr  = self.x + self.right + gap + 1
        yu  = self.y - self.up - gap - 1
        yd  = self.y + self.down + gap + 1
        self.dims = 0
        debug("xl = %s, xr = %s, yu = %s, yd = %s", xl, xr, yu, yd)

        # left & rigth:
        if self.left + self.right + 1 == self.model.fiber_size:
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
                    if self.model.field[y][xl] != 0:
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
                    if self.model.field[y][xr] != 0:
                        self.can_grow_right = False
                        debug("Something found on the right. Can't grow right.")
                        break

        # up & down
        if self.up + self.down + 1 == self.model.fiber_size:
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
                    if self.model.field[yu][x] != 0:
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
                    if self.model.field[yd][x] != 0:
                        self.can_grow_down = False
                        debug("Something found on the down. Can't grow down.")
                        break


    def grow(self):
        """docstring"""
        if self.dims == 2:
            self.model.nuclei.remove(self)
            self.model.fibers.append(self)
            self.status = 'f'
            info("The nucleus has reached the fiber size in both dimentions. It will not grow anymore.")
            info("There are now %s nuclei and %s fibers.", len(self.model.nuclei), len(self.model.fibers))
            info("Now the field looks now like this:")
            info(self.model.field)
        elif not (self.can_grow_left or self.can_grow_right or self.can_grow_up or self.can_grow_down):
            info("The nucleus can't grow so it will die.")
            self.die()
        else:
            choices = [self.can_grow_left, self.can_grow_right, self.can_grow_up, self.can_grow_down]
            directions = [self.grow_to_left, self.grow_to_right, self.grow_to_up, self.grow_to_down]
            can_grow = [directions[i] for i in range(4) if choices[i]]
            grow_to = random.choice(can_grow)
            debug("choices = %s, grow_to = %s, let's grow.", choices, grow_to)
            grow_to()
            self.status = 'g'
            info("Now the field looks now like this:")
            info(self.model.field)


    def grow_to_left(self):
        """Зародыш растёт влево.

            self.left увеличивается на 1.
            Клетки слева от существующего волокна заполняются волокном.
            """
        info("Growing left.")
        self.left += 1
        for y in range(self.y - self.up, self.y + self.down + 1):
            self.model.field[y][self.x - self.left] = 1

    def grow_to_right(self):
        info("Growing right.")
        self.right += 1
        for y in range(self.y - self.up, self.y + self.down + 1):
            self.model.field[y][self.x + self.right] = 1

    def grow_to_up(self):
        info("Growing up.")
        self.up += 1
        for x in range(self.x - self.left, self.x + self.right + 1):
            self.model.field[self.y - self.up][x] = 1

    def grow_to_down(self):
        info("Growing down.")
        self.down += 1
        for x in range(self.x - self.left, self.x + self.right + 1):
            self.model.field[self.y + self.down][x] = 1


    def die(self):
        
        # Выписываем зародыш из списка зародышей:
        self.model.nuclei.remove(self)

        # Заполняем место, где находится зародыш и волокно, нулями
        if self.status == 'n':
            self.model.field[self.y][self.x] = 0
        else:
            for i in range(self.x - self.left, self.x + self.right + 1):
                for j in range(self.y - self.up, self.y + self.down + 1):
                    self.model.field[j][i] = 0

        info("The nucleus died.")
        info("There are now %s nuclei and %s fibers. The field now looks like this:", 
            len(self.model.nuclei), len(self.model.fibers))
        info(self.model.field)




class Model:
    """Базовый класс для моделей

        Модель содержит:
            field - поле
            nuclei - список зародышей, которые ещё не выросли до нужного размера
            fibers - список зародышей, которые уже выросли и получили статус волокна (f)
        А также параметры field_size, fiber_size, gap.

        

        """

    def __init__(self, field_size, fiber_size, gap):
        self.field_size = field_size
        self.fiber_size = fiber_size
        self.gap = gap

        # Create a field, initialize it with zeros
        # Create an empty list of nuclei and fibers
        self.field = Field([[0 for i in range(field_size)] for i in range(field_size)])
        self.nuclei = []
        self.fibers = []

        

class Model3(Model):
    """docstring for Model3"""

    def __init__(self, field_size, fiber_size, gap, ratio):
        Model.__init__(self, field_size, fiber_size, gap)
        self.ratio = ratio
    
    def run(self):
        """Запуск модели.

            """

        self.spawn_many_nuclei()

        while len(self.nuclei) > 0:
            # Выбираем случайный зародыш
            nuc = self.nuclei[random.randrange(len(self.nuclei))]
            info("A random nucleus is chosen. x = %s, y = %s, status = %s.", nuc.x, nuc.y, nuc.status)

            # Проверяем его мёртвую зону. Если там что-нибудь есть - зародыш умирает.
            if nuc.status == 'n' and nuc.is_anything_near():
                nuc.die()
                continue
            
            nuc.look_around()
            nuc.grow()

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



class Model4(Model):
    """docstring for Model4"""
    def run(self):
        n = self.field_size
        counter = 0
        while True:
            counter += 1

            # Засеваем случайный зародыш
            x, y = random.randrange(n), random.randrange(n)
            if self.field[y][x] == 0:
                nuc = Nucleus(x, y, self)
                if nuc.is_anything_near():
                    nuc.die()
                else:
                    info("A random nucleus is spawned. x = %s, y = %s.", x, y)
                    info("Now the field looks like this:")
                    info(self.field)
            
            # Выбираем случайный зародыш
            nuc = self.nuclei[random.randrange(len(self.nuclei))]
            info("A random nucleus is chosen. x = %s, y = %s, status = %s.", nuc.x, nuc.y, nuc.status)

            # Проверяем его мёртвую зону. Если там что-нибудь есть - зародыш умирает.
            if nuc.status == 'n' and nuc.is_anything_near():
                nuc.die()
                continue
            
            nuc.look_around()
            nuc.grow()

            if len(self.nuclei) == 0:
                info("There are no more nuclei. Stopping the model.")
                info("%s iterations have been carried out.", counter)
                print counter, "iterations have been carried out."
                break

        # print "The field looks like this:"
        # print self.field
        print "{} nuclei have grown to fibers.".format(len(self.fibers))
        

if __name__ == '__main__':
    # Model3(100, 4, 5, 0.1).run()
    Model4(100, 4, 5).run()