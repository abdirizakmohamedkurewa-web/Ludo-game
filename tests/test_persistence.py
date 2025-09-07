"""
Tests for game state persistence.
"""

import json
from pathlib import Path

from ludo.bots.human_bot import HumanBot
from ludo.dice import Dice
from ludo.game import Game
from ludo.persistence import load_game, save_game
from ludo.player import Player
from ludo.utils.constants import PieceState, PlayerColor


def test_save_game(tmp_path: Path):
    """
    Tests that a game state can be saved to a JSON file.
    """
    # 1. Create a GameState
    players = [
        Player(color=PlayerColor.RED, role="human"),
        Player(color=PlayerColor.GREEN, role="human"),
    ]
    strategies = [HumanBot(), HumanBot()]
    game = Game(players=players, strategies=strategies, dice=Dice(seed=123))
    state = game.state
    state.dice_roll = 5
    state.current_player_index = 1
    state.is_game_over = False
    state.consecutive_sixes = 1

    # 2. Save the state to a temporary file
    save_file = tmp_path / "save.json"
    save_game(state, save_file)

    # 3. Read the file and parse the JSON
    with open(save_file, "r") as f:
        saved_data = json.load(f)

    # 4. Assert the contents are correct
    assert saved_data["schema_version"] == "1.0"
    assert saved_data["dice_seed"] == 123
    assert saved_data["current_player_index"] == 1
    assert saved_data["dice_roll"] == 5
    assert not saved_data["is_game_over"]
    assert saved_data["consecutive_sixes"] == 1

    # Check player data
    players = saved_data["players"]
    assert len(players) == 2
    assert players[0]["color"] == PlayerColor.RED.name
    assert players[1]["color"] == PlayerColor.GREEN.name

    # Check piece data for the first player
    pieces = players[0]["pieces"]
    assert len(pieces) == 4
    for i, piece in enumerate(pieces):
        assert piece["id"] == i
        assert piece["color"] == PlayerColor.RED.name
        assert piece["state"] == "YARD"
        assert piece["position"] == -1


def test_save_and_load_game(tmp_path: Path):
    """
    Tests that a game state can be saved and then loaded,
    resulting in an identical state.
    """
    # 1. Create an original GameState with some non-default values
    players = [
        Player(color=PlayerColor.BLUE, role="human"),
        Player(color=PlayerColor.YELLOW, role="human"),
    ]
    strategies = [HumanBot(), HumanBot()]
    game = Game(players=players, strategies=strategies, dice=Dice(seed=456))
    original_state = game.state
    original_state.dice_roll = 4
    original_state.current_player_index = 1
    original_state.consecutive_sixes = 2

    # Modify a piece's state to ensure deep parts of the state are saved/loaded
    piece_to_move = original_state.players[0].pieces[2]
    piece_to_move.state = PieceState.TRACK
    piece_to_move.position = 25

    # 2. Save the state to a temporary file
    save_file = tmp_path / "save.json"
    save_game(original_state, save_file)

    # 3. Load the state back
    loaded_state = load_game(save_file)

    # 4. Assert that the loaded state is identical to the original
    # The GameState is a dataclass, so __eq__ should perform a deep comparison
    assert loaded_state == original_state
