"""
Bot that asks a human for input.
"""
from typing import List
from ludo.bots.base import Strategy
from ludo.piece import Piece
from ludo.state import GameState


class HumanBot(Strategy):
    """A strategy that asks a human to choose a move via the CLI."""

    def choose_move(self, legal_moves: List[Piece], game_state: GameState) -> Piece:
        """
        Prompts the human player to choose a move from the list of legal options.

        Args:
            legal_moves: A list of `Piece` objects that can be legally moved.
            game_state: The current `GameState` of the game.

        Returns:
            The `Piece` object representing the chosen move.
        """
        print("Legal moves:")
        for i, piece in enumerate(legal_moves):
            print(f"  {i + 1}: Move piece {piece.id} at position {piece.position}")

        while True:
            try:
                choice = input(f"Choose a move (1-{len(legal_moves)}): ")
                choice_index = int(choice) - 1
                if 0 <= choice_index < len(legal_moves):
                    return legal_moves[choice_index]
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
