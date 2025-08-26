import pytest
from ludo.game import Game
from ludo.rules import Rules
from ludo.utils.constants import PieceState

@pytest.fixture
def game():
    """Returns a game instance with a fresh state."""
    return Game()

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
