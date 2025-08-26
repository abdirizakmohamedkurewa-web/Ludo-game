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
