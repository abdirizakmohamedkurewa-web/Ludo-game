"""
Save/load (JSON).
"""
import json
from dataclasses import asdict
from typing import Union
from pathlib import Path

from ludo.serialization import GameData, PieceData, PlayerData
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


def load_game(filepath: Union[str, Path]) -> GameState:
    """
    Loads a game state from a JSON file.

    Args:
        filepath: The path to the file from which to load the game.

    Returns:
        The loaded GameState object.
    """
    with open(filepath, "r") as f:
        data_dict = json.load(f)

    # Reconstruct the nested dataclasses from the dictionary
    players_data = [
        PlayerData(
            color=p["color"],
            role=p["role"],
            pieces=[
                PieceData(
                    id=piece["id"],
                    color=piece["color"],
                    state=piece["state"],
                    position=piece["position"],
                )
                for piece in p["pieces"]
            ],
        )
        for p in data_dict["players"]
    ]

    game_data = GameData(
        schema_version=data_dict["schema_version"],
        players=players_data,
        current_player_index=data_dict["current_player_index"],
        dice_roll=data_dict["dice_roll"],
        is_game_over=data_dict["is_game_over"],
        consecutive_sixes=data_dict["consecutive_sixes"],
        dice_seed=data_dict["dice_seed"],
    )

    return GameState.from_serializable(game_data)
