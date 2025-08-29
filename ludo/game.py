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
from ludo.move import move_piece


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
        move_piece(self.state, piece_to_move, roll)

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
