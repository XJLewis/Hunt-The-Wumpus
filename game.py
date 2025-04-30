import pygame
import random
import sys

# Constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 5, 5
TILE_SIZE = WIDTH // COLS
START_ARROWS = 5

# GPT gave some colors :)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hunt the Wumpus")
font = pygame.font.SysFont(None, 24)
big_font = pygame.font.SysFont(None, 40)

# States
START_SCREEN = True
GAME_OVER = False
WIN = False

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

# Start Game Loop
while True:
    if START_SCREEN:
        draw_start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
