# renderer.py

import pygame
from config import WIDTH, HEIGHT, WHITE, GRAY, BLUE, BLACK, RED, GREEN, PURPLE


def draw_game(win, game_state):
    """Draw the game and all game elements"""
    win.fill(WHITE)

    # Draw cave system
    draw_cave(win, game_state)

    # Draw UI elements
    draw_message(win, game_state.message)
    draw_arrows_count(win, game_state.arrows)

    # Draw game over message if applicable
    if game_state.game_over:
        draw_game_over(win, game_state)


def draw_cave(win, game_state):
    """Draw the cave system with dodecahedron layout"""
# Room positions - completely redesigned layout to minimize overlapping tunnels
    room_positions = [
        (WIDTH//2, HEIGHT//9),                    # 0 (top)
        (WIDTH//4, HEIGHT//4),                    # 1
        (WIDTH//7, HEIGHT//2),                    # 2
        (WIDTH//4, 3*HEIGHT//4),                  # 3
        (WIDTH//2, 8*HEIGHT//9),                  # 4 (bottom)
        (3*WIDTH//4, 3*HEIGHT//4),                # 5
        (6*WIDTH//7, HEIGHT//2),                  # 6
        (3*WIDTH//4, HEIGHT//4),                  # 7
        (3*WIDTH//5, 2*HEIGHT//7),                # 8
        (2*WIDTH//5, 2*HEIGHT//7),                # 9
        (2*WIDTH//5, 5*HEIGHT//7),                # 10
        (3*WIDTH//10, 2*HEIGHT//3),               # 11
        (WIDTH//2, 3*HEIGHT//4),                  # 12
        (7*WIDTH//10, 2*HEIGHT//3),               # 13
        (3*WIDTH//5, 5*HEIGHT//7),                # 14
        (5*WIDTH//7, 3*HEIGHT//7),                # 15
        (2*WIDTH//7, 3*HEIGHT//7),                # 16
        (WIDTH//2, 5*HEIGHT//8),                  # 17
        (WIDTH//3, 4*HEIGHT//9),                  # 18
        (2*WIDTH//3, 4*HEIGHT//9)                 # 19
    ]

    # Room radius - slightly larger for better visibility
    room_radius = 35

    # Draw tunnels first (behind rooms)
    for room_idx, connections in game_state.tunnels.items():
        x1, y1 = room_positions[room_idx]
        for connected_room in connections:
            x2, y2 = room_positions[connected_room]
            pygame.draw.line(win, BLACK, (x1, y1),
                             (x2, y2), 3)  # Thicker lines

    # Draw rooms
    for i, (x, y) in enumerate(room_positions):
        # Determine room color
        room_color = GRAY
        outline_color = BLACK
        outline_width = 2

        # Highlight player's room
        if i == game_state.player_room:
            outline_color = BLUE
            outline_width = 4
            room_color = (220, 230, 255)  # Light blue for player's room

        # Draw room (circle)
        pygame.draw.circle(win, room_color, (x, y), room_radius)
        pygame.draw.circle(win, outline_color, (x, y),
                           room_radius, outline_width)

        # Draw room number
        # Larger font for better visibility
        font = pygame.font.SysFont(None, 28)
        text = font.render(str(i), True, BLACK)
        text_rect = text.get_rect(center=(x, y))
        win.blit(text, text_rect)

        # Draw hazards if debug mode is on or game over
        if game_state.show_hazards or game_state.game_over:
            hazard_icon_size = 18  # Larger icons
            if game_state.room_contents[i] == "wumpus":
                icon_color = RED
                icon_points = [
                    (x, y - hazard_icon_size),
                    (x - hazard_icon_size, y + hazard_icon_size),
                    (x + hazard_icon_size, y + hazard_icon_size)
                ]
                pygame.draw.polygon(win, icon_color, icon_points)
            elif game_state.room_contents[i] == "pit":
                pygame.draw.circle(win, BLACK, (x, y), hazard_icon_size)
            elif game_state.room_contents[i] == "bat":
                icon_color = PURPLE
                icon_points = [
                    (x, y - hazard_icon_size),
                    (x - hazard_icon_size, y),
                    (x, y + hazard_icon_size),
                    (x + hazard_icon_size, y)
                ]
                pygame.draw.polygon(win, icon_color, icon_points)

    # Draw player
    x, y = room_positions[game_state.player_room]
    pygame.draw.circle(win, BLUE, (x, y), 15)  # Larger player marker

    # Draw possible moves
    for i, connected_room in enumerate(
    game_state.tunnels[game_state.player_room]):
        x, y = room_positions[connected_room]
        move_color = GREEN
        pygame.draw.circle(win, move_color, (x, y), 8)  # Larger move markers

        # Draw tunnel number for arrow shooting
        mid_x = (room_positions[game_state.player_room][0] + x) // 2
        mid_y = (room_positions[game_state.player_room][1] + y) // 2
        tunnel_font = pygame.font.SysFont(None, 24)  # Larger font
        tunnel_text = tunnel_font.render(
            str(i + 1), True, RED)  # Add 1 to display as 1-3

        # Add a small background circle for better visibility of numbers
        bg_radius = 12
        pygame.draw.circle(win, WHITE, (mid_x, mid_y), bg_radius)
        pygame.draw.circle(win, BLACK, (mid_x, mid_y), bg_radius, 1)

        win.blit(tunnel_text, (mid_x - 6, mid_y - 8))


def draw_message(win, message):
    """Draw message at the bottom of the screen"""
    if not message:
        return

    message_bg = pygame.Rect(10, HEIGHT + 5, WIDTH - 20, 40)
    pygame.draw.rect(win, (240, 240, 240), message_bg)
    pygame.draw.rect(win, BLACK, message_bg, 2)

    font = pygame.font.SysFont(None, 24)
    text = font.render(message, True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT + 25))
    win.blit(text, text_rect)


def draw_arrows_count(win, arrows):
    """Draw arrow count at the bottom of the screen"""
    font = pygame.font.SysFont(None, 24)
    text = font.render(f"Arrows: {arrows}", True, BLACK)
    win.blit(text, (WIDTH - 120, HEIGHT + 10))


def draw_game_over(win, game_state):
    """Draw game over screen"""
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    win.blit(overlay, (0, 0))

    font = pygame.font.SysFont(None, 60)  # Larger font
    if game_state.win:
        text = font.render("YOU WIN!", True, GREEN)
    else:
        text = font.render("GAME OVER", True, RED)

    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    win.blit(text, text_rect)

    font = pygame.font.SysFont(None, 30)  # Larger font
    message = font.render(game_state.message, True, WHITE)
    message_rect = message.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    win.blit(message, message_rect)

    restart = font.render("Press R to restart", True, WHITE)
    restart_rect = restart.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    win.blit(restart, restart_rect)


def draw_start_screen(win):
    """Draw the start screen"""
    win.fill(WHITE)
    font_title = pygame.font.SysFont(None, 60)  # Larger title
    font = pygame.font.SysFont(None, 28)  # Larger font

    title = font_title.render("HUNT THE WUMPUS", True, BLACK)
    title_rect = title.get_rect(center=(WIDTH // 2, 100))
    win.blit(title, title_rect)

    # Create a background for instructions
    instructions_bg = pygame.Rect(WIDTH//4, 150, WIDTH//2, 350)
    pygame.draw.rect(win, (240, 240, 240), instructions_bg)
    pygame.draw.rect(win, BLACK, instructions_bg, 2)

    lines = [
        "You are a hunter in a cave with 20 rooms connected by tunnels.",
        "Your goal is to kill the Wumpus without dying.",
        "",
        "Watch out for:",
        "- The Wumpus (you'll smell it nearby)",
        "- Bottomless Pits (you'll feel a draft nearby)",
        "- Giant Bats (you'll hear rustling nearby)",
        "",
        "Press 1-3 to move through tunnels",  # Updated from 0-2 to 1-3
        "SPACE + tunnel numbers (1-3) - Shoot arrow through paths",
        "D - Toggle debug mode",
        "",
        "Press ENTER to begin"
    ]

    for i, line in enumerate(lines):
        text = font.render(line, True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, 180 + i * 25))
        win.blit(text, text_rect)


def draw_shooting_instructions(win):
    """Draw instructions for shooting an arrow"""
    instruction_bg = pygame.Rect(10, HEIGHT + 5, WIDTH - 20, 40)
    # Light red background
    pygame.draw.rect(win, (255, 240, 240), instruction_bg)
    pygame.draw.rect(win, RED, instruction_bg, 2)

    font = pygame.font.SysFont(None, 24)
    text = font.render(
        "Enter your tunnel number for arrow path, then press ENTER",
        True,
        BLACK
    )
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT + 25))
    win.blit(text, text_rect)
