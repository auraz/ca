# -*- coding: utf-8 -*-

"""Клеточный автомат."""
    
import init
import field
import copy


class CellularAutomaton():
    """Простая реализация клеточного автомата.

        Начальное состояние и функция перехода задаётся в модуле init.
        Поле хранится в field, а функция перехода - в next_value.
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
        self.width = field.width()
        self.height = field.height()
        # Сделаем копию, иначе переданное извне поле будет меняться
        self.field = copy.deepcopy(field)
        self.field.surround()

    def next_cell_value(self, x, y):
        """Возвращает следующее значение клетки с координатами x и y."""
        return self.next_value(self.field.neighbors(x, y))
    
    def next(self):
        """Выполняет одну итерацию клеточного автомата."""
        new_field = field.Field([[self.next_cell_value(i, j) 
                                for i in range(self.width)] 
                                    for j in range(self.height)])
        self.field = new_field
        self.field.surround()
    



if __name__ == '__main__':
    ca = CellularAutomaton()
    print
    print "Initial state of the cellular automaton:"
    print ca.field.get_inner()
    print
    print "After one iteration:"
    ca.next()
    print ca.field.get_inner()
    print
