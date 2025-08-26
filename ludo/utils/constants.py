"""
Game constants (safe squares, paths, colors, etc.).
"""
from enum import Enum, auto


class PlayerColor(Enum):
    RED = auto()
    GREEN = auto()
    YELLOW = auto()
    BLUE = auto()


class PieceState(Enum):
    YARD = auto()
    TRACK = auto()
    HOME_COLUMN = auto()
    HOME = auto()
