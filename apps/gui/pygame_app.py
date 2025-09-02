import pygame
import sys
from apps.gui.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WHITE,
    BLACK,
    PLAYER_COLORS,
    GRID_SIZE,
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


def get_sample_game_state():
    """Creates a sample game state for rendering all piece states."""
    players = [
        Player(color=PlayerColor.RED, role="Human"),
        Player(color=PlayerColor.GREEN, role="Human"),
        Player(color=PlayerColor.YELLOW, role="Human"),
        Player(color=PlayerColor.BLUE, role="Human"),
    ]

    # Red Player
    players[0].pieces[0].state = PieceState.TRACK
    players[0].pieces[0].position = 48  # On the final stretch
    players[0].pieces[1].state = PieceState.HOME_COLUMN
    players[0].pieces[1].position = 54  # Almost home
    players[0].pieces[2].state = PieceState.HOME
    # players[0].pieces[3] remains in YARD

    # Green Player
    players[1].pieces[0].state = PieceState.TRACK
    players[1].pieces[0].position = START_SQUARES[PlayerColor.GREEN] # Start square
    players[1].pieces[1].state = PieceState.TRACK
    players[1].pieces[1].position = 20 # A random track position
    # players[1].pieces[2] remains in YARD
    # players[1].pieces[3] remains in YARD

    # Yellow Player
    players[2].pieces[0].state = PieceState.TRACK
    players[2].pieces[0].position = 30
    players[2].pieces[1].state = PieceState.TRACK
    players[2].pieces[1].position = 30 # Test stacking
    players[2].pieces[2].state = PieceState.YARD
    players[2].pieces[3].state = PieceState.YARD


    # Blue Player
    players[3].pieces[0].state = PieceState.HOME
    players[3].pieces[1].state = PieceState.HOME
    players[3].pieces[2].state = PieceState.HOME
    players[3].pieces[3].state = PieceState.TRACK
    players[3].pieces[3].position = 10


    return GameState(players=players, current_player_index=0)


def draw_pieces(screen, game_state):
    """Draws the player pieces on the board."""
    piece_radius = GRID_SIZE // 2 - 4
    for player in game_state.players:
        player_color = PLAYER_COLORS[player.color.name]
        for piece in player.pieces:
            x, y = -1, -1 # Default to off-screen
            if piece.state == PieceState.YARD:
                x, y = YARD_COORDINATES[player.color][piece.id]
            elif piece.state == PieceState.TRACK:
                if 0 <= piece.position < len(TRACK_COORDINATES):
                    x, y = TRACK_COORDINATES[piece.position]
            elif piece.state == PieceState.HOME_COLUMN:
                home_pos = piece.position - 52
                if 0 <= home_pos < len(HOME_COLUMN_COORDINATES[player.color]):
                    x, y = HOME_COLUMN_COORDINATES[player.color][home_pos]
            elif piece.state == PieceState.HOME:
                # Draw in the center of the home triangle
                if player.color == PlayerColor.GREEN:
                    x, y = BOARD_X_START + GRID_SIZE * 7.5, BOARD_Y_START + GRID_SIZE * 5
                elif player.color == PlayerColor.YELLOW:
                    x, y = BOARD_X_START + GRID_SIZE * 10, BOARD_Y_START + GRID_SIZE * 7.5
                elif player.color == PlayerColor.BLUE:
                    x, y = BOARD_X_START + GRID_SIZE * 7.5, BOARD_Y_START + GRID_SIZE * 10
                elif player.color == PlayerColor.RED:
                    x, y = BOARD_X_START + GRID_SIZE * 5, BOARD_Y_START + GRID_SIZE * 7.5
                # Add a small offset for multiple pieces in home
                x += (piece.id - 1.5) * piece_radius / 2
                y += (piece.id - 1.5) * piece_radius / 2


            if x != -1 and y != -1:
                # Center the piece in the grid square
                center_x = x + GRID_SIZE // 2
                center_y = y + GRID_SIZE // 2

                # Draw piece shadow
                pygame.draw.circle(screen, (0,0,0, 50), (center_x + 2, center_y + 2), piece_radius)
                # Draw piece
                pygame.draw.circle(screen, player_color, (center_x, center_y), piece_radius)
                # Draw border
                pygame.draw.circle(screen, BLACK, (center_x, center_y), piece_radius, 2)


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


def main():
    """Main function to run the Ludo game GUI."""
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Ludo")

    game_state = get_sample_game_state()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Drawing code will go here
        screen.fill(WHITE)
        draw_board(screen)
        draw_pieces(screen, game_state)

        # Update the display
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
