"""
Tests for game state persistence.
"""
import json
from pathlib import Path
from ludo.game import Game
from ludo.dice import Dice
from ludo.persistence import save_game
from ludo.utils.constants import PlayerColor


def test_save_game(tmp_path: Path):
    """
    Tests that a game state can be saved to a JSON file.
    """
    # 1. Create a GameState
    game = Game(players=["red", "green"], dice=Dice(seed=123))
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
    assert players[0]["color"] == PlayerColor.RED.value
    assert players[1]["color"] == PlayerColor.GREEN.value

    # Check piece data for the first player
    pieces = players[0]["pieces"]
    assert len(pieces) == 4
    for i, piece in enumerate(pieces):
        assert piece["id"] == i
        assert piece["color"] == PlayerColor.RED.value
        assert piece["state"] == "YARD"
        assert piece["position"] == -1
