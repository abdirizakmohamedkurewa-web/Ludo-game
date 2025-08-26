import pytest
from ludo.game import Game
from ludo.dice import Dice
from ludo.rules import Rules
from ludo.utils.constants import PieceState

@pytest.fixture
def game():
    """Returns a game instance with a fresh state."""
    return Game(players=["red", "green"], dice=Dice())

def test_enter_from_yard_on_roll_6(game):
    """
    Tests that a piece can enter from the yard if a 6 is rolled.
    """
    game.state.dice_roll = 6
    current_player = game.state.players[game.state.current_player_index]

    # Pre-condition: Ensure piece is in the yard
    piece_in_yard = current_player.pieces[0]
    assert piece_in_yard.state == PieceState.YARD

    legal_moves = Rules.get_legal_moves(game.state, game.state.dice_roll)

    assert piece_in_yard in legal_moves

def test_enter_from_yard_on_roll_not_6(game):
    """
    Tests that a piece cannot enter from the yard if the roll is not a 6.
    """
    game.state.dice_roll = 5
    current_player = game.state.players[game.state.current_player_index]

    # Pre-condition: Ensure piece is in the yard
    piece_in_yard = current_player.pieces[0]
    assert piece_in_yard.state == PieceState.YARD

    legal_moves = Rules.get_legal_moves(game.state, game.state.dice_roll)

    assert piece_in_yard not in legal_moves


def test_yard_exit_has_priority_on_roll_6(game):
    """
    Tests that if a 6 is rolled, moving a piece from the yard is the only
    legal move if there are pieces in the yard.
    """
    game.state.dice_roll = 6
    current_player = game.state.players[game.state.current_player_index]

    # Set up the board state: one piece in yard, three on the track
    piece_in_yard = current_player.pieces[0]
    piece_on_track1 = current_player.pieces[1]
    piece_on_track2 = current_player.pieces[2]
    piece_on_track3 = current_player.pieces[3]

    piece_in_yard.state = PieceState.YARD
    piece_on_track1.state = PieceState.TRACK
    piece_on_track1.position = 10
    piece_on_track2.state = PieceState.TRACK
    piece_on_track2.position = 12
    piece_on_track3.state = PieceState.TRACK
    piece_on_track3.position = 14

    # Get legal moves
    legal_moves = Rules.get_legal_moves(game.state, game.state.dice_roll)

    # Assert that only the yard piece is a legal move
    assert len(legal_moves) == 1
    assert piece_in_yard in legal_moves
    assert piece_on_track1 not in legal_moves
