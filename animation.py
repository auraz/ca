# -*- coding: utf-8 -*-

"""Визуализация клеточного автомата.

    Клавиша Enter - одна итерация,
    Spase - запустить/остановить анимацию
"""

import pygame, sys, math
from ca import *

# GLOBAL CONSTANTS
TIMER_INTERVAL = 250    # интервал между итерациями в миллисекундах
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500
CANVAS_SIZE = [CANVAS_WIDTH, CANVAS_HEIGHT]
MIN = 0     # black
MAX = 1     # white

CA = CellularAutomaton()

# Предполагается, что это не пустой клеточный автомат, иначе будет деление на 0
CELL_WIDTH = math.ceil(CANVAS_WIDTH / (CA.field.width() - 2.0))
CELL_HEIGHT = math.ceil(CANVAS_HEIGHT / (CA.field.height() - 2.0))

running = False

print "Press Enter to make one iteration"
print "or press Spase to start/stop animation."

pygame.init()


def draw(grid):
    """Draw the grid on the canvas"""
    # print grid
    for row in range(grid.height()):
        # print "new row N", row
        for col in range(grid.width()):
    
            level = (grid[row][col] - MIN) / (MAX - MIN + 0.0) * 255
            # print "cell =", grid[row][col], "level =", level,
            if level < 0:
                level = 0
            if level > 255:
                level = 255
            
            pygame.draw.rect(CANVAS,
                (level, level, level),  # colour
                (CELL_WIDTH * col, CELL_HEIGHT * row, CELL_WIDTH, CELL_HEIGHT))
    
    pygame.display.update()


CANVAS = pygame.display.set_mode(CANVAS_SIZE)
pygame.display.set_caption('Cellular Automaton Visualisation')

try:
    clock = pygame.time.Clock()
    TIMER = pygame.USEREVENT
    pygame.time.set_timer(TIMER, TIMER_INTERVAL)

    draw(CA.field.get_inner())

    # Main loop
    while True:
        # Рисование происходит не в каждой итерацию этого цикла,
        # а только по нажатию Enter или по срабатыванию таймера.

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:    # make one iteration of CA
                    CA.next()
                    draw(CA.field.get_inner())
                elif event.key == pygame.K_SPACE:   # start/stop animation
                    running = not running
            
            elif event.type == TIMER:
                if running:
                    CA.next()
                    draw(CA.field.get_inner())

        # Making pause
        clock.tick(20)      # this is frequency, not an interval

finally:
    pygame.quit()