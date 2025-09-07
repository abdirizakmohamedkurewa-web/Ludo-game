"""
Dataclasses for GameState, TurnState, etc.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from ludo.player import Player
from ludo.serialization import SCHEMA_VERSION, GameData


@dataclass
class GameState:
    """Represents the complete state of the game at a point in time."""

    players: List[Player]
    current_player_index: int = 0
    dice_roll: Optional[int] = None
    is_game_over: bool = False
    consecutive_sixes: int = 0
    dice_seed: Optional[int] = None

    def to_serializable(self) -> GameData:
        """Converts the GameState to a serializable GameData object."""
        return GameData(
            schema_version=SCHEMA_VERSION,
            players=[p.to_serializable() for p in self.players],
            current_player_index=self.current_player_index,
            dice_roll=self.dice_roll,
            is_game_over=self.is_game_over,
            consecutive_sixes=self.consecutive_sixes,
            dice_seed=self.dice_seed,
        )

    @classmethod
    def from_serializable(cls, data: GameData) -> GameState:
        """Creates a GameState from a serializable GameData object."""
        if data.schema_version != SCHEMA_VERSION:
            raise ValueError(
                f"Schema version mismatch: file has {data.schema_version}, "
                f"code expects {SCHEMA_VERSION}"
            )
        return cls(
            players=[Player.from_serializable(p) for p in data.players],
            current_player_index=data.current_player_index,
            dice_roll=data.dice_roll,
            is_game_over=data.is_game_over,
            consecutive_sixes=data.consecutive_sixes,
            dice_seed=data.dice_seed,
        )


@dataclass
class PlayerState:
    """Represents the state of a single player."""

    pass


@dataclass
class PieceState:
    """Represents the state of a single piece."""

    pass
