import pytest

from ludo.board import START_SQUARES
from ludo.bots.human_bot import HumanBot
from ludo.dice import Dice
from ludo.game import Game
from ludo.move import move_piece
from ludo.player import Player
from ludo.utils.constants import PieceState, PlayerColor


@pytest.fixture
def game():
    """Returns a game instance with a fresh state."""
    players = [
        Player(color=PlayerColor.RED, role="human"),
        Player(color=PlayerColor.GREEN, role="human"),
    ]
    strategies = [HumanBot(), HumanBot()]
    g = Game(players=players, strategies=strategies, dice=Dice())
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

    move_piece(game.state, piece_to_move, roll=6)

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
    move_piece(game.state, piece_to_move, roll)

    # Post-condition
    assert piece_to_move.state == PieceState.TRACK
    assert piece_to_move.position == 14
