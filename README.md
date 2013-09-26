﻿ca: Cellular automata engine for solid state physics


				Что уже сделано:


Сделана простая версия клеточного автомата.

Пользователь задаёт в модуле init:
	начальное состояние клеточного автомата (двухмерный список);
	функцию перехода.

Размер соседства фиксирован - 3 х 3 клетки (то есть данная клетка и 8 граничащих с ней клеток).

Класс CellularAutomaton умеет:
	правильно принимать то, что задал пользователь в модуле init;
	выполняють одну итерацию клеточного автомата;
	возвращать соседство заданной клетки;
	возвращать поле клеточного автомата.

Класс CellularAutomaton содержит объект типа Field. Класс Field умеет возвращать ширину, высоту и клетки из заданного диапазона.

Также есть функция, которая печатает текущее состояние клеточного автомата в виде таблицы из значений клеток.


					План

1. Переименовать класс Field в Grid. Это двухмерный список, унаследованный от List.	+

2. Реализовать класс Cell - клетку, имеющую несколько параметров (например, температура, масса, размер, тип).
	2.1 Сначала это будут фиксированные параметры.
	2.2 Позже - сделать возможность задавать параметры (их имена и количество) клеток извне (в модуле init).

3. Реализовать класс Field (унаследовав его от Grid) с методами, специфическими для клеточного автомата.	+
	3.1 Это будет двухмерный список из объектов типа Cell, по краям которого - None.	-+
	3.2 Часть методов перекочуют из класса CellularAutomaton.							+
	3.3 Также будет метод, возвращающий таблицу (Grid) из значений одного параметра.

4. Сделать визуализацию с помощью Pygame. Модуль, реализующий визуализацию, будет использовать двухмерные списки (объекты Grid).
	4.1 Сначала визуализация будет чёрно-белой и с фиксированными границами.
	4.2 Позже можно сделать настраиваемую цветовую шкалу (например, как на географической карте).
	4.3 Добавить автоопределение границ (но оставить возможность задания границ вручную).

5. Ознакомиться со следующими темами:
	5.1 Направленная кристаллизация
	5.2 Кристаллизация из расплава
	5.3 Эвтектика
Найти хотя бы по 1 математической модели каждого процесса.

6. Ознакомиться с самой физической задачей.

7. Начать решение задачи с использованием разработанного клеточного автомата. Параллельно улучшать саму программу (в частности, добавить третье измерение и соответственно изменить визуализацию).