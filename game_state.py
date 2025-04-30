# game_state.py

from config import ROWS, COLS
from utils import random_empty_cell

class GameState:
    def __init__(self):
        self.start_pos = (ROWS - 1, 0)
        self.reset()

    def reset(self):
        self.grid = [["empty" for _ in range(COLS)] for _ in range(ROWS)]
        self.player_pos = list(self.start_pos)

    def move_player(self, dr, dc):
        r, c = self.player_pos
        nr, nc = r + dr, c + dc
        if 0 <= nr < ROWS and 0 <= nc < COLS:
            self.player_pos = [nr, nc]
