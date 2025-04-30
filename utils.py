# utils.py

import random
from config import ROWS, COLS

def random_empty_cell(grid, exclude=[]):
    while True:
        r, c = random.randint(0, ROWS-1), random.randint(0, COLS-1)
        if grid[r][c] == "empty" and (r, c) not in exclude:
            return r, c
