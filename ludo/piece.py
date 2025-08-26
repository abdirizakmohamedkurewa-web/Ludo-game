"""
Piece entity & transitions.
"""
from dataclasses import dataclass
from ludo.utils.constants import PlayerColor, PieceState


@dataclass
class Piece:
    """Represents a single game piece."""
    id: int
    color: PlayerColor
    state: PieceState = PieceState.YARD
    position: int = -1  # -1 for YARD, 0-51 for track, 52-57 for home column
