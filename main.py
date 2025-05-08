# main.py

import pygame
import sys
from config import WIDTH, HEIGHT
from game_state import GameState
from renderer import draw_game, draw_start_screen, draw_shooting_instructions

# Initialize pygame
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT + 50))
pygame.display.set_caption("Hunt the Wumpus")

# Game states
START_SCREEN = True
game_state = GameState()

# Arrow shooting state
shooting_mode = False
arrow_path = []

clock = pygame.time.Clock()

# Game Loop
while True:
    if START_SCREEN:
        draw_start_screen(win)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_RETURN
            ):
                START_SCREEN = False
                game_state.reset()

    else:
        draw_game(win, game_state)
        if shooting_mode:
            draw_shooting_instructions(win)

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
                    shooting_mode = False
                    arrow_path = []

                # Enter shooting mode
                elif (
                    event.key == pygame.K_SPACE
                    and not shooting_mode
                    and not game_state.game_over
                ):
                    shooting_mode = True
                    arrow_path = []
                    game_state.message = (
                        "Select tunnels for arrow path (up to 3)"
                    )

                # Handle arrow shooting inputs
                elif shooting_mode:
                    if event.key == pygame.K_RETURN:
                        # Shoot arrow when Enter is pressed
                        if arrow_path:
                            game_state.shoot_arrow(arrow_path)
                            shooting_mode = False
                            arrow_path = []
                    elif event.key == pygame.K_ESCAPE:
                        # Cancel shooting
                        shooting_mode = False
                        arrow_path = []
                        game_state.message = ""
                    elif pygame.K_1 <= event.key <= pygame.K_3:
                        # Add tunnel to path (limit to 3 as in original game)
                        tunnel_idx = event.key - pygame.K_1
                        if len(arrow_path) < 3:
                            arrow_path.append(tunnel_idx)
                            game_state.message = (
                                f"Arrow path: {arrow_path}"
                            )

                # Movement (if not in shooting mode)
                elif not game_state.game_over and not shooting_mode:
                    if pygame.K_1 <= event.key <= pygame.K_3:
                        tunnel_idx = event.key - pygame.K_1
                        game_state.move_player(tunnel_idx)

    pygame.display.flip()
    clock.tick(30)
