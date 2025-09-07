"""
Defines the pixel coordinates for the Ludo board layout.
"""

from apps.gui.constants import GRID_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH
from ludo.utils.constants import PlayerColor

# A 15x15 grid forms the basis of the board
GRID_COUNT = 15
BOARD_SIZE = GRID_COUNT * GRID_SIZE
BOARD_X_START = (SCREEN_WIDTH - BOARD_SIZE) / 2
BOARD_Y_START = (SCREEN_HEIGHT - BOARD_SIZE) / 2


def grid_to_pixel(row, col):
    """Converts grid coordinates (row, col) to pixel coordinates (x, y)."""
    x = BOARD_X_START + col * GRID_SIZE
    y = BOARD_Y_START + row * GRID_SIZE
    return x, y


# Define the grid coordinates for the main track (52 squares)
# The path starts at Red's entry point and moves clockwise.
_track_grid_coords = [
    (13, 6),
    (12, 6),
    (11, 6),
    (10, 6),
    (9, 6),
    (8, 6),  # Red home arm
    (8, 5),
    (8, 4),
    (8, 3),
    (8, 2),
    (8, 1),
    (8, 0),  # Bottom-left turn
    (7, 0),  # Green entry arm corner
    (6, 0),
    (6, 1),
    (6, 2),
    (6, 3),
    (6, 4),
    (6, 5),  # Green home arm
    (5, 6),
    (4, 6),
    (3, 6),
    (2, 6),
    (1, 6),
    (0, 6),  # Top-left turn
    (0, 7),  # Yellow entry arm corner
    (0, 8),
    (1, 8),
    (2, 8),
    (3, 8),
    (4, 8),
    (5, 8),  # Yellow home arm
    (6, 9),
    (6, 10),
    (6, 11),
    (6, 12),
    (6, 13),
    (6, 14),  # Top-right turn
    (7, 14),  # Blue entry arm corner
    (8, 14),
    (8, 13),
    (8, 12),
    (8, 11),
    (8, 10),
    (8, 9),  # Blue home arm
    (9, 8),
    (10, 8),
    (11, 8),
    (12, 8),
    (13, 8),
    (14, 8),  # Bottom-right turn
    (14, 7),  # Red entry arm corner
]

# Define home column grid coordinates for each color
_home_column_grid_coords = {
    PlayerColor.RED: [(13, 7), (12, 7), (11, 7), (10, 7), (9, 7), (8, 7)],
    PlayerColor.GREEN: [(7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6)],
    PlayerColor.YELLOW: [(1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7)],
    PlayerColor.BLUE: [(7, 13), (7, 12), (7, 11), (7, 10), (7, 9), (7, 8)],
}

# Define yard grid coordinates for each color (4 positions per yard)
_yard_grid_coords = {
    PlayerColor.RED: [(10, 2), (10, 3), (11, 2), (11, 3)],
    PlayerColor.GREEN: [(2, 2), (2, 3), (3, 2), (3, 3)],
    PlayerColor.YELLOW: [(2, 10), (2, 11), (3, 10), (3, 11)],
    PlayerColor.BLUE: [(10, 10), (10, 11), (11, 10), (11, 11)],
}


# --- EXPORTED COORDINATES ---

# Convert all grid coordinates to pixel coordinates for export
TRACK_COORDINATES = [grid_to_pixel(r, c) for r, c in _track_grid_coords]

HOME_COLUMN_COORDINATES = {
    color: [grid_to_pixel(r, c) for r, c in coords]
    for color, coords in _home_column_grid_coords.items()
}

YARD_COORDINATES = {
    color: [grid_to_pixel(r, c) for r, c in coords] for color, coords in _yard_grid_coords.items()
}
