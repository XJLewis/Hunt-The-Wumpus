# main.py

import pygame
import sys
from config import WIDTH, HEIGHT, ROWS, COLS, TILE_SIZE
from game_state import GameState
from renderer import draw_grid, draw_start_screen

# Initialize pygame
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT + 50))  # Extra height for messages
pygame.display.set_caption("Hunt the Wumpus")

# Game states
START_SCREEN = True
game_state = GameState()

# Debug mode toggle
debug_mode = False

clock = pygame.time.Clock()

# Game Loop
while True:
    if START_SCREEN:
        draw_start_screen(win)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                START_SCREEN = False
                game_state.reset()
        
    else:
        draw_grid(win, game_state)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                # Toggle debug mode
                if event.key == pygame.K_d:
                    game_state.show_hazards = not game_state.showa_hazards
                
                # Restart game
                elif event.key == pygame.K_r and game_state.game_over:
                    game_state.reset()
                
                # Movement
                elif not game_state.game_over:
                    if event.key == pygame.K_UP:
                        game_state.move_player(-1, 0)
                    elif event.key == pygame.K_DOWN:
                        game_state.move_player(1, 0)
                    elif event.key == pygame.K_LEFT:
                        game_state.move_player(0, -1)
                    elif event.key == pygame.K_RIGHT:
                        game_state.move_player(0, 1)

    pygame.display.flip()
    clock.tick(30)