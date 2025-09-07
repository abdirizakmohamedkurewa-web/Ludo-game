import pytest

from ludo.board import HOME_COLUMN_LENGTH
from ludo.bots.human_bot import HumanBot
from ludo.dice import Dice
from ludo.game import Game
from ludo.move import move_piece
from ludo.player import Player
from ludo.rules import Rules
from ludo.utils.constants import PieceState, PlayerColor


@pytest.fixture
def game():
    """Returns a game instance with a fresh state."""
    players = [
        Player(color=PlayerColor.RED, role="human"),
        Player(color=PlayerColor.GREEN, role="human"),
    ]
    strategies = [HumanBot(), HumanBot()]
    return Game(players=players, strategies=strategies, dice=Dice())


def test_piece_requires_exact_roll_to_enter_home(game):
    """
    Tests that a piece in the home column requires an exact roll to move to HOME.
    """
    current_player = game.state.players[0]
    piece = current_player.pieces[0]

    # Position the piece 2 steps away from HOME
    piece.state = PieceState.HOME_COLUMN
    piece.position = 52 + (HOME_COLUMN_LENGTH - 1 - 2)  # 2 steps away from the end

    # A roll of 2 should be legal
    legal_moves_2 = Rules.get_legal_moves(game.state, 2)
    assert any(p == piece for p, d in legal_moves_2)

    # A roll of 3 should be illegal (overshoots)
    legal_moves_3 = Rules.get_legal_moves(game.state, 3)
    assert not any(p == piece for p, d in legal_moves_3)


def test_move_overshooting_home_is_illegal(game):
    """
    Tests that a move from the track is illegal if it overshoots the home column.
    """
    current_player = game.state.players[0]
    piece = current_player.pieces[0]

    # Position the piece on the track, 2 steps from its home entry
    piece.state = PieceState.TRACK
    piece.position = 51 - 2  # 2 steps before home entry square for RED (pos 49)

    # A roll of 5 should be legal (lands inside home column)
    # new_progress = 49 + 5 = 54. home_col_pos = 54-51 = 3. Legal.
    legal_moves_5 = Rules.get_legal_moves(game.state, 5)
    assert any(p == piece for p, d in legal_moves_5)

    # A roll of 9 should be illegal (overshoots)
    # new_progress = 49 + 9 = 58. home_col_pos = 58-51 = 7. Illegal.
    legal_moves_9 = Rules.get_legal_moves(game.state, 9)
    assert not any(p == piece for p, d in legal_moves_9)


def test_player_wins_when_all_pieces_are_home(game):
    """
    Tests that the game is marked as over when a player gets all pieces home.
    """
    current_player = game.state.players[0]

    # Set all but one piece to HOME
    for i in range(3):
        current_player.pieces[i].state = PieceState.HOME

    # Position the last piece one step away from HOME
    last_piece = current_player.pieces[3]
    last_piece.state = PieceState.HOME_COLUMN
    last_piece.position = 52 + (HOME_COLUMN_LENGTH - 1 - 1)

    # Pre-condition: game is not over
    assert not game.state.is_game_over

    # Move the last piece to HOME
    move_piece(game.state, last_piece, 1)

    # Post-condition: game is over
    assert game.state.is_game_over


def test_game_not_over_if_not_all_pieces_home(game):
    """
    Tests that the game does not end if a player has some, but not all, pieces home.
    """
    current_player = game.state.players[0]

    # Set two pieces to HOME
    current_player.pieces[0].state = PieceState.HOME
    current_player.pieces[1].state = PieceState.HOME

    # Position one piece on the track
    last_piece = current_player.pieces[2]
    last_piece.state = PieceState.TRACK
    last_piece.position = 20

    # Move the piece
    move_piece(game.state, last_piece, 3)

    assert not game.state.is_game_over
