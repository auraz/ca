"""Класс Nucleus и некоторые вспомогательные функции."""

from ca.grid import Grid

class Nucleus:
    """Зародыш.

        Этот класс предназначен для хранения данных.
        Предполагается, что здесь будут храниться такие данные:

        status - состояние зародыша, может иметь три значения:
            'n' - зародыш (nucleus)
            'g' - растущее (growing) волокно
            'f' - волокно (fiber), которое уже выросло
        x, y - координаты зародыша
        left, right, up, down - на сколько клеток этот зародыш вырос
        в каждом из этих направлений
        """

    def __init__(self, x, y, status = 'n', left = 0, right = 0, up = 0, down = 0):
        self.x = x
        self.y = y
        self.status = status
        self.left = left
        self.right = right
        self.up = up
        self.down = down

    def kill(self, field):
        print "Dying..."
        if self.status == 'n':
            field[self.y][self.x] = 0
        else:
            # print "for i in range({}, {}:)".format(self.x - self.left, self.x + self.right + 1)
            for i in range(self.x - self.left, self.x + self.right + 1):
                # print "for j in range({}, {}):"format(self.y - self.up, self.y + self.down + 1)
                for j in range(self.y - self.up, self.y + self.down + 1):
                    print "({}, {}) ".format(i, j),
                    field[j][i] = 0

    def __str__(self):
        return '*'
        # return str(self.__dict__)

    def grow_to_left(self, field):
        print "*/Growing left."
        self.left += 1
        for y in range(self.y - self.up, self.y + self.down + 1):
            field[y][self.x - self.left] = 1

    def grow_to_right(self, field):
        print "*/Growing right."
        self.right += 1
        for y in range(self.y - self.up, self.y + self.down + 1):
            field[y][self.x + self.right] = 1

    def grow_to_up(self, field):
        print "*/Growing up."
        self.up += 1
        for x in range(self.x - self.left, self.x + self.right + 1):
            field[self.y - self.up][x] = 1

    def grow_to_down(self, field):
        print "*/Growing down."
        self.down += 1
        for x in range(self.x - self.left, self.x + self.right + 1):
            field[self.y + self.down][x] = 1




def is_anything_near(nuc, f, n, r):
    x1 = max(nuc.x - r, 0)
    y1 = max(nuc.y - r, 0)
    x2 = min(nuc.x + r + 1, n)
    y2 = min(nuc.y + r + 1, n)
    print "Checking in range {} to {} by x and {} to {} by y".format(x1, x2-1, y1, y2-1)
    for j in range(y1, y2):
        for i in range(x1, x2):
            print f[j][i],
            if f[j][i] != 0 and (i != nuc.x or j != nuc.y):
                print "Something found at x = {} and y = {}!".format(i, j)
                # print "i =", i, 'x =', x, 'j =', j, 'y =', y
                return True
        print
    return False


def print_field(field):
    for y in range(field.height()):
        for x in range(field.width()):
            if field[y][x] == 0:
                print '.',
            elif field[y][x] == 1:
                print 'o',
            else:
                print '#',
        print
