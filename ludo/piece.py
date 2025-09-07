"""
Piece entity & transitions.
"""

from __future__ import annotations

from dataclasses import dataclass

from ludo.serialization import PieceData
from ludo.utils.constants import PieceState, PlayerColor


@dataclass
class Piece:
    """Represents a single game piece."""

    id: int
    color: PlayerColor
    state: PieceState = PieceState.YARD
    position: int = -1  # -1 for YARD, 0-51 for track, 52-57 for home column

    def to_serializable(self) -> PieceData:
        """Converts the Piece to a serializable PieceData object."""
        return PieceData(
            id=self.id,
            color=self.color.name,
            state=self.state.name,
            position=self.position,
        )

    @classmethod
    def from_serializable(cls, data: PieceData) -> Piece:
        """Creates a Piece from a serializable PieceData object."""
        return cls(
            id=data.id,
            color=PlayerColor[data.color],
            state=PieceState[data.state],
            position=data.position,
        )
