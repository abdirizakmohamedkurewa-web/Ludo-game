"""
Move validation, capture rules, safe squares.
"""
from typing import List
from ludo.state import GameState
from ludo.piece import Piece
from ludo.utils.constants import PieceState
from ludo.board import (
    HOME_COLUMN_LENGTH,
    START_SQUARES,
    TRACK_LENGTH,
)


class Rules:
    """Contains all the game logic and rules."""
    @staticmethod
    def get_legal_moves(game_state: GameState, roll: int) -> List[Piece]:
        """
        Determines which of the current player's pieces have legal moves.
        - If a 6 is rolled, priority is given to moving a piece from the yard.
        - Pieces on the track can move if they don't overshoot the home column.
        - Pieces in the home column can only move if the roll is exact.
        """
        player = game_state.players[game_state.current_player_index]
        legal_moves = []

        # Rule: If a 6 is rolled, moving a piece from the yard takes priority
        if roll == 6:
            yard_pieces = [p for p in player.pieces if p.state == PieceState.YARD]
            if yard_pieces:
                return yard_pieces

        # Check for legal moves for pieces on the track or in the home column
        for piece in player.pieces:
            if piece.state == PieceState.TRACK:
                start_square = START_SQUARES[piece.color]
                progress = (piece.position - start_square + TRACK_LENGTH) % TRACK_LENGTH
                new_progress = progress + roll
                # A piece's total journey is 51 steps on the track + 6 in the home column
                if new_progress < TRACK_LENGTH - 1 + HOME_COLUMN_LENGTH:
                    legal_moves.append(piece)

            elif piece.state == PieceState.HOME_COLUMN:
                # The piece's position in the home column (0-4, since 5 is HOME)
                current_home_pos = piece.position - 52
                # The final position in the home column is at index 5
                final_home_pos = HOME_COLUMN_LENGTH - 1
                needed_roll = final_home_pos - current_home_pos
                if roll == needed_roll:
                    legal_moves.append(piece)

        return legal_moves
