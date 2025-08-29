"""
Simple bot that chooses a random legal move.
"""
import random
from typing import List
from ludo.bots.base import Strategy
from ludo.piece import Piece
from ludo.state import GameState


class RandomBot(Strategy):
    """A bot that chooses a random move from the list of legal moves."""

    def choose_move(self, legal_moves: List[Piece], game_state: GameState) -> Piece:
        """
        Selects a random piece to move from the list of legal moves.

        Args:
            legal_moves: A list of `Piece` objects that can be legally moved.
            game_state: The current `GameState` of the game (unused by this bot).

        Returns:
            The `Piece` object representing the chosen move.
        """
        return random.choice(legal_moves)
