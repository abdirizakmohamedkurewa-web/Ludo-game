import pytest
from unittest.mock import MagicMock, patch

from ludo.game import Game
from ludo.player import Player
from ludo.bots.base import Strategy
from ludo.dice import Dice
from ludo.state import GameState
from ludo.utils.constants import PlayerColor


@pytest.fixture
def mock_game():
    """Fixture to create a mock Game instance for testing CLI interactions."""
    players = [
        Player(color=PlayerColor.RED, role="human"),
        Player(color=PlayerColor.GREEN, role="random"),
    ]
    strategies = [MagicMock(spec=Strategy), MagicMock(spec=Strategy)]
    dice = MagicMock(spec=Dice)
    dice.seed = 42
    game = Game(players, strategies, dice)
    return game

def test_get_player_command_human(mock_game):
    """Test getting a command from a human player."""
    with patch("builtins.input", return_value="roll"):
        command = mock_game._get_player_command(mock_game.state.players[0])
        assert command == ["roll"]

def test_get_player_command_bot(mock_game):
    """Test getting a command from a bot player."""
    with patch("builtins.print") as mock_print:
        command = mock_game._get_player_command(mock_game.state.players[1])
        assert command == ["roll"]
        mock_print.assert_any_call("Bot (random) is thinking...")

def test_handle_save_valid(mock_game):
    """Test the save command with a valid filepath."""
    with patch("ludo.game.save_game") as mock_save:
        mock_game._handle_save(["save", "my_game.json"])
        mock_save.assert_called_once_with(mock_game.state, "my_game.json")

def test_handle_save_invalid(mock_game):
    """Test the save command with a missing filepath."""
    with patch("ludo.game.save_game") as mock_save, \
         patch("builtins.print") as mock_print:
        mock_game._handle_save(["save"])
        mock_save.assert_not_called()
        mock_print.assert_called_with("Error: Missing filepath. Usage: save <filepath>")

def test_handle_roll_normal(mock_game):
    """Test the roll command for a normal roll."""
    mock_game.dice.roll.return_value = 4
    with patch("ludo.game.Game.play_turn") as mock_play_turn, \
         patch("builtins.print") as mock_print:
        mock_game._handle_roll(mock_game.state.players[0])
        mock_print.assert_any_call("Rolled a 4")
        mock_play_turn.assert_called_once_with(4)

def test_handle_roll_extra_turn(mock_game):
    """Test the roll command when a 6 is rolled, granting an extra turn."""
    mock_game.dice.roll.return_value = 6
    # Ensure the player index doesn't change
    mock_game.state.current_player_index = 0
    with patch("ludo.game.Game.play_turn", side_effect=lambda _: setattr(mock_game.state, 'current_player_index', 0)), \
         patch("builtins.print") as mock_print:
        mock_game._handle_roll(mock_game.state.players[0])
        mock_print.assert_any_call("Got an extra turn for rolling a 6.")

def test_handle_roll_three_sixes_forfeit(mock_game):
    """Test that rolling three consecutive sixes forfeits the turn."""
    mock_game.dice.roll.return_value = 6
    # Simulate player index changing
    with patch("ludo.game.Game.play_turn", side_effect=lambda _: setattr(mock_game.state, 'current_player_index', 1)), \
         patch("builtins.print") as mock_print:
        mock_game._handle_roll(mock_game.state.players[0])
        mock_print.assert_any_call("Rolled three consecutive 6s. Forfeiting turn.")

def test_handle_roll_win(mock_game):
    """Test the roll command when the game is won."""
    mock_game.dice.roll.return_value = 1
    def set_game_over(_):
        mock_game.state.is_game_over = True

    with patch("ludo.game.Game.play_turn", side_effect=set_game_over), \
         patch("builtins.print") as mock_print:
        mock_game._handle_roll(mock_game.state.players[0])
        mock_print.assert_any_call("--- Player RED wins! ---")

def test_cli_loop_quit(mock_game):
    """Test that the CLI loop can be exited with 'quit'."""
    with patch("ludo.game.Game._get_player_command", return_value=["quit"]), \
         patch("builtins.print") as mock_print:
        mock_game.loop_cli()
        mock_print.assert_any_call("Quitting game.")

def test_cli_loop_invalid_command(mock_game):
    """Test that the CLI loop handles unknown commands for human players."""
    # Simulate a sequence of commands: an invalid one, then quit
    commands = [["foobar"], ["quit"]]
    with patch("ludo.game.Game._get_player_command", side_effect=commands), \
         patch("builtins.print") as mock_print:
        mock_game.loop_cli()
        mock_print.assert_any_call("Unknown command: foobar")
