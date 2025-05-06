# game_state.py

from config import ROWS, COLS
from utils import random_empty_cell

class GameState:
    def __init__(self):
        self.start_pos = (ROWS - 1, 0)
        self.reset()

    def reset(self):
        """Reset the game state"""
        self.grid = [["empty" for _ in range(COLS)] for _ in range(ROWS)]
        self.player_pos = list(self.start_pos)
        self.wumpus_pos = None
        
        # Player should start in an empty square
        self.grid[self.player_pos[0]][self.player_pos[1]] = "empty"
        
        # Place wumpus
        self.place_wumpus()
        
        # Place pits
        self.place_pits()
        
        # Place bats
        self.place_bats()

    def place_wumpus(self):
        """Place the wumpus in a random empty cell away from the player"""
        r, c = random_empty_cell(self.grid, [self.start_pos])
        self.wumpus_pos = (r, c)
        self.grid[r][c] = "wumpus"

    def place_pits(self):
        """Place pits in random empty cells"""
        for _ in range(2):  # Add 2 pits
            r, c = random_empty_cell(self.grid, [self.start_pos, self.wumpus_pos])
            self.grid[r][c] = "pit"

    def place_bats(self):
        """Place bats in random empty cells"""
        for _ in range(2):  # Add 2 bats
            r, c = random_empty_cell(self.grid, [self.start_pos, self.wumpus_pos])
            self.grid[r][c] = "bat"

    def move_player(self, dr, dc):
        r, c = self.player_pos
        nr, nc = r + dr, c + dc
        if 0 <= nr < ROWS and 0 <= nc < COLS:
            self.player_pos = [nr, nc]