# main.py

import pygame
import sys
from config import WIDTH, HEIGHT, ROWS, COLS, TILE_SIZE
from game_state import GameState
from renderer import draw_grid, draw_start_screen

# Initialize pygame
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT + 50))
pygame.display.set_caption("Hunt the Wumpus")

# Game states
START_SCREEN = True
game_state = GameState()

# Arrow shooting state
shooting_mode = False

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
                    game_state.show_hazards = not game_state.show_hazards
                
                # Restart game
                elif event.key == pygame.K_r and game_state.game_over:
                    game_state.reset()
                
                # Enter shooting mode
                elif event.key == pygame.K_SPACE and not shooting_mode and not game_state.game_over:
                    shooting_mode = True
                    game_state.message = "Select direction to shoot arrow"
                
                # Movement or shooting based on mode
                elif not game_state.game_over:
                    if shooting_mode:
                        if event.key == pygame.K_UP:
                            game_state.shoot_arrow(-1, 0)
                            shooting_mode = False
                        elif event.key == pygame.K_DOWN:
                            game_state.shoot_arrow(1, 0)
                            shooting_mode = False
                        elif event.key == pygame.K_LEFT:
                            game_state.shoot_arrow(0, -1)
                            shooting_mode = False
                        elif event.key == pygame.K_RIGHT:
                            game_state.shoot_arrow(0, 1)
                            shooting_mode = False
                        elif event.key == pygame.K_ESCAPE:  # Cancel shooting
                            shooting_mode = False
                            game_state.message = ""
                    else:
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