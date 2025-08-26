import pytest
from ludo.game import Game
from ludo.dice import Dice
from ludo.utils.constants import PieceState, PlayerColor
from ludo.board import START_SQUARES

@pytest.fixture
def game():
    """Returns a game instance with a fresh state."""
    g = Game(players=["red", "green"], dice=Dice())
    # Let's work with the RED player for consistency
    g.state.current_player_index = 0
    return g

def test_move_piece_from_yard(game):
    """
    Tests moving a piece from the YARD to its starting position on the board.
    """
    piece_to_move = game.state.players[0].pieces[0]

    # Pre-condition
    assert piece_to_move.state == PieceState.YARD
    assert piece_to_move.position == -1

    game.move_piece(piece_to_move, roll=6)

    # Post-condition
    assert piece_to_move.state == PieceState.TRACK
    expected_position = START_SQUARES[PlayerColor.RED]
    assert piece_to_move.position == expected_position


def test_move_piece_on_track(game):
    """
    Tests moving a piece that is already on the main track.
    """
    player = game.state.players[0]
    piece_to_move = player.pieces[0]

    # Setup: Place a piece on the track
    piece_to_move.state = PieceState.TRACK
    piece_to_move.position = 10
    roll = 4
    game.move_piece(piece_to_move, roll)

    # Post-condition
    assert piece_to_move.state == PieceState.TRACK
    assert piece_to_move.position == 14
