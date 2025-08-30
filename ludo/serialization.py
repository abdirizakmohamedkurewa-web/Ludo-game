"""
Dataclasses for game state serialization (JSON).
"""
from dataclasses import dataclass
from typing import List, Optional

SCHEMA_VERSION = "1.0"


@dataclass
class PieceData:
    """Serializable representation of a Piece."""
    id: int
    color: str  # PlayerColor.value
    state: str  # PieceState.value
    position: int


@dataclass
class PlayerData:
    """Serializable representation of a Player."""
    color: str  # PlayerColor.value
    pieces: List[PieceData]


@dataclass
class GameData:
    """Serializable representation of a GameState."""
    schema_version: str
    players: List[PlayerData]
    current_player_index: int
    dice_roll: Optional[int]
    is_game_over: bool
    consecutive_sixes: int
    dice_seed: Optional[int]
