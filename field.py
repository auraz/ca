# -*- coding: utf-8 -*-

class Field(list):

    # def __init__(self, param):
    #     pass

    # def width(self):
    #     return self.width

    # def height(self):
    #     return self.height


    def get_subfield(self, left  = 0, top    = 0,
                        width = 1, height = 1):
        """Возвращает клетки из заданного прямоугольного диапазона.

            left и top задают положение верхнего левого угла диапазона.
            width и height - его ширина и высота.

            Всегда возвращает двухмерный список, даже если там всего одна клетка.
            """

        return [row[left + 1 : left + width + 1]
            for row in self.field[top + 1 : top + height + 1]]
    
    def get_field(self):
        """Возвращает все клетки клеточного автомата"""
        return self.get_subfield(0, 0, self.width, self.height)

    def get_cell(self, x, y):
        """Возвращает значение клетки с координатами x и y."""
        return self.get_subfield(x, y)[0][0]


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
        return self.get_subfield(x - 1, y - 1, 3, 3)
    
    # Сомневаюсь, нужен ли этот метод.
    # def are_neighbors(self, x1, y1, x2, y2):
    #     """проверяет, являются ли заданные две клетки соседними"""
    #     return x2 - x1 in [-1, 0, 1] and y2 - y1 in [-1, 0, 1]
    