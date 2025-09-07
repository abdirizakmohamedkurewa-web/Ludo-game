"""
Handles the logic for applying a move to a piece and updating the game state.
"""

from typing import Tuple

from ludo.board import HOME_COLUMN_LENGTH, SAFE_SQUARES, START_SQUARES, TRACK_LENGTH
from ludo.piece import Piece
from ludo.state import GameState
from ludo.utils.constants import PieceState

Move = Tuple[Piece, int]  # A move is a piece and its destination position


def move_piece(game_state: GameState, piece: Piece, roll: int):
    """Moves a piece according to the given dice roll and updates the game state."""
    if piece.state == PieceState.YARD:
        # Move from YARD to start square
        piece.state = PieceState.TRACK
        piece.position = START_SQUARES[piece.color]
        # No further logic needed for this move, but we need to check for captures on the start
        # square.

    elif piece.state == PieceState.TRACK:
        # This calculation is tricky. Let's simplify and assume position is absolute on track.
        # This is consistent with how piece.position is defined.
        new_position_on_track = (piece.position + roll) % TRACK_LENGTH

        # Check if the piece enters or moves within the home column
        # We need to know the piece's progress relative to its start to see if it passes the
        # home entry
        current_progress = (
            piece.position - START_SQUARES[piece.color] + TRACK_LENGTH
        ) % TRACK_LENGTH
        new_progress = current_progress + roll

        if new_progress >= 51:  # 51 is the number of steps to reach home entry
            home_pos = new_progress - 51
            if home_pos < HOME_COLUMN_LENGTH:
                piece.state = PieceState.HOME_COLUMN
                piece.position = 52 + home_pos
            else:  # Overshot
                pass  # This should be an illegal move, handled by Rules
        else:
            # Move along the main track
            piece.position = new_position_on_track

    elif piece.state == PieceState.HOME_COLUMN:
        current_home_pos = piece.position - 52
        new_home_pos = current_home_pos + roll
        if new_home_pos < HOME_COLUMN_LENGTH:
            piece.position = 52 + new_home_pos
        else:  # Overshot
            pass  # This should be an illegal move, handled by Rules

    # Check if the piece reached the final HOME state
    final_home_pos_idx = HOME_COLUMN_LENGTH - 1
    if piece.state == PieceState.HOME_COLUMN and (piece.position - 52) == final_home_pos_idx:
        piece.state = PieceState.HOME

    # Check for captures, only if the piece landed on the main track
    if piece.state == PieceState.TRACK and piece.position not in SAFE_SQUARES:
        for player in game_state.players:
            if player.color == piece.color:
                continue
            # Make a copy of the opponent pieces to avoid issues with modifying while iterating
            for opponent_piece in list(player.pieces):
                if (
                    opponent_piece.state == PieceState.TRACK
                    and opponent_piece.position == piece.position
                ):
                    opponent_piece.state = PieceState.YARD
                    opponent_piece.position = -1  # Back to yard

    # Check for win condition
    current_player = game_state.players[game_state.current_player_index]
    if all(p.state == PieceState.HOME for p in current_player.pieces):
        game_state.is_game_over = True
