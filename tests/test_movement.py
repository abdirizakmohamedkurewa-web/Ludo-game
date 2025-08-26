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
