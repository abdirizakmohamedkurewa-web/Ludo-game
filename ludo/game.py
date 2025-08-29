"""
Game orchestration (turns, state machine).
"""
from typing import Sequence
from ludo.dice import Dice
from ludo.state import GameState
from ludo.player import Player
from ludo.piece import Piece
from ludo.rules import Rules
from ludo.utils.constants import PlayerColor, PieceState
from ludo.board import START_SQUARES, TRACK_LENGTH, HOME_COLUMN_LENGTH, SAFE_SQUARES


class Game:
    """Orchestrates a game of Ludo."""
    def __init__(self, players: Sequence[str], dice: Dice, three_six_forfeit: bool = True, use_blocking_rule: bool = True):
        self.dice = dice
        self.three_six_forfeit = three_six_forfeit
        self.use_blocking_rule = use_blocking_rule

        colors = [PlayerColor.RED, PlayerColor.GREEN, PlayerColor.YELLOW, PlayerColor.BLUE]

        player_objects = []
        for i, role in enumerate(players):
            if i < len(colors):
                # NOTE: Role ("human", "random", etc.) is ignored for now.
                player_objects.append(Player(color=colors[i]))

        self.state = GameState(players=player_objects)

    def play_turn(self, roll: int):
        """
        Processes a single, automated game turn given a dice roll.
        It updates the game state, including choosing and making a move
        (defaults to the first legal one), and advancing the player turn
        if necessary.
        """
        self.state.dice_roll = roll

        # 1. Handle consecutive sixes
        if roll == 6:
            self.state.consecutive_sixes += 1
        else:
            self.state.consecutive_sixes = 0

        # 2. Check for three consecutive sixes forfeit
        if self.three_six_forfeit and self.state.consecutive_sixes == 3:
            self.next_player()
            return  # Turn is forfeited

        # 3. Get legal moves
        legal_moves = Rules.get_legal_moves(
            self.state, roll, self.use_blocking_rule
        )

        # 4. Handle case with no legal moves
        if not legal_moves:
            if roll != 6:
                self.next_player()
            # If roll is 6, player keeps the turn for another roll.
            return

        # 5. Choose a move (for now, always the first legal one)
        piece_to_move = legal_moves[0]
        self.move_piece(piece_to_move, roll)

        # 6. Check for win condition
        if self.state.is_game_over:
            return

        # 7. Advance player if the roll was not a 6
        if roll != 6:
            self.next_player()

    def loop_cli(self):
        """Runs the game loop for the Command-Line Interface."""
        while not self.state.is_game_over:
            player = self.state.players[self.state.current_player_index]
            print(f"\n--- {player.color.value}'s Turn ---")

            roll = self.dice.roll()
            print(f"Rolled a {roll}")

            old_player_index = self.state.current_player_index
            self.play_turn(roll)

            if self.state.is_game_over:
                print(f"\n--- Player {player.color.value} wins! ---")
                break

            new_player_index = self.state.current_player_index
            if roll == 6:
                if old_player_index != new_player_index:
                    print("Rolled three consecutive 6s. Forfeiting turn.")
                else:
                    print("Got an extra turn for rolling a 6.")

    def next_player(self):
        """Advances to the next player."""
        self.state.current_player_index = (self.state.current_player_index + 1) % len(self.state.players)
        self.state.consecutive_sixes = 0

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
