# game_state.py

from config import ROWS, COLS, NUM_PITS, NUM_BATS, START_ARROWS
from utils import random_empty_cell, is_adjacent

class GameState:
    def __init__(self):
        self.start_pos = (ROWS - 1, 0)
        self.reset()

    def reset(self):
        """Reset the game state"""
        self.grid = [["empty" for _ in range(COLS)] for _ in range(ROWS)]
        self.player_pos = list(self.start_pos)
        self.wumpus_pos = None
        self.arrows = START_ARROWS
        self.game_over = False
        self.win = False
        self.message = ""
        self.show_hazards = False  # Debug mode to show all hazards
        
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
        for _ in range(NUM_PITS):
            r, c = random_empty_cell(self.grid, [self.start_pos, self.wumpus_pos])
            self.grid[r][c] = "pit"

    def place_bats(self):
        """Place bats in random empty cells"""
        for _ in range(NUM_BATS):
            r, c = random_empty_cell(self.grid, [self.start_pos, self.wumpus_pos])
            self.grid[r][c] = "bat"

    def move_player(self, dr, dc):
        """Move the player in the specified direction"""
        if self.game_over:
            return
            
        r, c = self.player_pos
        nr, nc = r + dr, c + dc
        
        # Check if the move is valid
        if 0 <= nr < ROWS and 0 <= nc < COLS:
            self.player_pos = [nr, nc]
            self.check_hazards()
            self.get_warnings()

    def check_hazards(self):
        """Check if the player encountered any hazards"""
        r, c = self.player_pos
        cell_type = self.grid[r][c]
        
        if cell_type == "wumpus":
            self.game_over = True
            self.win = False
            self.message = "Game Over! The Wumpus got you!"
        
        elif cell_type == "pit":
            self.game_over = True
            self.win = False
            self.message = "Game Over! You fell into a pit!"
        
        elif cell_type == "bat":
            self.message = "The bats carried you to a new location!"
            # Move to a random empty cell
            new_r, new_c = random_empty_cell(self.grid)
            self.player_pos = [new_r, new_c]
            self.check_hazards()  # Check hazards again at the new location
    
    def get_warnings(self):
        """Get warnings about nearby hazards"""
        if self.game_over:
            return
            
        r, c = self.player_pos
        warnings = []
        
        # Check adjacent cells
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                cell_type = self.grid[nr][nc]
                if cell_type == "wumpus":
                    warnings.append("You smell something terrible nearby.")
                elif cell_type == "pit":
                    warnings.append("You feel a draft.")
                elif cell_type == "bat":
                    warnings.append("You hear rustling.")
        
        self.message = " ".join(warnings) if warnings else ""
    
    def shoot_arrow(self, dr, dc):
        """Shoot an arrow in the specified direction"""
        if self.game_over or self.arrows <= 0:
            return
            
        self.arrows -= 1
        
        r, c = self.player_pos
        while True:
            r += dr
            c += dc
            
            # Arrow went out of bounds
            if not (0 <= r < ROWS and 0 <= c < COLS):
                self.message = "Your arrow flies off into the darkness."
                break
                
            cell_type = self.grid[r][c]
            if cell_type == "wumpus":
                self.game_over = True
                self.win = True
                self.message = "You killed the Wumpus! You win!"
                break
        
        # Check if out of arrows
        if self.arrows <= 0 and not self.win:
            self.game_over = True
            self.message = "Game Over! You're out of arrows!"