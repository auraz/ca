# -*- coding: utf-8 -*-

import pygame, sys
from ca import *

# GLOBAL CONSTANTS
PAUSE = 500    # milliseconds
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500
CANVAS_SIZE = [CANVAS_WIDTH, CANVAS_HEIGHT]
MIN = 0
MAX = 3

CA = CellularAutomaton()

# Предполагается, что это не пустой клеточный автомат, иначе будет деление на 0
CELL_WIDTH = CANVAS_WIDTH / (CA.field.width() - 2)
CELL_HEIGHT = CANVAS_HEIGHT / (CA.field.height() - 2)

running = False

pygame.init()


def draw(grid):
    """Draw the grid on the canvas"""
    for row in range(grid.height()):
        for col in range(grid.width()):
    
            level = (grid[row][col] - MIN) / (MAX - MIN) * 255
            if level < 0:
                level = 0
            if level > 255:
                level = 255
            
            pygame.draw.rect(CANVAS,
                (level, level, level),  # colour
                (CELL_WIDTH * col, CELL_HEIGHT * row, CELL_WIDTH, CELL_HEIGHT))
    
    pygame.display.update()
    # print grid


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