# renderer.py

import pygame
from config import TILE_SIZE, ROWS, COLS, GRAY, BLUE, WHITE, RED, BLACK, PURPLE

def draw_grid(win, grid, player_pos):
    win.fill(WHITE)
    
    # Draw grid cells and hazards
    for r in range(ROWS):
        for c in range(COLS):
            rect = pygame.Rect(c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(win, GRAY, rect, 1)
            
            # Draw hazards (visible for debugging)
            cell_type = grid[r][c]
            if cell_type == "wumpus":
                pygame.draw.polygon(win, RED, [
                    (rect.centerx, rect.top + 10),
                    (rect.left + 10, rect.bottom - 10),
                    (rect.right - 10, rect.bottom - 10)
                ])
            elif cell_type == "pit":
                pygame.draw.circle(win, BLACK, rect.center, TILE_SIZE//3)
            elif cell_type == "bat":
                pygame.draw.polygon(win, PURPLE, [
                    (rect.centerx, rect.top + 10),
                    (rect.left + 10, rect.centery),
                    (rect.centerx, rect.bottom - 10),
                    (rect.right - 10, rect.centery)
                ])

    # Draw player
    player_rect = pygame.Rect(player_pos[1]*TILE_SIZE, player_pos[0]*TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.circle(win, BLUE, player_rect.center, TILE_SIZE//4)