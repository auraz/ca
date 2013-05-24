# -*- coding: utf-8 -*-

import pygame, sys, math
from ca import *

# GLOBAL CONSTANTS
PAUSE = 300.0    # milliseconds
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500
CANVAS_SIZE = [CANVAS_WIDTH, CANVAS_HEIGHT]
MIN = 0
MAX = 1

CA = CellularAutomaton()

# Предполагается, что это не пустой клеточный автомат, иначе будет деление на 0
CELL_WIDTH = math.ceil(CANVAS_WIDTH / (CA.field.width() - 2))
CELL_HEIGHT = math.ceil(CANVAS_HEIGHT / (CA.field.height() - 2))

running = False

pygame.init()


def draw(grid):
    """Draw the grid on the canvas"""
    # print grid
    for row in range(grid.height()):
        # print "new row N", row
        for col in range(grid.width()):
    
            level = (grid[row][col] - MIN) / (MAX - MIN) * 255
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

    draw(CA.field.get_inner())
    
    while True:         # Main game loop
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    CA.next()
                    draw(CA.field.get_inner())
                elif event.key == pygame.K_SPACE:
                    running = not running

        if running:
            CA.next()
            draw(CA.field.get_inner())

        # Making pause
        clock.tick(1000.0 / PAUSE)      # this is frequency, not an interval
        

finally:
    pygame.quit()