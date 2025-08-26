"""
Move validation, capture rules, safe squares.
"""
from typing import List
from ludo.state import GameState
from ludo.piece import Piece
from ludo.utils.constants import PieceState


class Rules:
    """Contains all the game logic and rules."""
    @staticmethod
    def get_legal_moves(game_state: GameState, roll: int) -> List[Piece]:
        """
        Determines which of the current player's pieces have legal moves.
        If a 6 is rolled, priority is given to moving a piece from the yard.
        """
        player = game_state.players[game_state.current_player_index]

        if roll == 6:
            yard_pieces = [p for p in player.pieces if p.state == PieceState.YARD]
            if yard_pieces:
                # If a 6 is rolled and pieces are in the yard, these are the only legal moves
                return yard_pieces

        # If the roll is not 6, or if it is 6 but no pieces are in the yard,
        # then any piece on the track is a legal move.
        return [p for p in player.pieces if p.state == PieceState.TRACK]
