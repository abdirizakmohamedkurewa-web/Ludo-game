"""
Board layout, piece movement calculations.
"""

from ludo.utils.constants import PlayerColor

# The main track has 52 squares (0-51)
TRACK_LENGTH = 52

# Entry squares for each color
START_SQUARES = {
    PlayerColor.RED: 0,
    PlayerColor.GREEN: 13,
    PlayerColor.YELLOW: 26,
    PlayerColor.BLUE: 39,
}

# The square before a piece enters its home column
HOME_ENTRY_SQUARES = {
    PlayerColor.RED: 51,
    PlayerColor.GREEN: 12,
    PlayerColor.YELLOW: 25,
    PlayerColor.BLUE: 38,
}

# The home column has 6 squares (52-57)
HOME_COLUMN_LENGTH = 6

# Squares that are safe from captures
SAFE_SQUARES = {
    START_SQUARES[PlayerColor.RED] + 8,
    START_SQUARES[PlayerColor.GREEN] + 8,
    START_SQUARES[PlayerColor.YELLOW] + 8,
    START_SQUARES[PlayerColor.BLUE] + 8,
} | set(START_SQUARES.values())
