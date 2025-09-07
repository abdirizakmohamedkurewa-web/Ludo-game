import sys

import pygame  # type: ignore

from apps.gui.board_layout import (
    BOARD_X_START,
    BOARD_Y_START,
    GRID_COUNT,
    HOME_COLUMN_COORDINATES,
    TRACK_COORDINATES,
    YARD_COORDINATES,
)
from apps.gui.constants import (
    BLACK,
    GRID_SIZE,
    LIGHT_GRAY,
    PLAYER_COLORS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    WHITE,
)
from ludo.board import SAFE_SQUARES, START_SQUARES
from ludo.bots.human_bot import HumanBot
from ludo.dice import Dice
from ludo.game import Game
from ludo.move import move_piece
from ludo.player import Player
from ludo.rules import Rules
from ludo.utils.constants import PieceState, PlayerColor


def get_pos_pixel_coords(color, position):
    """Calculates the pixel coordinates for a given board position index."""
    if 0 <= position < 52:  # Main track
        return TRACK_COORDINATES[position]
    elif 52 <= position < 58:  # Home column
        home_pos = position - 52
        if 0 <= home_pos < len(HOME_COLUMN_COORDINATES[color]):
            return HOME_COLUMN_COORDINATES[color][home_pos]
    return None  # For YARD or HOME state, which don't have a single destination square


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
        else:  # RED
            x, y = BOARD_X_START + GRID_SIZE * 5, BOARD_Y_START + GRID_SIZE * 7.5
        piece_radius = GRID_SIZE // 2 - 4
        x += (piece.id - 1.5) * piece_radius / 2
        y += (piece.id - 1.5) * piece_radius / 2
    else:
        return None

    return x + GRID_SIZE // 2, y + GRID_SIZE // 2


def draw_pieces(screen, game_state, legal_moves, selected_piece, animation=None):
    """Draws the player pieces on the board."""
    piece_radius = GRID_SIZE // 2 - 4
    movable_pieces = [move[0] for move in legal_moves]
    animating_piece = (
        animation["piece"] if animation and animation["type"] == "piece_move" else None
    )

    for player in game_state.players:
        player_color = PLAYER_COLORS[player.color.name]
        for piece in player.pieces:
            # Skip drawing the animating piece from its static position
            if piece == animating_piece:
                continue

            pos = get_piece_pixel_pos(player, piece)
            if pos:
                center_x, center_y = pos
                # Draw piece shadow
                pygame.draw.circle(
                    screen, (0, 0, 0, 50), (center_x + 2, center_y + 2), piece_radius
                )
                # Draw piece
                pygame.draw.circle(screen, player_color, (center_x, center_y), piece_radius)
                # Draw border
                pygame.draw.circle(screen, BLACK, (center_x, center_y), piece_radius, 2)

                # Highlight if it's a legal move
                if piece in movable_pieces:
                    highlight_color = (255, 255, 0, 150)  # Yellow highlight
                    pygame.draw.circle(
                        screen, highlight_color, (center_x, center_y), piece_radius, 4
                    )

                # Highlight if selected
                if piece == selected_piece:
                    pygame.draw.circle(
                        screen, (0, 255, 255), (center_x, center_y), piece_radius + 2, 3
                    )

    # Draw the animating piece at its interpolated position
    if animating_piece:
        player = game_state.players[game_state.current_player_index]
        player_color = PLAYER_COLORS[player.color.name]
        center_x, center_y = animation["current_pos"]
        # Draw piece shadow
        pygame.draw.circle(screen, (0, 0, 0, 50), (center_x + 2, center_y + 2), piece_radius)
        # Draw piece
        pygame.draw.circle(screen, player_color, (center_x, center_y), piece_radius)
        # Draw border
        pygame.draw.circle(screen, BLACK, (center_x, center_y), piece_radius, 2)


def draw_legal_move_highlights(screen, game, selected_piece, legal_moves):
    """Draws highlights for the possible destination squares of a selected piece."""
    if not selected_piece:
        return

    highlight_color = (0, 255, 255, 100)  # Cyan, semi-transparent

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
    pygame.draw.rect(
        screen, PLAYER_COLORS["GREEN"], (BOARD_X_START, BOARD_Y_START, yard_size, yard_size)
    )
    # YELLOW
    pygame.draw.rect(
        screen,
        PLAYER_COLORS["YELLOW"],
        (BOARD_X_START + GRID_SIZE * 9, BOARD_Y_START, yard_size, yard_size),
    )
    # BLUE
    pygame.draw.rect(
        screen,
        PLAYER_COLORS["BLUE"],
        (BOARD_X_START + GRID_SIZE * 9, BOARD_Y_START + GRID_SIZE * 9, yard_size, yard_size),
    )
    # RED
    pygame.draw.rect(
        screen,
        PLAYER_COLORS["RED"],
        (BOARD_X_START, BOARD_Y_START + GRID_SIZE * 9, yard_size, yard_size),
    )

    # Inner Yard circles
    pygame.draw.circle(
        screen,
        WHITE,
        (BOARD_X_START + yard_size / 2, BOARD_Y_START + yard_size / 2),
        yard_size / 2 - GRID_SIZE,
        5,
    )
    pygame.draw.circle(
        screen,
        WHITE,
        (BOARD_X_START + GRID_SIZE * 9 + yard_size / 2, BOARD_Y_START + yard_size / 2),
        yard_size / 2 - GRID_SIZE,
        5,
    )
    pygame.draw.circle(
        screen,
        WHITE,
        (
            BOARD_X_START + GRID_SIZE * 9 + yard_size / 2,
            BOARD_Y_START + GRID_SIZE * 9 + yard_size / 2,
        ),
        yard_size / 2 - GRID_SIZE,
        5,
    )
    pygame.draw.circle(
        screen,
        WHITE,
        (BOARD_X_START + yard_size / 2, BOARD_Y_START + GRID_SIZE * 9 + yard_size / 2),
        yard_size / 2 - GRID_SIZE,
        5,
    )

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
        pygame.draw.rect(screen, BLACK, (x, y, GRID_SIZE, GRID_SIZE), 1)  # Black border

        # Highlight safe squares with a star
        if i in SAFE_SQUARES and i not in START_SQUARES.values():
            center_x, center_y = x + GRID_SIZE // 2, y + GRID_SIZE // 2
            pygame.draw.circle(screen, BLACK, (center_x, center_y), 5)

    # --- 3. Draw Home Columns ---
    for color, coords in HOME_COLUMN_COORDINATES.items():
        player_color = PLAYER_COLORS[color.name]
        for _i, (x, y) in enumerate(coords):
            pygame.draw.rect(screen, player_color, (x, y, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BLACK, (x, y, GRID_SIZE, GRID_SIZE), 1)  # Black border

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
    pygame.draw.polygon(
        screen, PLAYER_COLORS["GREEN"], [home_points[0], home_points[1], (center_x, center_y)]
    )
    pygame.draw.polygon(
        screen, PLAYER_COLORS["YELLOW"], [(home_points[1]), (home_points[3]), (center_x, center_y)]
    )
    pygame.draw.polygon(
        screen, PLAYER_COLORS["BLUE"], [(home_points[3]), (home_points[4]), (center_x, center_y)]
    )
    pygame.draw.polygon(
        screen, PLAYER_COLORS["RED"], [(home_points[4]), (home_points[0]), (center_x, center_y)]
    )
    pygame.draw.rect(
        screen,
        BLACK,
        (
            BOARD_X_START + GRID_SIZE * 6,
            BOARD_Y_START + GRID_SIZE * 6,
            GRID_SIZE * 3,
            GRID_SIZE * 3,
        ),
        1,
    )


def draw_info_panel(screen, game, font, ui_buttons, animation=None):
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
    if animation and animation["type"] == "dice_roll":
        dice_text = f"Rolling... {animation['display_roll']}"
    elif game.state.dice_roll is not None:
        dice_text = f"Rolled a: {game.state.dice_roll}"

    dice_surf = font.render(dice_text, True, BLACK)
    screen.blit(dice_surf, (panel_x + 20, panel_y + 80))

    # --- 3. "Roll Dice" Button ---
    roll_button_rect = pygame.Rect(panel_x + 20, panel_y + 140, panel_width - 40, 50)
    ui_buttons["roll_dice"] = roll_button_rect  # Store for click detection

    # Make button uninteractable during roll
    button_color = PLAYER_COLORS["GREEN"]
    if game.state.dice_roll is not None or (animation and animation["type"] == "dice_roll"):
        button_color = (150, 220, 150)  # Faded green

    pygame.draw.rect(screen, button_color, roll_button_rect)
    roll_text_surf = font.render("Roll Dice", True, BLACK)
    text_rect = roll_text_surf.get_rect(center=roll_button_rect.center)
    screen.blit(roll_text_surf, text_rect)


def draw_game_over_screen(screen, winner, font, ui_buttons):
    """Draws the game over overlay."""
    overlay_color = (0, 0, 0, 180)  # Semi-transparent black
    s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    s.fill(overlay_color)
    screen.blit(s, (0, 0))

    # --- Winner Text ---
    winner_color_name = winner.color.name
    winner_text = f"Player {winner_color_name} Wins!"
    text_surf = font.render(winner_text, True, PLAYER_COLORS[winner_color_name])
    text_rect = text_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 60))
    screen.blit(text_surf, text_rect)

    # --- "Play Again" Button ---
    play_again_rect = pygame.Rect(SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2, 140, 50)
    ui_buttons["play_again"] = play_again_rect
    pygame.draw.rect(screen, PLAYER_COLORS["GREEN"], play_again_rect)
    play_again_text = font.render("Play Again", True, BLACK)
    text_rect = play_again_text.get_rect(center=play_again_rect.center)
    screen.blit(play_again_text, text_rect)

    # --- "Quit" Button ---
    quit_rect = pygame.Rect(SCREEN_WIDTH / 2 + 10, SCREEN_HEIGHT / 2, 140, 50)
    ui_buttons["quit"] = quit_rect
    pygame.draw.rect(screen, PLAYER_COLORS["RED"], quit_rect)
    quit_text = font.render("Quit", True, BLACK)
    text_rect = quit_text.get_rect(center=quit_rect.center)
    screen.blit(quit_text, text_rect)


def main():
    """Main function to run the Ludo game GUI."""
    pygame.init()
    font = pygame.font.SysFont("Arial", 24)
    big_font = pygame.font.SysFont("Arial", 48, bold=True)
    clock = pygame.time.Clock()
    ui_buttons = {}  # To store rects of UI elements for interaction

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Ludo")

    dice = Dice()

    # --- Game Factory Function ---
    def create_game():
        players = [
            Player(color=PlayerColor.RED, role="human"),
            Player(color=PlayerColor.GREEN, role="human"),
            Player(color=PlayerColor.YELLOW, role="human"),
            Player(color=PlayerColor.BLUE, role="human"),
        ]
        strategies = [HumanBot(), HumanBot(), HumanBot(), HumanBot()]
        return Game(players=players, strategies=strategies, dice=dice)

    game = create_game()

    # Game loop variables
    legal_moves = []
    selected_piece = None
    animation = None  # For handling animations
    winner = None

    running = True
    while running:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # --- Handle User Input ---
            # Block game input if an animation is running or game is over
            if animation:
                continue

            if winner:  # Game is over, only handle game over screen buttons
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if ui_buttons.get("play_again") and ui_buttons["play_again"].collidepoint(
                        event.pos
                    ):
                        print("Starting a new game...")
                        game = create_game()
                        winner = None
                        legal_moves = []
                        selected_piece = None
                        animation = None
                        ui_buttons = {}
                    elif ui_buttons.get("quit") and ui_buttons["quit"].collidepoint(event.pos):
                        running = False
                continue  # Skip the rest of the event loop

            if event.type == pygame.MOUSEBUTTONDOWN:
                # 1. Handle Roll Dice Button Click
                if ui_buttons.get("roll_dice") and ui_buttons["roll_dice"].collidepoint(event.pos):
                    if game.state.dice_roll is None:
                        # --- Start Dice Roll Animation ---
                        animation = {
                            "type": "dice_roll",
                            "timer": 0.0,
                            "duration": 0.5,  # seconds
                            "interval": 0.05,
                            "interval_timer": 0.0,
                            "display_roll": 1,
                        }

                # 2. Handle Piece Interaction (Selection and Movement)
                elif game.state.dice_roll is not None and legal_moves:
                    mouse_pos = event.pos
                    current_player = game.state.players[game.state.current_player_index]
                    moved_piece = False

                    # --- A. Is a piece selected? If so, try to move it. ---
                    if selected_piece:
                        destinations = [
                            dest for p, dest in legal_moves if p.id == selected_piece.id
                        ]

                        for dest_pos in destinations:
                            coords = get_pos_pixel_coords(current_player.color, dest_pos)
                            if coords and pygame.Rect(
                                coords[0], coords[1], GRID_SIZE, GRID_SIZE
                            ).collidepoint(mouse_pos):
                                # --- Start Piece Move Animation ---
                                start_pos_pixels = get_piece_pixel_pos(
                                    current_player, selected_piece
                                )
                                end_pos_pixels = (
                                    coords[0] + GRID_SIZE // 2,
                                    coords[1] + GRID_SIZE // 2,
                                )

                                animation = {
                                    "type": "piece_move",
                                    "piece": selected_piece,
                                    "start_pos": start_pos_pixels,
                                    "end_pos": end_pos_pixels,
                                    "current_pos": start_pos_pixels,
                                    "timer": 0.0,
                                    "duration": 0.3,  # seconds
                                    "roll": game.state.dice_roll,
                                    "destination": dest_pos,
                                }

                                legal_moves = []  # Clear highlights
                                moved_piece = True
                                break  # Exit the destinations loop

                        # If the click was not on a valid move, deselect the piece so the user can
                        # re-select.
                        if not moved_piece:
                            print("Invalid destination clicked. Deselecting piece.")
                            selected_piece = None

                    # --- B. If no piece was moved, try to select a new piece. ---
                    if not moved_piece:
                        movable_pieces = [move[0] for move in legal_moves]
                        for piece in current_player.pieces:
                            if piece in movable_pieces:
                                pos = get_piece_pixel_pos(current_player, piece)
                                if pos:
                                    piece_radius = GRID_SIZE // 2 - 4
                                    piece_rect = pygame.Rect(
                                        pos[0] - piece_radius,
                                        pos[1] - piece_radius,
                                        piece_radius * 2,
                                        piece_radius * 2,
                                    )
                                    if piece_rect.collidepoint(mouse_pos):
                                        selected_piece = piece
                                        print(f"Selected piece {piece.id}")
                                        break

        # --- Update Animations ---
        if animation:
            animation["timer"] += time_delta
            if animation["type"] == "dice_roll":
                animation["interval_timer"] += time_delta
                if animation["interval_timer"] >= animation["interval"]:
                    animation["display_roll"] = dice.roll()  # Visually cycle numbers
                    animation["interval_timer"] = 0.0

                if animation["timer"] >= animation["duration"]:
                    # --- Animation Finished: Set final dice roll ---
                    roll = dice.roll()  # The "real" roll
                    game.state.dice_roll = roll
                    legal_moves = Rules.get_legal_moves(game.state, roll)
                    selected_piece = None
                    print(
                        f"Player rolled a {roll}. "
                        f"Legal moves: {[(m[0].id, m[1]) for m in legal_moves]}"
                    )

                    if not legal_moves:
                        print("No legal moves available.")
                        if roll != 6:
                            game.next_player()
                        game.state.dice_roll = None

                    animation = None  # End animation

            elif animation["type"] == "piece_move":
                progress = min(animation["timer"] / animation["duration"], 1.0)

                start_x, start_y = animation["start_pos"]
                end_x, end_y = animation["end_pos"]

                # Linear interpolation
                current_x = start_x + (end_x - start_x) * progress
                current_y = start_y + (end_y - start_y) * progress
                animation["current_pos"] = (current_x, current_y)

                if progress >= 1.0:
                    # --- Animation Finished: Update Game State ---
                    piece_to_move = animation["piece"]
                    roll = animation["roll"]

                    move_piece(game.state, piece_to_move, roll)
                    print(
                        f"Moved piece {piece_to_move.id} to "
                        f"destination {animation['destination']}"
                    )

                    if game.state.is_game_over:
                        winner = game.state.players[game.state.current_player_index]
                        print(f"Player {winner.color.name} has won!")

                    if roll != 6:
                        game.next_player()

                    # Reset for next turn
                    selected_piece = None
                    game.state.dice_roll = None
                    animation = None  # End animation

        # --- Drawing Code ---
        screen.fill(WHITE)
        draw_board(screen)
        draw_legal_move_highlights(screen, game, selected_piece, legal_moves)
        draw_pieces(screen, game.state, legal_moves, selected_piece, animation)
        draw_info_panel(screen, game, font, ui_buttons, animation)

        if winner:
            draw_game_over_screen(screen, winner, big_font, ui_buttons)

        # Update the display
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
