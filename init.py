# -*- coding: utf-8 -*-

import field

"""Здесь пользователь задаёт параметры клеточного автомата.

    field - начальное состояние. Это двухмерный список.

    next_value(neighbors) - функция перехода.
    Можно выбрать одну из имеющихся функций или написать свою.
    Нужную функцию следует подставить в выражение
    next_value = ...
    в конце модуля.

    Функция должна возвращать новое значение клетки по заданным значениям
    её соседей. На вход подаётся neighbors - двухмерный список,
    содержащий значения самой клетки и всех её соседей. Сама клетка
    всегда находится по центру этого списка.

    Функция должна правильно обрабатывать пограничные случаи. Границы
    клеточного автомата обозначаются значениями None. Например, если
    neighbors содержит таблицу

    None None None
    None   1    2
    None   4    5

    , то это значит, что клетка находится в левом верхнем углу и
    содержит число 1.
    """

a = [
     [0, 0, 0, 0, 9],
     [0, 0, 0, 0, 0],
     [0, 9, 0, 0, 0],
     [0, 0, 0, 0, 0],
     [9, 0, 0, 0, 0],
     [0, 0, 9, 0, 0],
                     ]

# b = [
#      [0, 0, 0, 0,-1],
#      [0, 0, 0, 0, 0],
#      [0, 1, 0, 0, 0],
#      [0, 0, 0, 0, 0],
#      [-1,0, 0, 0, 0],
#      [0, 0, 1, 0, 0],
#                      ])

field = field.Field(a)

#or field = Field(10, 10)

def average(neighbors):
    """Среднее арифметическое всех соседей. None исключаем из расчёта."""
    n, s = 0, 0
    for row in neighbors:
        for cell in row:
            if cell is not None:
                n += 1
                s += cell
    return float(s) / n


# Подставить нужную функцию:
next_value = average
