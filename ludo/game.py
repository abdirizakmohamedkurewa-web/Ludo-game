"""
Game orchestration (turns, state machine).
"""
from ludo.state import GameState
from ludo.player import Player
from ludo.piece import Piece
from ludo.utils.constants import PlayerColor, PieceState
from ludo.board import START_SQUARES, TRACK_LENGTH


class Game:
    """Orchestrates a game of Ludo."""
    def __init__(self):
        self.state = self._create_initial_state()

    def _create_initial_state(self) -> GameState:
        """Creates the starting state for a new game."""
        colors = [PlayerColor.RED, PlayerColor.GREEN, PlayerColor.YELLOW, PlayerColor.BLUE]
        players = [Player(color=color) for color in colors]
        return GameState(players=players)

    def move_piece(self, piece: Piece):
        """Moves a piece according to the last dice roll."""
        if piece.state == PieceState.YARD:
            # Move from YARD to start square
            piece.state = PieceState.TRACK
            piece.position = START_SQUARES[piece.color]
        elif piece.state == PieceState.TRACK:
            # Move along the track
            roll = self.state.dice_roll
            if roll is None:
                raise ValueError("Cannot move piece without a dice roll.")

            # Simple movement for now, no wrapping around the board yet
            piece.position = (piece.position + roll) % TRACK_LENGTH
