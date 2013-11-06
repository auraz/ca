"""Класс Nucleus и некоторые вспомогательные функции."""

import random
from ca.grid import Grid

class Nucleus:
    """Зародыш.

        Зародыш содержит следующие данные:

        status - состояние зародыша, может иметь три значения:
            'n' - зародыш (nucleus) - значение по умолчанию
            'g' - растущее (growing) волокно
            'f' - волокно (fiber), которое уже выросло
        x, y - координаты зародыша
        left, right, up, down - на сколько клеток этот зародыш вырос
        в каждом из этих направлений
        model
        """

    def __init__(self, x, y, model, status = 'n', left = 0, right = 0, up = 0, down = 0):
        """Создаёт новый зародыш.

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

    def kill(self):
        
        # Выписываем зародыш из списка зародышей:
        self.model.nuclei.remove(self)

        # Заполняем место, где находится зародыш и волокно, нулями
        if self.status == 'n':
            self.model.field[self.y][self.x] = 0
        else:
            for i in range(self.x - self.left, self.x + self.right + 1):
                for j in range(self.y - self.up, self.y + self.down + 1):
                    self.model.field[j][i] = 0

    def __str__(self):
        return '*'
        # return str(self.__dict__)

    def is_anything_near(self):
        f = self.model.field
        n = self.model.field_size
        gap = self.model.gap
        x1 = max(self.x - gap, 0)
        y1 = max(self.y - gap, 0)
        x2 = min(self.x + gap + 1, n)
        y2 = min(self.y + gap + 1, n)
        # print "Checking in range {} to {} by x and {} to {} by y".format(x1, x2-1, y1, y2-1)
        for j in range(y1, y2):
            for i in range(x1, x2):
                # print f[j][i],
                if f[j][i] != 0 and (i != self.x or j != self.y):
                    # print "Something found at x = {} and y = {}!".format(i, j)
                    # print "i =", i, 'x =', x, 'j =', j, 'y =', y
                    return True
            # print
        return False

    def look_around(self):
        gap = self.model.gap
        n   = self.model.field_size
        xl = self.x - self.left - gap - 1
        xr = self.x + self.right + gap + 1
        yu = self.y - self.up - gap - 1
        yd = self.y + self.down + gap + 1
        self.dims = 0
        print "xl = {}, xr = {}, yu = {}, yd = {}".format(xl, xr, yu, yd)

        # left & rigth:
        if self.left + self.right + 1 == self.model.fiber_size:
            self.can_grow_left = False
            self.can_grow_right = False
            self.dims += 1
            print "Already reached the size in x dimension. Can't grow left or right."
        else:
            print "Not reached the size in x dimension yet."
            if xl < 0:
                print "Near the left border."
                if self.x - self.left == 0:
                    self.can_grow_left = False
                else:
                    self.can_grow_left = True
                print "Can grow left:", self.can_grow_left
            else:
                self.can_grow_left = True
                print "Checking for y in range({}, {})".format(max(yu + 1, 0), min(yd, n))
                for y in range(max(yu + 1, 0), min(yd, n)):
                    print self.model.field[y][xl]
                    if self.model.field[y][xl] != 0:
                        self.can_grow_left = False
                        print "Something found on the left. Can't grow left."
                        break
                # print "The way left is clear. Can grow left."
            if xr > n - 1:
                print "Near the right border."
                if self.x + self.right == n - 1:
                    self.can_grow_right = False
                else:
                    self.can_grow_right = True
                print "Can grow right:", self.can_grow_right
            else:
                self.can_grow_right = True
                print "Checking for y in range({}, {})".format(max(yu + 1, 0), min(yd, n))
                for y in range(max(yu + 1, 0), min(yd, n)):
                    print self.model.field[y][xr]
                    if self.model.field[y][xr] != 0:
                        self.can_grow_right = False
                        print "Something found on the right. Can't grow right."
                        break
                # print "The way right is clear. Can grow right."

        # up & down
        # print "Figuring out if it can grow up or down."
        if self.up + self.down + 1 == self.model.fiber_size:
            self.can_grow_up = False
            self.can_grow_down = False
            self.dims += 1
            print "Already reached the size in y dimension. Can't grow up or down."
        else:
            print "Not reached the size in y dimension yet."
            if yu < 0:
                print "Near the top border."
                if self.y - self.up == 0:
                    self.can_grow_up = False
                else:
                    self.can_grow_up = True
                print "Can grow up:", self.can_grow_up
            else:
                self.can_grow_up = True
                print "Checking for x in range({}, {})".format(max(xl + 1, 0), min(xr, n))
                for x in range(max(xl + 1, 0), min(xr, n)):
                    print self.model.field[yu][x],
                    if self.model.field[yu][x] != 0:
                        self.can_grow_up = False
                        print "Something found on the up. Can't grow up."
                        break
                # print "The way up is clear. Can grow up."
            if yd > n - 1:
                print "Near the bottom border."
                if self.y + self.down == n - 1:
                    self.can_grow_down = False
                else:
                    self.can_grow_down = True
                print "Can grow down:", self.can_grow_down
            else:
                self.can_grow_down = True
                print "Checking for x in range({}, {})".format(max(xl + 1, 0), min(xr, n))
                for x in range(max(xl + 1, 0), min(xr, n)):
                    print self.model.field[yd][x],
                    if self.model.field[yd][x] != 0:
                        self.can_grow_down = False
                        print "Something found on the down. Can't grow down."
                        break
                # print "The way down is clear. Can grow down."

    def grow(self):
        """docstring"""
        if self.dims == 2:
            self.model.nuclei.remove(self)
            self.model.fibers.append(self)
            self.status = 'f'
            print "*/Reached nirvana!!! Congrats. There are now {} nuclei and {} fibers.".format(len(self.model.nuclei), len(self.model.fibers))
        elif not (self.can_grow_left or self.can_grow_right or self.can_grow_up or self.can_grow_down):
            print "*/Sorry guy... You can't grow so you'll dye."
            self.kill()
            print "There are now {} nuclei and {} fibers".format(len(self.model.nuclei), len(self.model.fibers))
            print "Now the field looks now like this:"
            self.model.print_field()
        else:
            choices = [self.can_grow_left, self.can_grow_right, self.can_grow_up, self.can_grow_down]
            directions = [self.grow_to_left, self.grow_to_right, self.grow_to_up, self.grow_to_down]
            can_grow = [directions[i] for i in range(4) if choices[i]]
            grow_to = random.choice(can_grow)
            if self.can_grow_left:
                print 'Can grow left.'
            if self.can_grow_right:
                print 'Can grow right.'
            if self.can_grow_up:
                print 'Can grow up.'
            if self.can_grow_down:
                print 'Can grow down.'
            print "choices = {}, grow_to = {}, let's grow.".format(choices, grow_to)
            grow_to()
            self.status = 'g'
            print "Now the field looks now like this:"
            self.model.print_field()





    def grow_to_left(self):
        """Зародыш растёт влево.

            self.left увеличивается на 1.
            Клетки слева от существующего волокна заполняются волокном.
            # Клетки слева от существующей зоны влияния увеличиваются на 1.
            """
        print "*/Growing left."
        self.left += 1
        for y in range(self.y - self.up, self.y + self.down + 1):
            self.model.field[y][self.x - self.left] = 1

    def grow_to_right(self):
        print "*/Growing right."
        self.right += 1
        for y in range(self.y - self.up, self.y + self.down + 1):
            self.model.field[y][self.x + self.right] = 1

    def grow_to_up(self):
        print "*/Growing up."
        self.up += 1
        for x in range(self.x - self.left, self.x + self.right + 1):
            self.model.field[self.y - self.up][x] = 1

    def grow_to_down(self):
        print "*/Growing down."
        self.down += 1
        for x in range(self.x - self.left, self.x + self.right + 1):
            self.model.field[self.y + self.down][x] = 1





class Model:
    """Базовый класс для моделей"""
    def __init__(self, field_size, fiber_size, gap):
        self.field_size = field_size
        self.fiber_size = fiber_size
        self.gap = gap

        # Create a field, initialize it with zeros
        # Create an empty list of nuclei and fibers
        self.field = Grid([[0 for i in range(field_size)] for i in range(field_size)])
        self.nuclei = []
        self.fibers = []

        


    def print_field(self):
        for y in range(self.field.height()):
            for x in range(self.field.width()):
                if self.field[y][x] == 0:
                    print '.',
                elif self.field[y][x] == 1:
                    print 'o',
                else:
                    print '#',
            print


    # def spawn_a_nucleus(self):
    #     pass

    # def where_can_grow(self):
    #     pass

    # def grow_or_die(self):
    #     pass


class Model3(Model):
    """docstring for Model3"""

    def __init__(self, field_size, fiber_size, gap, ratio):
        Model.__init__(self, field_size, fiber_size, gap)
        self.ratio = ratio
    
    def run(self):
        # """Запуск модели.

        #     Цикл.
        #         Забрасывается один зародыш. Если он попадает в чью-то мёртвую зону - тут же умирает.
        #         Выбирается случайный зародыш.
        #         Проверяется, в какие стороны он может расти.
        #         Если ни в какие - он либо умирает, либо объявляется досгигнувшим статуса волокна.
        #         Иначе случайно выбирается направление, и он в этом направлении растёт.
        #     Условие окончания цикла пока не ясно.
        #     """

        self.spawn_many_nuclei()

        while len(self.nuclei) > 0:
            # Выбираем случайный зародыш
            nuc = self.nuclei[random.randrange(len(self.nuclei))]

            # Перевіряємо його мертву зону. Якщо там щось є - зародок вмирає.
            if nuc.status == 'n' and nuc.is_anything_near():
                nuc.kill()
                continue
            nuc.look_around()
            nuc.grow()

        print "There are now {} nuclei and {} fibers".format(len(self.nuclei), len(self.fibers))




    def spawn_many_nuclei(self):
        """Забросить зародышей в количестве self.ratio от общего числа клеток."""

        n = self.field_size
        while len(self.nuclei) < self.ratio * n**2:
            x, y = random.randrange(n), random.randrange(n)
            if self.field[y][x] == 0:
                nuc = Nucleus(x, y, self)
                # print 'No {}: x = {}, y = {}'.format(len(nuclei), nuc.x, nuc.y)
        # print_field(field)


if __name__ == '__main__':
    Model3(100, 4, 5, 0.1).run()