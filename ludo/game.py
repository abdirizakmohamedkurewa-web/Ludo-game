"""
Game orchestration (turns, state machine).
"""
from typing import Sequence
from ludo.dice import Dice
from ludo.state import GameState
from ludo.player import Player
from ludo.piece import Piece
from ludo.utils.constants import PlayerColor, PieceState
from ludo.board import START_SQUARES, TRACK_LENGTH


class Game:
    """Orchestrates a game of Ludo."""
    def __init__(self, players: Sequence[str], dice: Dice):
        self.dice = dice

        colors = [PlayerColor.RED, PlayerColor.GREEN, PlayerColor.YELLOW, PlayerColor.BLUE]

        player_objects = []
        for i, role in enumerate(players):
            if i < len(colors):
                # NOTE: Role ("human", "random", etc.) is ignored for now.
                player_objects.append(Player(color=colors[i]))

        self.state = GameState(players=player_objects)

    def loop_cli(self):
        """Runs the game loop for the Command-Line Interface."""
        print("Game loop starts now (not implemented).")

    def move_piece(self, piece: Piece, roll: int):
        """Moves a piece according to the given dice roll."""
        if piece.state == PieceState.YARD:
            # Move from YARD to start square
            piece.state = PieceState.TRACK
            piece.position = START_SQUARES[piece.color]
        elif piece.state == PieceState.TRACK:
            # Move along the track
            piece.position = (piece.position + roll) % TRACK_LENGTH
