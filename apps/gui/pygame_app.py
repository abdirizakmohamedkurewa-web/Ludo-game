import pygame
import sys
from apps.gui.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WHITE,
    PLAYER_COLORS,
    GRID_SIZE,
    BOARD_MARGIN,
)
from ludo.state import GameState
from ludo.player import Player
from ludo.piece import Piece
from ludo.utils.constants import PlayerColor, PieceState


def get_sample_game_state():
    """Creates a sample game state for rendering."""
    players = [
        Player(color=PlayerColor.RED),
        Player(color=PlayerColor.GREEN),
        Player(color=PlayerColor.YELLOW),
        Player(color=PlayerColor.BLUE),
    ]
    players[0].pieces[0].state = PieceState.TRACK
    players[0].pieces[0].position = 5
    players[1].pieces[0].state = PieceState.TRACK
    players[1].pieces[0].position = 20
    players[2].pieces[0].state = PieceState.HOME
    return GameState(players=players)


def draw_pieces(screen, game_state):
    # This is a simplified example. A more robust implementation would
    # map all 52 track positions to coordinates.
    for player in game_state.players:
        for piece in player.pieces:
            color = PLAYER_COLORS[player.color.name]
            if piece.state == PieceState.YARD:
                # Simplified yard positioning
                if player.color == PlayerColor.GREEN:
                    pygame.draw.circle(screen, color, (150, 150), 15)
                elif player.color == PlayerColor.RED:
                    pygame.draw.circle(screen, color, (650, 150), 15)
                elif player.color == PlayerColor.YELLOW:
                    pygame.draw.circle(screen, color, (150, 650), 15)
                elif player.color == PlayerColor.BLUE:
                    pygame.draw.circle(screen, color, (650, 650), 15)

            elif piece.state == PieceState.TRACK:
                # Super simplified track positioning for the example
                if piece.position < 13:
                     pygame.draw.circle(screen, color, (400 + piece.position * 20, 100), 15)
                else:
                     pygame.draw.circle(screen, color, (400, 200 + piece.position * 10), 15)

            elif piece.state == PieceState.HOME:
                pygame.draw.circle(screen, color, (400, 400), 20)  # Center for home


def draw_board(screen):
    """Draws the Ludo board."""
    # Define board areas
    board_size = SCREEN_WIDTH - 2 * BOARD_MARGIN
    yard_size = board_size / 3 * 1.25
    track_width = board_size / 3 * 0.75

    # Draw yards
    pygame.draw.rect(screen, PLAYER_COLORS["GREEN"], (BOARD_MARGIN, BOARD_MARGIN, yard_size, yard_size))
    pygame.draw.rect(screen, PLAYER_COLORS["RED"], (SCREEN_WIDTH - BOARD_MARGIN - yard_size, BOARD_MARGIN, yard_size, yard_size))
    pygame.draw.rect(screen, PLAYER_COLORS["YELLOW"], (BOARD_MARGIN, SCREEN_HEIGHT - BOARD_MARGIN - yard_size, yard_size, yard_size))
    pygame.draw.rect(screen, PLAYER_COLORS["BLUE"], (SCREEN_WIDTH - BOARD_MARGIN - yard_size, SCREEN_HEIGHT - BOARD_MARGIN - yard_size, yard_size, yard_size))

    center_x = SCREEN_WIDTH / 2
    center_y = SCREEN_HEIGHT / 2

    # Draw home triangle
    pygame.draw.polygon(screen, PLAYER_COLORS["GREEN"], [(center_x, center_y), (BOARD_MARGIN, BOARD_MARGIN), (SCREEN_WIDTH-BOARD_MARGIN, BOARD_MARGIN)])
    pygame.draw.polygon(screen, PLAYER_COLORS["RED"], [(center_x, center_y), (SCREEN_WIDTH-BOARD_MARGIN, BOARD_MARGIN), (SCREEN_WIDTH-BOARD_MARGIN, SCREEN_HEIGHT - BOARD_MARGIN)])
    pygame.draw.polygon(screen, PLAYER_COLORS["YELLOW"], [(center_x, center_y), (BOARD_MARGIN, SCREEN_HEIGHT-BOARD_MARGIN), (BOARD_MARGIN, BOARD_MARGIN)])
    pygame.draw.polygon(screen, PLAYER_COLORS["BLUE"], [(center_x, center_y), (SCREEN_WIDTH-BOARD_MARGIN, SCREEN_HEIGHT - BOARD_MARGIN), (BOARD_MARGIN, SCREEN_HEIGHT - BOARD_MARGIN)])

    # Draw tracks
    for i in range(15):
        # Top track
        pygame.draw.rect(screen, WHITE, (BOARD_MARGIN + yard_size + (i % 3) * (track_width/3), BOARD_MARGIN + (i // 3) * (yard_size/5), (track_width/3), (yard_size/5)), 1)
        # Right track
        pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH - BOARD_MARGIN - yard_size + (i // 5) * (yard_size/5), BOARD_MARGIN + yard_size + (i % 3) * (track_width/3), (yard_size/5), (track_width/3)), 1)
        # Bottom track
        pygame.draw.rect(screen, WHITE, (BOARD_MARGIN + (i % 3) * (track_width/3), SCREEN_HEIGHT - BOARD_MARGIN - yard_size + (i // 3) * (yard_size/5), (track_width/3), (yard_size/5)), 1)
        # Left track
        pygame.draw.rect(screen, WHITE, (BOARD_MARGIN + (i // 5) * (yard_size/5), BOARD_MARGIN + (i % 3) * (track_width/3), (yard_size/5), (track_width/3)), 1)


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
