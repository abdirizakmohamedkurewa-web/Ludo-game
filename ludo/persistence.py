"""
Save/load (JSON).
"""
import json
from dataclasses import asdict
from typing import Union
from pathlib import Path
from ludo.state import GameState


def save_game(state: GameState, filepath: Union[str, Path]) -> None:
    """
    Saves the game state to a JSON file.

    Args:
        state: The GameState object to save.
        filepath: The path to the file where the game will be saved.
    """
    game_data = state.to_serializable()
    data_dict = asdict(game_data)
    with open(filepath, "w") as f:
        json.dump(data_dict, f, indent=4)
