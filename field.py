# -*- coding: utf-8 -*-

class Field(list):

    def width(self):
        if self == []:
            return 0
        else:
            return len(self[0])

    def height(self):
        return len(self)


    def get_subfield(self, left  = 0, top    = 0,
                        width = 1, height = 1):
        """Возвращает клетки из заданного прямоугольного диапазона.

            left и top задают положение верхнего левого угла диапазона.
            width и height - его ширина и высота.

            Всегда возвращает двухмерный список, даже если там всего одна клетка.
            """

        return [row[left : left + width]
            for row in self[top : top + height]]

