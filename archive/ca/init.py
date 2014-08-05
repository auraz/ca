# -*- coding: utf-8 -*-

import field
import random
from math import *

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

# левый код, который я хочу не только закомментировать, но и зафолдить,
# чтобы не мешал
    
    # a = [
    #      [0, 0, 0, 0, 9],
    #      [0, 0, 0, 0, 0],
    #      [0, 9, 0, 0, 0],
    #      [0, 0, 0, 0, 0],
    #      [9, 0, 0, 0, 0],
    #      [0, 0, 9, 0, 0],
    #                      ]

    # b = [
    #      [0, 0, 0, 0, 0],
    #      [0, 0, 0, 0, 0],
    #      [0, 0, 1, 0, 0],
    #      [0, 0, -1,0, 0],
    #      [0, 0, 0, 0, 0],
    #      [0, 0, 0, 0, 0],
    #                      ]

c = [[0 for i in range(130)] for i in range(100)]
c[51][62], c[51][63], c[52][61], c[52][62], c[53][62] = 1, 1, 1, 1, 1
# c[1][2], c[2][3], c[3][3], c[3][2], c[3][1] = 1, 1, 1, 1, 1
    # Это выглядит так:
    # 0 0 0 0 0 ...
    # 0 0 1 0 0 ...
    # 0 0 0 1 0 ...
    # 0 1 1 1 0 ...
    # 0 0 0 0 0 ...
    # ...  ...  ...
    #
    # Или так:
    #
    #     *
    #       *
    #   * * *
    #

# дальше - по заданию

# def is_any_nucleus_near(x, y, f, n, r):
#     """Проверяет, нет ли зародыша (единички) около заданной клетки.

#         x, y - координаты клетки
#         f - поле (точнее, квадратный двухмерный список)
#         n - его размер
#         r - расстояние, в пределах которого не должно быть зародыша
#         """

#     x1 = max(x - r, 0)
#     y1 = max(y - r, 0)
#     x2 = min(x + r + 1, n)
#     y2 = min(y + r + 1, n)
#     for i in range(x1, x2):
#         for j in range(y1, y2):
#             if f[j][i] == 1:
#                 return True
#     return False

# n = 100
# r = 8
# count = 0
# f = [[0 for i in range(n)] for i in range(n)]   # заполняем нулями

# for i in range(500000):
#     x, y = random.randrange(n), random.randrange(n)
#     if not is_any_nucleus_near(x, y, f, n, r):
#         f[y][x] = 1
#         count += 1

field = field.Field(c)
# print count, 'nuclei'
# print field

def average(neighbors):
    """Среднее арифметическое всех соседей. None исключаем из расчёта."""
    n, s = 0, 0
    for row in neighbors:
        for cell in row:
            if cell is not None:
                n += 1
                s += cell
    return float(s) / n

def sum(neighbors):
    """Сумма всех соседей. None исключаем из расчёта."""
    s = 0
    for row in neighbors:
        for cell in row:
            if cell is not None:
                s += cell
    return s


def life(neighbors):
    """Conway's Game of Life"""
    cell = neighbors[1][1]
    s = sum(neighbors) - cell
    if cell == 0:
        if s == 3:
            return 1
        else:
            return 0
    else:
        if s == 2 or s == 3:
            return 1
        else:
            return 0




# Подставить нужную функцию:
next_value = life
