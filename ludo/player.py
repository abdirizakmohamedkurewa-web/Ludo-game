"""
Player entity, color, pieces.
"""
from dataclasses import dataclass, field
from typing import List
from ludo.piece import Piece
from ludo.utils.constants import PlayerColor


@dataclass
class Player:
    """Represents a player in the game."""
    color: PlayerColor
    pieces: List[Piece] = field(default_factory=list)

    def __post_init__(self):
        if not self.pieces:
            self.pieces = [Piece(id=i, color=self.color) for i in range(4)]
