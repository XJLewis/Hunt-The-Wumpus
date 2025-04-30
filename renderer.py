# renderer.py

import pygame
from config import TILE_SIZE, ROWS, COLS, GRAY, BLUE, WHITE

def draw_grid(win, grid, player_pos):
    win.fill(WHITE)
    for r in range(ROWS):
        for c in range(COLS):
            rect = pygame.Rect(c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(win, GRAY, rect, 1)

            if [r, c] == player_pos:
                pygame.draw.circle(win, BLUE, rect.center, TILE_SIZE//4)
