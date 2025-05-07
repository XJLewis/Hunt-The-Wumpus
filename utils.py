# utils.py

import random

def random_empty_cell(grid, exclude=[]):
    """Find a random empty cell that is not in the excluded list"""
    # This is a utility function kept from the grid-based version
    # In our tunnel-based version it is not used, but included for reference
    return None

def is_adjacent(pos1, pos2):
    """Check if two positions are adjacent"""
    r1, c1 = pos1
    r2, c2 = pos2
    
    # Check if positions are adjacent (up, down, left, right)
    return abs(r1 - r2) + abs(c1 - c2) == 1