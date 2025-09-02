"""
Move validation, capture rules, safe squares.
"""
from typing import List
from ludo.state import GameState
from ludo.piece import Piece
from ludo.move import Move
from ludo.utils.constants import PieceState, PlayerColor
from ludo.board import (
    HOME_COLUMN_LENGTH,
    START_SQUARES,
    TRACK_LENGTH,
)


class Rules:
    """Contains all the game logic and rules."""
    @staticmethod
    def get_legal_moves(game_state: GameState, roll: int, use_blocking_rule: bool = True) -> List[Move]:
        """
        Determines which of the current player's pieces have legal moves.
        Returns a list of (piece, destination) tuples.
        """
        player = game_state.players[game_state.current_player_index]
        legal_moves: List[Move] = []
        start_square = START_SQUARES[player.color]

        # Rule: If a 6 is rolled, moving a piece from the yard is a legal move
        if roll == 6:
            yard_pieces = [p for p in player.pieces if p.state == PieceState.YARD]
            if yard_pieces:
                # The destination is the player's start square
                legal_moves.append((yard_pieces[0], start_square))

        # Check for legal moves for pieces on the track or in the home column
        for piece in player.pieces:
            if piece.state == PieceState.TRACK:
                current_progress = (piece.position - start_square + TRACK_LENGTH) % TRACK_LENGTH
                new_progress = current_progress + roll

                # Check for blocks if the rule is enabled
                path_is_clear = True
                if use_blocking_rule:
                    for i in range(1, roll): # Check intermediate squares
                        intermediate_square = (piece.position + i) % TRACK_LENGTH
                        if Rules.is_square_blocked_by_opponent(intermediate_square, player.color, game_state):
                            path_is_clear = False
                            break
                if not path_is_clear:
                    continue

                # A piece's total journey is 51 steps on track + 6 in home column
                if new_progress < 51: # Stays on main track
                    destination = (piece.position + roll) % TRACK_LENGTH
                    legal_moves.append((piece, destination))
                elif new_progress < 51 + HOME_COLUMN_LENGTH: # Enters home column
                    home_col_pos = new_progress - 51
                    destination = 52 + home_col_pos # 52 is the base for home column positions
                    legal_moves.append((piece, destination))

            elif piece.state == PieceState.HOME_COLUMN:
                current_home_pos = piece.position - 52
                new_home_pos = current_home_pos + roll
                if new_home_pos < HOME_COLUMN_LENGTH:
                    destination = 52 + new_home_pos
                    legal_moves.append((piece, destination))

        return legal_moves

    @staticmethod
    def is_square_blocked_by_opponent(
        square_position: int, current_player_color: PlayerColor, game_state: GameState
    ) -> bool:
        """Checks if a square is blocked by two or more pieces of the same opponent color."""
        for player in game_state.players:
            if player.color == current_player_color:
                continue  # Friendly pieces don't block the current player

            opponent_pieces_on_square = 0
            for piece in player.pieces:
                if piece.position == square_position and piece.state == PieceState.TRACK:
                    opponent_pieces_on_square += 1

            if opponent_pieces_on_square >= 2:
                return True  # Found a block from this opponent

        return False
