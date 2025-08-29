"""
Base classes for bot strategies.
"""
from typing import List, Protocol, runtime_checkable
# Use forward references (strings) to avoid circular imports
from ludo.piece import Piece
from ludo.state import GameState


@runtime_checkable
class Strategy(Protocol):
    """
    A protocol that defines the interface for a Ludo bot strategy.
    A strategy is responsible for choosing a move from a list of legal options.
    """

    def choose_move(self, legal_moves: List[Piece], game_state: GameState) -> Piece:
        """
        Selects a piece to move from the list of legal moves.

        Args:
            legal_moves: A list of `Piece` objects that can be legally moved.
            game_state: The current `GameState` of the game.

        Returns:
            The `Piece` object representing the chosen move.
        """
        ...
