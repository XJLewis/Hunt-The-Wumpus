# renderer.py

import pygame
from config import TILE_SIZE, ROWS, COLS, WHITE, GRAY, BLUE, BLACK, RED, GREEN, YELLOW, BROWN, PURPLE

def draw_grid(win, game_state):
    """Draw the game grid and all game elements"""
    win.fill(WHITE)
    grid = game_state.grid
    player_pos = game_state.player_pos
    
    # Draw grid cells
    for r in range(ROWS):
        for c in range(COLS):
            rect = pygame.Rect(c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(win, GRAY, rect, 1)
            
            # Draw hazards if debug mode is on
            if game_state.show_hazards or game_state.game_over:
                cell_type = grid[r][c]
                if cell_type == "wumpus":
                    pygame.draw.polygon(win, RED, [
                        (rect.centerx, rect.top + 10),
                        (rect.left + 10, rect.bottom - 10),
                        (rect.right - 10, rect.bottom - 10)
                    ])
                elif cell_type == "pit":
                    pygame.draw.circle(win, BLACK, rect.center, TILE_SIZE//3)
                elif cell_type == "bat":
                    pygame.draw.polygon(win, PURPLE, [
                        (rect.centerx, rect.top + 10),
                        (rect.left + 10, rect.centery),
                        (rect.centerx, rect.bottom - 10),
                        (rect.right - 10, rect.centery)
                    ])
    
    # Draw player
    player_rect = pygame.Rect(player_pos[1]*TILE_SIZE, player_pos[0]*TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.circle(win, BLUE, player_rect.center, TILE_SIZE//4)
    
    # Draw UI elements
    draw_message(win, game_state.message)
    draw_arrows_count(win, game_state.arrows)
    
    # Draw game over message if applicable
    if game_state.game_over:
        draw_game_over(win, game_state)

def draw_message(win, message):
    """Draw message at the bottom of the screen"""
    if not message:
        return
        
    font = pygame.font.SysFont(None, 24)
    text = font.render(message, True, BLACK)
    win.blit(text, (20, ROWS * TILE_SIZE + 10))

def draw_arrows_count(win, arrows):
    """Draw arrow count at the bottom of the screen"""
    font = pygame.font.SysFont(None, 24)
    text = font.render(f"Arrows: {arrows}", True, BLACK)
    win.blit(text, (COLS * TILE_SIZE - 120, ROWS * TILE_SIZE + 10))

def draw_game_over(win, game_state):
    """Draw game over screen"""
    overlay = pygame.Surface((COLS * TILE_SIZE, ROWS * TILE_SIZE))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    win.blit(overlay, (0, 0))
    
    font = pygame.font.SysFont(None, 48)
    if game_state.win:
        text = font.render("YOU WIN!", True, GREEN)
    else:
        text = font.render("GAME OVER", True, RED)
    
    text_rect = text.get_rect(center=(COLS * TILE_SIZE // 2, ROWS * TILE_SIZE // 2 - 50))
    win.blit(text, text_rect)
    
    font = pygame.font.SysFont(None, 24)
    message = font.render(game_state.message, True, WHITE)
    message_rect = message.get_rect(center=(COLS * TILE_SIZE // 2, ROWS * TILE_SIZE // 2))
    win.blit(message, message_rect)
    
    restart = font.render("Press R to restart", True, WHITE)
    restart_rect = restart.get_rect(center=(COLS * TILE_SIZE // 2, ROWS * TILE_SIZE // 2 + 50))
    win.blit(restart, restart_rect)

def draw_start_screen(win):
    """Draw the start screen"""
    win.fill(WHITE)
    font_title = pygame.font.SysFont(None, 48)
    font = pygame.font.SysFont(None, 24)
    
    title = font_title.render("HUNT THE WUMPUS", True, BLACK)
    title_rect = title.get_rect(center=(COLS * TILE_SIZE // 2, 100))
    win.blit(title, title_rect)
    
    lines = [
        "You are a hunter in a cave with 5x5 rooms.",
        "Your goal is to kill the Wumpus without dying.",
        "",
        "Watch out for:",
        "- The Wumpus (you'll smell it nearby)",
        "- Bottomless Pits (you'll feel a draft nearby)",
        "- Bats (you'll hear rustling nearby)",
        "",
        "Arrow Keys - Move",
        "SPACE + Arrow Key - Shoot arrow",
        "",
        "Press ENTER to begin"
    ]
    
    for i, line in enumerate(lines):
        text = font.render(line, True, BLACK)
        text_rect = text.get_rect(center=(COLS * TILE_SIZE // 2, 150 + i * 25))
        win.blit(text, text_rect)