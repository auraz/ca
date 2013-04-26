# -*- coding: utf-8 -*-

"""Клеточный автомат."""
    
import init
import copy

class CellularAutomaton():
    """Простая реализация клеточного автомата.

        Начальное состояние и функция перехода задаётся в модуле init.
        
        Поле клеточного автомата хранится в виде таблицы клеток,
        окружённой со всех сторон слем из None. Например:

        None None None None None
        None   1    2    3  None
        None   4    5    6  None
        None   7    8    9  None
        None  10   11   12  None
        None None None None None

        Этот слой обозначает границу клеточного автомата.
        Получить поле без слоя из None можно методом get_field().

        Сама таблица реализована в виде двухмерного списка.

        Нумерация начинается (по обеим осям) с -1.
        -1 - это граница, 0 - первая строка/столбец.
        """


    def __init__(self, field = init.field, next_value = init.next_value):
        """Создаёт новый клеточный автомат.

            field - начальное состояние (двухмерный список).
            next_value - функция перехода.
            
            По умолчанию начальное состояние и функция перехода берутся
            из модуля init.         
            Можно задать альтернативное начальное состояние и/или
            альтернативную функцию перехода, передав их в качестве аргументов.
            """

        self.next_value = next_value
        self.width = len(field[0])
        self.height = len(field)
        # Сделаем копию, иначе переданный извне список будет меняться
        self.field = copy.deepcopy(field)
        self.__surround(self.field)

    def __surround(self, grid):
        """Окружает заданный двухмерный список слоем из None со всех сторон.

            grid - двухмерный список.

            Меняет сам список. Возвращает None.
            """

        # Определяем ширину и высоту списка:
        w = len(grid[0])
        h = len(grid)

        for row in grid:
            row[w:w] = [None]   # справа
            row[0:0] = [None]   # слева

        grid[h:h] = [[None for i in range(w + 2)]]   # снизу
        grid[0:0] = [grid[h]]                        # сверху
    
    def next_cell_value(self, x, y):
        """Возвращает следующее значение клетки с координатами x и y."""
        return self.next_value(self.neighbors(x, y))
    
    def next(self):
        """Выполняет одну итерацию клеточного автомата."""
        new_field = [[self.next_cell_value(i, j) 
                        for i in range(self.width)] 
                            for j in range(self.height)]
        self.field = new_field
        self.__surround(self.field)
    


def print_2d(seq):
    """Выводит двухмерную последовательность построчно."""
    for row in seq:
        print row


if __name__ == '__main__':
    ca = CellularAutomaton()
    print
    print "Initial state of the cellular automaton:"
    print_2d(ca.get_field())
    print
    print "After one iteration:"
    ca.next()
    print_2d(ca.get_field())
    print
