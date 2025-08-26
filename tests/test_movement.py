import pytest
from ludo.game import Game
from ludo.dice import Dice
from ludo.player import Player
from ludo.piece import Piece
from ludo.utils.constants import PlayerColor, PieceState


def test_move_piece_on_track():
    # Arrange
    dice = Dice(seed=1)  # Use a fixed seed for predictability
    game = Game(players=['human'], dice=dice)

    # Get the player created by the Game instance
    player = game.state.players[0]
    assert player.color == PlayerColor.RED

    # Get a piece and set it up for the test
    piece_to_move = player.pieces[0]
    piece_to_move.state = PieceState.TRACK
    piece_to_move.position = 10

    roll = 5

    # Act
    game.move_piece(piece_to_move, roll)

    # Assert
    assert piece_to_move.position == 15
    assert piece_to_move.state == PieceState.TRACK


def test_move_piece_into_home_column():
    # Arrange
    dice = Dice(seed=1)
    game = Game(players=['human'], dice=dice)
    player = game.state.players[0]
    assert player.color == PlayerColor.RED

    piece_to_move = player.pieces[0]
    piece_to_move.state = PieceState.TRACK
    piece_to_move.position = 50  # Two squares before RED's home entry

    roll = 3

    # Act
    game.move_piece(piece_to_move, roll)

    # Assert
    # Progress: 50. New progress: 53. Enters home.
    # Home position index: 53 - 51 = 2.
    # Absolute position: 52 (base) + 2 = 54.
    assert piece_to_move.state == PieceState.HOME_COLUMN
    assert piece_to_move.position == 54


def test_move_piece_within_home_column():
    # Arrange
    dice = Dice(seed=1)
    game = Game(players=['human'], dice=dice)
    player = game.state.players[0]
    assert player.color == PlayerColor.RED

    piece_to_move = player.pieces[0]
    piece_to_move.state = PieceState.HOME_COLUMN
    piece_to_move.position = 53  # Corresponds to home column index 1

    roll = 2

    # Act
    game.move_piece(piece_to_move, roll)

    # Assert
    # New home index: 1 + 2 = 3.
    # New absolute position: 52 (base) + 3 = 55.
    assert piece_to_move.state == PieceState.HOME_COLUMN
    assert piece_to_move.position == 55


def test_move_piece_to_home():
    # Arrange
    dice = Dice(seed=1)
    game = Game(players=['human'], dice=dice)
    player = game.state.players[0]
    assert player.color == PlayerColor.RED

    piece_to_move = player.pieces[0]
    piece_to_move.state = PieceState.HOME_COLUMN
    piece_to_move.position = 56  # Corresponds to home column index 4

    roll = 1

    # Act
    game.move_piece(piece_to_move, roll)

    # Assert
    # New home index: 4 + 1 = 5. This is the final HOME spot.
    # New absolute position: 52 (base) + 5 = 57.
    assert piece_to_move.state == PieceState.HOME
    assert piece_to_move.position == 57
