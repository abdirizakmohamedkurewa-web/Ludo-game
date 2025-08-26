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
        """
        legal_pieces = []
        player = game_state.players[game_state.current_player_index]

        if roll == 6:
            # If a 6 is rolled, any piece in the yard is a legal move
            for piece in player.pieces:
                if piece.state == PieceState.YARD:
                    legal_pieces.append(piece)

        # Any piece on the track is a legal move
        for piece in player.pieces:
            if piece.state == PieceState.TRACK:
                legal_pieces.append(piece)

        return legal_pieces
