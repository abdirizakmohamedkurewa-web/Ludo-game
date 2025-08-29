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
            return  # No further logic needed for this move

        elif piece.state == PieceState.TRACK:
            start_square = START_SQUARES[piece.color]
            progress = (piece.position - start_square + TRACK_LENGTH) % TRACK_LENGTH
            new_progress = progress + roll

            # Check if the piece enters or moves within the home column
            if new_progress >= 51:
                home_pos = new_progress - 51
                piece.state = PieceState.HOME_COLUMN
                piece.position = 52 + home_pos
            else:
                # Move along the main track
                piece.position = (piece.position + roll) % TRACK_LENGTH

        elif piece.state == PieceState.HOME_COLUMN:
            current_home_pos = piece.position - 52
            new_home_pos = current_home_pos + roll
            piece.position = 52 + new_home_pos

        # Check if the piece reached the final HOME state
        final_home_pos_idx = HOME_COLUMN_LENGTH - 1
        if piece.state == PieceState.HOME_COLUMN and (piece.position - 52) == final_home_pos_idx:
            piece.state = PieceState.HOME

        # Check for captures, only if the piece landed on the main track
        if piece.state == PieceState.TRACK and piece.position not in SAFE_SQUARES:
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

        # Check for win condition
        current_player = self.state.players[self.state.current_player_index]
        if all(p.state == PieceState.HOME for p in current_player.pieces):
            self.state.is_game_over = True
