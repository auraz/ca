# -*- coding: utf-8 -*-

"""Клеточный автомат."""
    
import init
from grid import Grid
import copy


class Cell(object):
    pass




class Field(Grid):
    """Двухмерный список.

        Двухмерный список, предназначенный для использования в качестве
        поля клеточного автомата (но может быть использован и для других
        целей).
        Этот класс унаследован от list и ведёт себя так же, как и list.
        Поддерживает тот же синтаксис и методы.
        Его можно заполнять любыми объектами.
        Но нужно следить за тем, чтобы это был именно двухмерный список -
        список из списков, при этом каждый вложенный список должен быть
        одной и той же длины. Иначе он будет работать неправильно.
        Внутренняя проверка этих условий пока что не реализована.
        """

    def surround(self):
        """Окружает поле слоем из None со всех сторон.

            Меняет само поле. Возвращает None.
            """

        # Получаем ширину и высоту списка:
        w = self.width()
        h = self.height()

        for row in self:
            row[w:w] = [None]   # справа
            row[0:0] = [None]   # слева

        self[h:h] = [[None for i in range(w + 2)]]   # снизу
        self[0:0] = [self[h]]                        # сверху
    
    def get_inner(self):
        """Returns the field without the border."""
        return self.get_subgrid(1, 1, self.width() - 2, self.height() - 2)



    def neighbors(self, x, y):
        """Возвращает всех соседей заданной клетки.

            x и y - координаты клетки.

            Возвращает двухмерный список 3 х 3, содержащий значения
            заданной клетки и 8 её соседей. При этом сама заданная
            клетка всегда будет по центру.
            Если клетка находится у границы клеточного автомата,
            часть соседей будет иметь значение на None.
            Например, если метод вернул

            None None None
            None   1    2
            None   4    5

            , то это значит, что клетка находится в левом верхнем углу.
            """
        return self.get_subgrid(x, y, 3, 3)

#   get_a, get_b (returning Grid instances)

    # def __str__(seq):
    #     """Выводит двухмерную последовательность построчно."""
    #     return 

