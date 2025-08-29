"""
Game orchestration (turns, state machine).
"""
from typing import Sequence
from ludo.dice import Dice
from ludo.state import GameState
from ludo.player import Player
from ludo.piece import Piece
from ludo.utils.constants import PlayerColor, PieceState
from ludo.board import START_SQUARES, TRACK_LENGTH, HOME_COLUMN_LENGTH, SAFE_SQUARES


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
            start_square = START_SQUARES[piece.color]
            progress = (piece.position - start_square + TRACK_LENGTH) % TRACK_LENGTH
            new_progress = progress + roll

            # A piece enters the home column after passing the 50th square of its path
            if new_progress >= 51:
                home_pos = new_progress - 51
                if home_pos < HOME_COLUMN_LENGTH:
                    piece.state = PieceState.HOME_COLUMN
                    piece.position = 52 + home_pos
                    if home_pos == HOME_COLUMN_LENGTH - 1:
                        piece.state = PieceState.HOME
                # Note: "Exact roll" logic is not implemented here. We assume the move is legal.
            else:
                # Move along the track
                piece.position = (piece.position + roll) % TRACK_LENGTH

                # Check for captures
                if piece.position not in SAFE_SQUARES:
                    for player in self.state.players:
                        if player.color == piece.color:
                            continue
                        for opponent_piece in player.pieces:
                            if (
                                opponent_piece.state == PieceState.TRACK
                                and opponent_piece.position == piece.position
                            ):
                                opponent_piece.state = PieceState.YARD
                                opponent_piece.position = -1  # Back to yard
        elif piece.state == PieceState.HOME_COLUMN:
            current_home_pos = piece.position - 52
            new_home_pos = current_home_pos + roll

            if new_home_pos < HOME_COLUMN_LENGTH:
                piece.position = 52 + new_home_pos
                if new_home_pos == HOME_COLUMN_LENGTH - 1:
                    piece.state = PieceState.HOME
            # Note: "Exact roll" logic is not implemented here.
