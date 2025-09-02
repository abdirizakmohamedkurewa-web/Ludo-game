import pygame
import sys
from apps.gui.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WHITE,
    BLACK,
    PLAYER_COLORS,
    GRID_SIZE,
    LIGHT_GRAY,
)
from apps.gui.board_layout import (
    TRACK_COORDINATES,
    HOME_COLUMN_COORDINATES,
    YARD_COORDINATES,
    BOARD_X_START,
    BOARD_Y_START,
    GRID_COUNT
)
from ludo.state import GameState
from ludo.player import Player
from ludo.piece import Piece
from ludo.utils.constants import PlayerColor, PieceState
from ludo.board import START_SQUARES, SAFE_SQUARES
from ludo.game import Game
from ludo.dice import Dice
from ludo.bots.human_bot import HumanBot
from ludo.rules import Rules
from ludo.move import move_piece


def get_pos_pixel_coords(color, position):
    """Calculates the pixel coordinates for a given board position index."""
    if 0 <= position < 52: # Main track
        return TRACK_COORDINATES[position]
    elif 52 <= position < 58: # Home column
        home_pos = position - 52
        if 0 <= home_pos < len(HOME_COLUMN_COORDINATES[color]):
            return HOME_COLUMN_COORDINATES[color][home_pos]
    return None # For YARD or HOME state, which don't have a single destination square

def get_piece_pixel_pos(player, piece):
    """Calculates the pixel position (center) of a given piece."""
    if piece.state == PieceState.YARD:
        x, y = YARD_COORDINATES[player.color][piece.id]
    elif piece.state in (PieceState.TRACK, PieceState.HOME_COLUMN):
        coords = get_pos_pixel_coords(player.color, piece.position)
        if coords is None:
            return None
        x, y = coords
    elif piece.state == PieceState.HOME:
        # Simplified for now, can be improved
        if player.color == PlayerColor.GREEN:
            x, y = BOARD_X_START + GRID_SIZE * 7.5, BOARD_Y_START + GRID_SIZE * 5
        elif player.color == PlayerColor.YELLOW:
            x, y = BOARD_X_START + GRID_SIZE * 10, BOARD_Y_START + GRID_SIZE * 7.5
        elif player.color == PlayerColor.BLUE:
            x, y = BOARD_X_START + GRID_SIZE * 7.5, BOARD_Y_START + GRID_SIZE * 10
        else: # RED
            x, y = BOARD_X_START + GRID_SIZE * 5, BOARD_Y_START + GRID_SIZE * 7.5
        piece_radius = GRID_SIZE // 2 - 4
        x += (piece.id - 1.5) * piece_radius / 2
        y += (piece.id - 1.5) * piece_radius / 2
    else:
        return None

    return x + GRID_SIZE // 2, y + GRID_SIZE // 2


def draw_pieces(screen, game_state, legal_moves, selected_piece):
    """Draws the player pieces on the board."""
    piece_radius = GRID_SIZE // 2 - 4
    movable_pieces = [move[0] for move in legal_moves]

    for player in game_state.players:
        player_color = PLAYER_COLORS[player.color.name]
        for piece in player.pieces:
            pos = get_piece_pixel_pos(player, piece)
            if pos:
                center_x, center_y = pos
                # Draw piece shadow
                pygame.draw.circle(screen, (0,0,0, 50), (center_x + 2, center_y + 2), piece_radius)
                # Draw piece
                pygame.draw.circle(screen, player_color, (center_x, center_y), piece_radius)
                # Draw border
                pygame.draw.circle(screen, BLACK, (center_x, center_y), piece_radius, 2)

                # Highlight if it's a legal move
                if piece in movable_pieces:
                    highlight_color = (255, 255, 0, 150) # Yellow highlight
                    pygame.draw.circle(screen, highlight_color, (center_x, center_y), piece_radius, 4)

                # Highlight if selected
                if piece == selected_piece:
                    pygame.draw.circle(screen, (0, 255, 255), (center_x, center_y), piece_radius + 2, 3)


def draw_legal_move_highlights(screen, game, selected_piece, legal_moves):
    """Draws highlights for the possible destination squares of a selected piece."""
    if not selected_piece:
        return

    highlight_color = (0, 255, 255, 100) # Cyan, semi-transparent

    for piece, destination in legal_moves:
        if piece.id == selected_piece.id:
            player_color = game.state.players[game.state.current_player_index].color
            coords = get_pos_pixel_coords(player_color, destination)
            if coords:
                highlight_rect = pygame.Rect(coords[0], coords[1], GRID_SIZE, GRID_SIZE)
                # Use a surface to draw with alpha transparency
                s = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
                s.fill(highlight_color)
                screen.blit(s, highlight_rect.topleft)

def draw_board(screen):
    """Draws the Ludo board layout."""
    # --- 1. Draw Yards ---
    yard_size = GRID_SIZE * 6
    # GREEN
    pygame.draw.rect(screen, PLAYER_COLORS["GREEN"], (BOARD_X_START, BOARD_Y_START, yard_size, yard_size))
    # YELLOW
    pygame.draw.rect(screen, PLAYER_COLORS["YELLOW"], (BOARD_X_START + GRID_SIZE * 9, BOARD_Y_START, yard_size, yard_size))
    # BLUE
    pygame.draw.rect(screen, PLAYER_COLORS["BLUE"], (BOARD_X_START + GRID_SIZE * 9, BOARD_Y_START + GRID_SIZE * 9, yard_size, yard_size))
    # RED
    pygame.draw.rect(screen, PLAYER_COLORS["RED"], (BOARD_X_START, BOARD_Y_START + GRID_SIZE * 9, yard_size, yard_size))

    # Inner Yard circles
    pygame.draw.circle(screen, WHITE, (BOARD_X_START + yard_size / 2, BOARD_Y_START + yard_size / 2), yard_size / 2 - GRID_SIZE, 5)
    pygame.draw.circle(screen, WHITE, (BOARD_X_START + GRID_SIZE * 9 + yard_size / 2, BOARD_Y_START + yard_size / 2), yard_size / 2 - GRID_SIZE, 5)
    pygame.draw.circle(screen, WHITE, (BOARD_X_START + GRID_SIZE * 9 + yard_size / 2, BOARD_Y_START + GRID_SIZE * 9 + yard_size / 2), yard_size / 2 - GRID_SIZE, 5)
    pygame.draw.circle(screen, WHITE, (BOARD_X_START + yard_size / 2, BOARD_Y_START + GRID_SIZE * 9 + yard_size / 2), yard_size / 2 - GRID_SIZE, 5)


    # --- 2. Draw Track Squares ---
    for i, (x, y) in enumerate(TRACK_COORDINATES):
        # Default square is white
        color = WHITE
        # Color the start squares
        if i == START_SQUARES[PlayerColor.RED]:
            color = PLAYER_COLORS["RED"]
        elif i == START_SQUARES[PlayerColor.GREEN]:
            color = PLAYER_COLORS["GREEN"]
        elif i == START_SQUARES[PlayerColor.YELLOW]:
            color = PLAYER_COLORS["YELLOW"]
        elif i == START_SQUARES[PlayerColor.BLUE]:
            color = PLAYER_COLORS["BLUE"]

        pygame.draw.rect(screen, color, (x, y, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, BLACK, (x, y, GRID_SIZE, GRID_SIZE), 1) # Black border

        # Highlight safe squares with a star
        if i in SAFE_SQUARES and i not in START_SQUARES.values():
            center_x, center_y = x + GRID_SIZE // 2, y + GRID_SIZE // 2
            pygame.draw.circle(screen, BLACK, (center_x, center_y), 5)


    # --- 3. Draw Home Columns ---
    for color, coords in HOME_COLUMN_COORDINATES.items():
        player_color = PLAYER_COLORS[color.name]
        for i, (x, y) in enumerate(coords):
            pygame.draw.rect(screen, player_color, (x, y, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BLACK, (x, y, GRID_SIZE, GRID_SIZE), 1) # Black border

    # --- 4. Draw Home Triangle ---
    center_x = BOARD_X_START + GRID_SIZE * GRID_COUNT / 2
    center_y = BOARD_Y_START + GRID_SIZE * GRID_COUNT / 2
    home_points = [
        (BOARD_X_START + GRID_SIZE * 6, BOARD_Y_START + GRID_SIZE * 6),
        (BOARD_X_START + GRID_SIZE * 9, BOARD_Y_START + GRID_SIZE * 6),
        (center_x, center_y),
        (BOARD_X_START + GRID_SIZE * 9, BOARD_Y_START + GRID_SIZE * 9),
        (BOARD_X_START + GRID_SIZE * 6, BOARD_Y_START + GRID_SIZE * 9),
        (center_x, center_y),
    ]
    # Draw four triangles pointing to the center
    pygame.draw.polygon(screen, PLAYER_COLORS["GREEN"], [home_points[0], home_points[1], (center_x, center_y)])
    pygame.draw.polygon(screen, PLAYER_COLORS["YELLOW"], [(home_points[1]), (home_points[3]), (center_x, center_y)])
    pygame.draw.polygon(screen, PLAYER_COLORS["BLUE"], [(home_points[3]), (home_points[4]), (center_x, center_y)])
    pygame.draw.polygon(screen, PLAYER_COLORS["RED"], [(home_points[4]), (home_points[0]), (center_x, center_y)])
    pygame.draw.rect(screen, BLACK, (BOARD_X_START + GRID_SIZE * 6, BOARD_Y_START + GRID_SIZE * 6, GRID_SIZE * 3, GRID_SIZE * 3), 1)


def draw_info_panel(screen, game, font, ui_buttons):
    """Draws the UI panel with game state information."""
    panel_x = BOARD_X_START + GRID_SIZE * GRID_COUNT + 20
    panel_y = BOARD_Y_START
    panel_width = SCREEN_WIDTH - panel_x - 20
    panel_height = GRID_SIZE * GRID_COUNT

    # Panel Background
    pygame.draw.rect(screen, LIGHT_GRAY, (panel_x, panel_y, panel_width, panel_height))

    # --- 1. Display Current Player ---
    current_player = game.state.players[game.state.current_player_index]
    player_color_name = current_player.color.name
    player_color_rgb = PLAYER_COLORS[player_color_name]

    turn_text_surf = font.render(f"{player_color_name}'s Turn", True, BLACK)
    screen.blit(turn_text_surf, (panel_x + 20, panel_y + 20))
    pygame.draw.circle(screen, player_color_rgb, (panel_x + panel_width - 40, panel_y + 40), 15)
    pygame.draw.circle(screen, BLACK, (panel_x + panel_width - 40, panel_y + 40), 15, 2)


    # --- 2. Display Dice Roll ---
    dice_text = "Roll the dice!"
    if game.state.dice_roll is not None:
        dice_text = f"Rolled a: {game.state.dice_roll}"

    dice_surf = font.render(dice_text, True, BLACK)
    screen.blit(dice_surf, (panel_x + 20, panel_y + 80))

    # --- 3. "Roll Dice" Button ---
    roll_button_rect = pygame.Rect(panel_x + 20, panel_y + 140, panel_width - 40, 50)
    ui_buttons["roll_dice"] = roll_button_rect # Store for click detection

    pygame.draw.rect(screen, PLAYER_COLORS["GREEN"], roll_button_rect)
    roll_text_surf = font.render("Roll Dice", True, BLACK)
    text_rect = roll_text_surf.get_rect(center=roll_button_rect.center)
    screen.blit(roll_text_surf, text_rect)


def main():
    """Main function to run the Ludo game GUI."""
    pygame.init()
    font = pygame.font.SysFont("Arial", 24)
    ui_buttons = {} # To store rects of UI elements for interaction

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Ludo")

    # --- Game Initialization ---
    dice = Dice()
    players = [
        Player(color=PlayerColor.RED, role="human"),
        Player(color=PlayerColor.GREEN, role="human"),
        Player(color=PlayerColor.YELLOW, role="human"),
        Player(color=PlayerColor.BLUE, role="human"),
    ]
    strategies = [HumanBot(), HumanBot(), HumanBot(), HumanBot()]
    game = Game(players=players, strategies=strategies, dice=dice)

    # Game loop variables
    legal_moves = []
    selected_piece = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 1. Handle Roll Dice Button Click
                if ui_buttons.get("roll_dice") and ui_buttons["roll_dice"].collidepoint(event.pos):
                    if game.state.dice_roll is None:
                        roll = game.dice.roll()
                        game.state.dice_roll = roll
                        legal_moves = Rules.get_legal_moves(game.state, roll)
                        selected_piece = None # Reset selection on new roll
                        print(f"Player rolled a {roll}. Legal moves: {[(m[0].id, m[1]) for m in legal_moves]}")

                # 2. Handle Piece Selection
                elif game.state.dice_roll is not None and legal_moves:
                    current_player = game.state.players[game.state.current_player_index]
                    movable_pieces = [move[0] for move in legal_moves]
                    for piece in current_player.pieces:
                        if piece in movable_pieces:
                            pos = get_piece_pixel_pos(current_player, piece)
                            if pos:
                                piece_radius = GRID_SIZE // 2 - 4
                                if pygame.Rect(pos[0]-piece_radius, pos[1]-piece_radius, piece_radius*2, piece_radius*2).collidepoint(event.pos):
                                    selected_piece = piece
                                    print(f"Selected piece {piece.id}")
                                    break # Select only one piece

        # Drawing code will go here
        screen.fill(WHITE)
        draw_board(screen)
        draw_legal_move_highlights(screen, game, selected_piece, legal_moves)
        draw_pieces(screen, game.state, legal_moves, selected_piece)
        draw_info_panel(screen, game, font, ui_buttons)

        # Update the display
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
