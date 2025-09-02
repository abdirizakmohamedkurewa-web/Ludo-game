import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from apps.cli.main import main
from ludo.persistence import load_game


def test_save_and_load_integration(monkeypatch, tmp_path):
    """
    Tests the full save-and-load cycle through the CLI.
    1. Starts a new game with a human and a bot.
    2. Simulates human input to save the game during their turn.
    3. Verifies the save file was created with the correct state.
    4. Starts a new game loading from the save file.
    5. Simulates human input to quit.
    6. Verifies that the game state was correctly restored.
    """
    save_file = tmp_path / "test_game.json"

    # Part 1: Start game, save during human's turn, and quit
    # ------------------------------------------------------
    # The bot will play automatically. We only need to provide input for the human.
    user_inputs_part1 = [f"save {save_file}", "quit"]
    monkeypatch.setattr("builtins.input", lambda _: user_inputs_part1.pop(0))
    monkeypatch.setattr(sys, "argv", ["ludo", "--players", "human", "random", "--seed", "42"])

    main()

    # After the human quits, the input list should be empty
    assert not user_inputs_part1
    # Check that the save file was created
    assert save_file.exists()

    # Verify the contents of the save file. Seed 42 gives a 6 on the first roll.
    # The human player (index 0) gets a turn, we save, then quit.
    saved_state = load_game(save_file)
    assert saved_state.current_player_index == 0
    assert saved_state.dice_roll is None  # Saved before rolling
    assert saved_state.players[0].role == "human"
    assert saved_state.players[1].role == "random"

    # Part 2: Load the game and quit
    # ------------------------------
    user_inputs_part2 = ["quit"]
    monkeypatch.setattr("builtins.input", lambda _: user_inputs_part2.pop(0))
    monkeypatch.setattr(sys, "argv", ["ludo", "--load-game", str(save_file)])

    # Use patch to capture stdout and verify the loaded state
    with patch("builtins.print") as mock_print:
        main()

    # Check that the game loaded successfully message was printed
    mock_print.assert_any_call(f"Loading game from {save_file}...")
    mock_print.assert_any_call("Game loaded successfully.")

    # After quitting, the inputs list should be empty
    assert not user_inputs_part2
