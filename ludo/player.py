"""
Player entity, color, pieces.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
from ludo.piece import Piece
from ludo.utils.constants import PlayerColor
from ludo.serialization import PlayerData


@dataclass
class Player:
    """Represents a player in the game."""
    color: PlayerColor
    pieces: List[Piece] = field(default_factory=list)

    def __post_init__(self):
        if not self.pieces:
            self.pieces = [Piece(id=i, color=self.color) for i in range(4)]

    def to_serializable(self) -> PlayerData:
        """Converts the Player to a serializable PlayerData object."""
        return PlayerData(
            color=self.color.value,
            pieces=[p.to_serializable() for p in self.pieces],
        )

    @classmethod
    def from_serializable(cls, data: PlayerData) -> Player:
        """Creates a Player from a serializable PlayerData object."""
        return cls(
            color=PlayerColor(data.color),
            pieces=[Piece.from_serializable(p) for p in data.pieces],
        )
