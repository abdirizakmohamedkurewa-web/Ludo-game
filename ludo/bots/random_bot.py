"""
Simple bot that chooses a random legal move.
"""

import random
from typing import List

from ludo.bots.base import Strategy
from ludo.move import Move
from ludo.state import GameState


class RandomBot(Strategy):
    """A bot that chooses a random move from the list of legal moves."""

    def choose_move(self, legal_moves: List[Move], game_state: GameState) -> Move:
        """
        Selects a random move from the list of legal moves.

        Args:
            legal_moves: A list of (Piece, destination) tuples.
            game_state: The current `GameState` of the game (unused by this bot).

        Returns:
            The chosen (Piece, destination) tuple.
        """
        return random.choice(legal_moves)
