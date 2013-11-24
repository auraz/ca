# -*- coding: UTF-8 -*-

"""Модель образования и роста зародышей.

    Эта модель представляет собой модифицированный клеточный автомат.

    Основные параметры модели:
        field_size или n - размер поля;
        fiber_size или d - конечный размер волокна;
        gap        или g - минимальная толщина пустого пространства
                           между волокнами.

    Есть поле. Это квадратная таблица n x n. Её ячейки называются клетками.
    В этом поле образуются зародыши, и из них растут волокна.

    Каждый зародыш стремится вырасти до волокна размером d x d клеток.
    При этом между волокнами должно быть не менее g свободных клеток
    по вертикали, горизонтали и диагонали.

    Клетки могут содержать любые данные, но не все они имеют смысл.
    Следующие значения имеют смысл в рамках модели:
        0 - пустая (свободная) клетка;
        1 - клетка волокна;
        Nucleus - зародыш.

    Изначально поле заполнено нулями. Это значит, что оно пустое.
    Когда образуется зародыш, он занимает одну клетку. В этой клетке содержится
    объект класса Nucleus, который содержит основную информацию о зародыше.
    Когда зародыш растёт, соседние клетки заполняются единичками. Эти клетки
    интерпретируются как клетки волокна.
    В конце-концов зародыш либо вырастает до волокна размером d x d клеток,
    после чего объявляется сформировавшимся волокном и уже никак не изменяется,
    либо, если ему некуда расти, умирает вместе со своим волокном.

    Чтобы создать свою модель, надо унаследовать от класса Model
    (или от его потомка) и реализовать метод run(). После этого создать объект
    этого нового класса и вызвать его метод run(). Поле, заполненное нулями,
    и пустые списки зародышей и волокон, будут созданы автоматически.

    Промежуточные состояния модели и происходящие изменения записываются в лог.
    В дальнейшем будет добавлена и визуализация.

    Отличия этой модели от клеточного автомата:

        1. В клеточном автомате правила перехода формулируются для клетки,
           а в этой модели - для зародыша.
        2. В клеточном автомате правила перехода применяются ко всем клеткам
           одновременно. В этой модели такого требования нет. Чаще всего
           изменения затрагивают один зародыш. Можно реализовать и одновременный
           обход всех зародышей, но это уже не является неотъемлемым свойством
           модели.
        3. В клеточном автомате правила перехода для данной клетки основаны на
           соседних клетках, множество которых чётко определено. В этой модели
           этого требования тоже нет. Можно как угодно задавать правила,
           по которым будет изменяться состояние зародыша. Можно при этом
           учитывать как угодно далеко расположенные клетки.

    """

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
    """Этот класс создан только для того, чтобы переопределить метод __str__()."""
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

        Зародыш содержит следующие данные:

        x, y - координаты зародыша в поле
        model - модель, в которой находится зародыш
        status - состояние зародыша, может иметь три значения:
            'n' - зародыш (nucleus) - значение по умолчанию
            'g' - растущее (growing) волокно
            'f' - волокно (fiber), которое уже выросло
        left, right, up, down - на сколько клеток этот зародыш вырос
                                в каждом из этих направлений
        
        Зародыш не может существовать сам по себе. Он привязан к модели. Он
        содержит ссылку на свою модель, и через эту ссылку получает доступ к
        полю и списку зародышей, в которых он находится. Например, так:
        self.model.field

        Зародыш имеет мёртвую зону - это все клетки, расстояние до которых
        не превышает gap по каждой координате. В этой зоне должны быть одни
        нули, иначе зародыш умрёт.
        Если зародыш уже начал расти, и у него появились клетки волокна, то
        мёртвая зона будет шире: расстояние считается до ближайшей клетки
        волокна.

        Зародыш умеет зарождаться, проверять свою мёртвую зону, расти, умирать.
        Также он умеет определять, в каких направлениях можно расти.
        """

    def __init__(self, x, y, model, status = 'n', left = 0, right = 0, up = 0, down = 0):
        """Создаёт новый зародыш.

            Помимо заполнения данных, также прописывает зародыш в поле и
            в списке зародышей.
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
            Например, если gap == 2, то проверяет следующие клетки
            (отмечены звёздочками):
            
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

            Результаты записывает в поля данных зародыша
            для последующего использования:
            self.can_grow_left
            self.can_grow_right
            self.can_grow_up
            self.can_grow_down
            self.dims - число измерений, по которым зародыш
                        уже достиг размера fiber_size
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


    def try_to_grow(self):
        """Зародыш растёт, объявляется готовым волокном или умирает.
            
            Зародыш растёт в случайном направлении из доступных,
            объявляется сформировавшимся волокном или умирает.
            """
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
        """Зародыш растёт налево.

            self.left увеличивается на 1.
            Клетки слева от существующего волокна заполняются волокном.
            """
        info("Growing left.")
        self.left += 1
        for y in range(self.y - self.up, self.y + self.down + 1):
            self.model.field[y][self.x - self.left] = 1

    def grow_to_right(self):
        """Зародыш растёт направо.

            self.left увеличивается на 1.
            Клетки слева от существующего волокна заполняются волокном.
            """
        info("Growing right.")
        self.right += 1
        for y in range(self.y - self.up, self.y + self.down + 1):
            self.model.field[y][self.x + self.right] = 1

    def grow_to_up(self):
        """Зародыш растёт вверх.

            self.left увеличивается на 1.
            Клетки слева от существующего волокна заполняются волокном.
            """
        info("Growing up.")
        self.up += 1
        for x in range(self.x - self.left, self.x + self.right + 1):
            self.model.field[self.y - self.up][x] = 1

    def grow_to_down(self):
        """Зародыш растёт вниз.

            self.left увеличивается на 1.
            Клетки слева от существующего волокна заполняются волокном.
            """
        info("Growing down.")
        self.down += 1
        for x in range(self.x - self.left, self.x + self.right + 1):
            self.model.field[self.y + self.down][x] = 1


    def die(self):
        """Зародыш умирает.
            
            Вместе с зародышем умирает и его волокно.
            Место в поле, где находился зародыш и волокно, заполяется нулями.
            Зародыш выписывается из списка зародышей.
            """
        
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




class Model:
    """Базовый класс для моделей.

        Модель содержит:
            field - поле
            nuclei - список зародышей, которые ещё не выросли до нужного размера
            fibers - список зародышей, которые уже выросли
                     и получили статус волокна (f)
        А также параметры field_size, fiber_size, gap.

        Каждый зародыш содержит ссылку на модель. Через эту ссылку он получает
        доступ к полю и спискам зародышей, в которых находится.

        Чтобы создать свою модель, нужно унаследовать от этого класса
        и реализовать метод run().
        """

    def __init__(self, field_size, fiber_size, gap):
        """Создаёт новую модель.

            Помимо заполнения данных, создаёт поле и заполняет его нулями.
            А также создаёт пустые списки зародышей и волокон.
            """
        self.field_size = field_size
        self.fiber_size = fiber_size
        self.gap = gap

        # Create a field, initialize it with zeros
        # Create an empty list of nuclei and fibers
        self.field = Field([[0 for i in range(field_size)] for i in range(field_size)])
        self.nuclei = []
        self.fibers = []


    def report(self):
        """Выводит в лог текущее состояние модели."""

        info("There are now %s nuclei and %s fibers. The field now looks like this:", 
            len(self.nuclei), len(self.fibers))
        info(self.field)


        

class Model3(Model):
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
        Model.__init__(self, field_size, fiber_size, gap)
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



class Model4(Model):
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
        


class Model5(Model4):
    """Модель 5.

        Сначала полностью выполняем Модель 4.
        После этого проходимся по всему полю и дополнительно засеваем зародыши
        там, где это возможно (чтобы у каждого была пустая мёртвая зона),
        то есть в больших порах.
        Далее они все пытаются расти и сформировать дополнительные волокна.
        """

    def run(self):
        """Запуск модели."""
        
        Model4.run(self)
        
        n = self.field_size
        for x in range(n):
            for y in range(n):
                if self.field[y][x] == 0:
                    nuc = Nucleus(x, y, self)
                    if nuc.is_anything_near():
                        nuc.die()
        print len(self.nuclei), "additional nuclei have been spawned."

        while len(self.nuclei) > 0:
            nuc = self.nuclei[random.randrange(len(self.nuclei))]
            info("A random nucleus is chosen. x = %s, y = %s, status = %s.", nuc.x, nuc.y, nuc.status)

            if nuc.status == 'n' and nuc.is_anything_near():
                nuc.die()
                continue
            
            nuc.look_around()
            nuc.try_to_grow()
        
        print len(self.fibers), "nuclei have grown to fibers."



if __name__ == '__main__':
    for i in range(10):
        Model5(
            field_size = 100,
            fiber_size =   4,
            gap        =   5).run()
        print