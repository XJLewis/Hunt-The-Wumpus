# main.py

import pygame
import sys
from config import WIDTH, HEIGHT, WHITE, BLACK, START_ARROWS
from game_state import GameState
from renderer import draw_grid

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hunt the Wumpus")
font = pygame.font.SysFont(None, 24)

START_SCREEN = True
game_state = GameState()

def draw_start_screen():
    win.fill(WHITE)
    lines = [
        "HUNT THE WUMPUS",
        "",
        "Arrow Keys - Move",
        f"SPACE + Arrow Key - Shoot arrow (you have {START_ARROWS})",
        "",
        "Avoid hazards and shoot the Wumpus!",
        "",
        "Press ENTER to begin"
    ]
    for i, line in enumerate(lines):
        txt = font.render(line, True, BLACK)
        win.blit(txt, (40, 60 + i * 30))
    pygame.display.flip()

clock = pygame.time.Clock()

# Game Loop
while True:
    if START_SCREEN:
        draw_start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                START_SCREEN = False
        continue

    draw_grid(win, game_state.grid, game_state.player_pos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
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
