"""
Game orchestration (turns, state machine).
"""

from typing import Optional, Sequence

from ludo.bots.base import Strategy
from ludo.dice import Dice
from ludo.move import move_piece
from ludo.persistence import save_game
from ludo.player import Player
from ludo.rules import Rules
from ludo.state import GameState


class Game:
    """
    Orchestrates a game of Ludo, managing the game state, player turns,
    and the application of game rules.

    Attributes:
        dice (Dice): The dice instance for the game.
        strategies (Sequence[Strategy]): A sequence of bot strategies, one for
            each player.
        three_six_forfeit (bool): If True, rolling three consecutive sixes
            forfeits the turn.
        use_blocking_rule (bool): If True, two pieces of the same color on
            the same square form a block.
        state (GameState): The current state of the game.
    """

    def __init__(
        self,
        players: Sequence[Player],
        strategies: Sequence[Strategy],
        dice: Dice,
        state: Optional[GameState] = None,
        three_six_forfeit: bool = True,
        use_blocking_rule: bool = True,
    ):
        """
        Initializes a new Ludo game.

        Args:
            players: A sequence of Player objects participating in the game.
            strategies: A sequence of bot strategies corresponding to the players.
            dice: A Dice object to be used for rolling.
            state: An optional GameState to load from. If None, a new game
                state is created.
            three_six_forfeit: A boolean flag to enable or disable the
                "three consecutive sixes forfeit turn" rule.
            use_blocking_rule: A boolean flag to enable or disable the
                blocking rule.
        """
        self.dice = dice
        self.strategies = strategies
        self.three_six_forfeit = three_six_forfeit
        self.use_blocking_rule = use_blocking_rule

        if state:
            self.state = state
        else:
            self.state = GameState(players=list(players), dice_seed=self.dice.seed)

    def play_turn(self, roll: int):
        """
        Processes a single, automated game turn given a dice roll.

        This method performs the following steps:
        1. Handles consecutive sixes and checks for turn forfeiture.
        2. Determines all legal moves for the current player based on the roll.
        3. If legal moves are available, it uses the player's strategy to
           choose a move.
        4. Applies the chosen move to the game state.
        5. Checks for a win condition.
        6. Advances to the next player if the roll was not a 6.

        Args:
            roll: The integer result of a dice roll (1-6).
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
        legal_moves = Rules.get_legal_moves(self.state, roll, self.use_blocking_rule)

        # 4. Handle case with no legal moves
        if not legal_moves:
            print("No legal moves available.")
            if roll != 6:
                self.next_player()
            # If roll is 6, player keeps the turn for another roll.
            return

        # 5. Choose a move using the current player's strategy
        current_strategy = self.strategies[self.state.current_player_index]
        chosen_move = current_strategy.choose_move(legal_moves, self.state)
        piece_to_move, _ = chosen_move
        move_piece(self.state, piece_to_move, roll)

        # 6. Check for win condition
        if self.state.is_game_over:
            return

        # 7. Advance player if the roll was not a 6
        if roll != 6:
            self.next_player()

    def _get_player_command(self, player: Player) -> list[str]:
        """Gets a command from the current player (human or bot)."""
        if player.role == "human":
            command_str = input("Enter command (roll, save <file>, quit): ")
            return command_str.strip().split()
        else:
            print(f"Bot ({player.role}) is thinking...")
            return ["roll"]

    def _handle_roll(self, player: Player):
        """Handles the 'roll' command."""
        roll = self.dice.roll()
        print(f"Rolled a {roll}")

        old_player_index = self.state.current_player_index
        self.play_turn(roll)

        if self.state.is_game_over:
            print(f"--- Player {player.color.name} wins! ---")
            return

        new_player_index = self.state.current_player_index
        if roll == 6:
            if old_player_index != new_player_index:
                print("Rolled three consecutive 6s. Forfeiting turn.")
            else:
                print("Got an extra turn for rolling a 6.")

    def _handle_save(self, command: list[str]):
        """Handles the 'save' command."""
        if len(command) > 1:
            filepath = command[1]
            save_game(self.state, filepath)
            print(f"Game saved to {filepath}")
        else:
            print("Error: Missing filepath. Usage: save <filepath>")

    def loop_cli(self):
        """Runs the game loop for the Command-Line Interface."""
        while not self.state.is_game_over:
            player = self.state.players[self.state.current_player_index]
            print(f"\n--- {player.color.value}'s Turn ({player.role}) ---")

            command = self._get_player_command(player)
            action = command[0].lower() if command else ""

            if action == "roll":
                self._handle_roll(player)
            elif action == "save":
                self._handle_save(command)
            elif action == "quit":
                print("Quitting game.")
                break
            elif player.role == "human":
                print(f"Unknown command: {action}")

    def next_player(self):
        """Advances to the next player."""
        self.state.current_player_index = (self.state.current_player_index + 1) % len(
            self.state.players
        )
        self.state.consecutive_sixes = 0
