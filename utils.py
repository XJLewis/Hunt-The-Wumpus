# utils.py

import random
from config import ROWS, COLS

def random_empty_cell(grid, exclude=[]):
    """Find a random empty cell that is not in the excluded list"""
    available_cells = []
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == "empty" and (r, c) not in exclude:
                available_cells.append((r, c))
    
    if not available_cells:
        return None
    
    return random.choice(available_cells)

def is_adjacent(pos1, pos2):
    """Check if two positions are adjacent"""
    r1, c1 = pos1
    r2, c2 = pos2
    
    # Check if positions are adjacent (up, down, left, right)
    return abs(r1 - r2) + abs(c1 - c2) == 1