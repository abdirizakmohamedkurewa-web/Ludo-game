import pytest

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

    # Check if the move (piece, destination) exists
    assert any(p == piece_in_yard for p, d in legal_moves)
    # Check that the destination is the start square for that player
    start_square = 0  # Red's start square
    assert any(d == start_square for p, d in legal_moves if p == piece_in_yard)


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

    assert not any(p == piece_in_yard for p, d in legal_moves)


def test_yard_exit_and_other_moves_on_roll_6(game):
    """
    Tests that if a 6 is rolled, moving a piece from the yard is a
    legal move, as are other pieces on the board.
    """
    game.state.dice_roll = 6
    current_player = game.state.players[game.state.current_player_index]

    # Set up the board state: one piece in yard, one on the track
    piece_in_yard = current_player.pieces[0]
    piece_on_track = current_player.pieces[1]

    piece_in_yard.state = PieceState.YARD
    piece_on_track.state = PieceState.TRACK
    piece_on_track.position = 10

    # Get legal moves
    legal_moves = Rules.get_legal_moves(game.state, game.state.dice_roll)
    legal_pieces = [p for p, d in legal_moves]

    # Assert that both the yard piece and track piece are legal moves
    assert len(legal_moves) == 2
    assert piece_in_yard in legal_pieces
    assert piece_on_track in legal_pieces


def test_move_is_blocked_by_opponent_blockade(game):
    """
    Tests that a piece cannot pass a blockade of two opponent pieces.
    """
    # Player 1 (red) is at the start
    red_player = game.state.players[0]
    red_piece = red_player.pieces[0]
    red_piece.state = PieceState.TRACK
    red_piece.position = 0

    # Player 2 (green) has a blockade at position 2
    green_player = game.state.players[1]
    green_piece1 = green_player.pieces[0]
    green_piece2 = green_player.pieces[1]
    green_piece1.state = PieceState.TRACK
    green_piece1.position = 2
    green_piece2.state = PieceState.TRACK
    green_piece2.position = 2

    # Attempt to move the red piece by rolling a 4 (would pass the blockade)
    roll = 4
    legal_moves = Rules.get_legal_moves(game.state, roll, use_blocking_rule=True)

    # The move should be illegal
    assert not any(p == red_piece for p, d in legal_moves)


def test_move_is_not_blocked_if_rule_is_disabled(game):
    """
    Tests that a piece can pass an opponent blockade if the rule is disabled.
    """
    # Player 1 (red) is at the start
    red_player = game.state.players[0]
    red_piece = red_player.pieces[0]
    red_piece.state = PieceState.TRACK
    red_piece.position = 0

    # Player 2 (green) has a blockade at position 2
    green_player = game.state.players[1]
    green_piece1 = green_player.pieces[0]
    green_piece2 = green_player.pieces[1]
    green_piece1.state = PieceState.TRACK
    green_piece1.position = 2
    green_piece2.state = PieceState.TRACK
    green_piece2.position = 2

    # Attempt to move the red piece by rolling a 4 (would pass the blockade)
    roll = 4
    legal_moves = Rules.get_legal_moves(game.state, roll, use_blocking_rule=False)

    # The move should be legal
    assert any(p == red_piece for p, d in legal_moves)


def test_capture_opponent_piece(game):
    """
    Tests that landing on a square with an opponent's piece captures it,
    sending it back to the yard.
    """
    red_player = game.state.players[0]
    red_piece = red_player.pieces[0]
    red_piece.state = PieceState.TRACK
    red_piece.position = 10

    green_player = game.state.players[1]
    green_piece = green_player.pieces[0]
    green_piece.state = PieceState.TRACK
    green_piece.position = 12  # This is not a safe square

    # Move the red piece to land on the green piece
    move_piece(game.state, red_piece, 2)

    # Check that the red piece moved and the green piece was captured
    assert red_piece.position == 12
    assert green_piece.state == PieceState.YARD
    assert green_piece.position == -1  # Standard representation for yard


def test_no_capture_on_safe_square(game):
    """
    Tests that landing on a safe square with an opponent's piece
    does not capture it.
    """
    red_player = game.state.players[0]
    red_piece = red_player.pieces[0]
    red_piece.state = PieceState.TRACK
    red_piece.position = 10

    green_player = game.state.players[1]
    green_piece = green_player.pieces[0]
    green_piece.state = PieceState.TRACK
    green_piece.position = 13  # Green's start square, which is a safe square

    # Move the red piece to land on the green piece on a safe square
    move_piece(game.state, red_piece, 3)

    # The red piece should move, but the green piece should not be captured
    assert red_piece.position == 13
    assert green_piece.state == PieceState.TRACK  # State is unchanged
    assert green_piece.position == 13  # Position is unchanged


def test_move_is_blocked_by_distant_blockade(game):
    """
    Tests that a piece cannot pass a blockade even if it's far away.
    """
    red_player = game.state.players[0]
    red_piece = red_player.pieces[0]
    red_piece.state = PieceState.TRACK
    red_piece.position = 0

    # Player 2 (green) has a blockade at position 5
    green_player = game.state.players[1]
    green_piece1 = green_player.pieces[0]
    green_piece2 = green_player.pieces[1]
    green_piece1.state = PieceState.TRACK
    green_piece1.position = 5
    green_piece2.state = PieceState.TRACK
    green_piece2.position = 5

    # Attempt to move the red piece by rolling a 6 (would pass the blockade)
    roll = 6
    legal_moves = Rules.get_legal_moves(game.state, roll, use_blocking_rule=True)

    # The move should be illegal
    assert not any(p == red_piece for p, d in legal_moves)


def test_move_is_not_blocked_by_own_pieces(game):
    """
    Tests that a player is not blocked by a blockade of their own pieces.
    """
    # Player 1 (red) is at the start and also has a blockade
    red_player = game.state.players[0]
    red_piece_to_move = red_player.pieces[0]
    red_blockade_1 = red_player.pieces[1]
    red_blockade_2 = red_player.pieces[2]

    red_piece_to_move.state = PieceState.TRACK
    red_piece_to_move.position = 0

    red_blockade_1.state = PieceState.TRACK
    red_blockade_1.position = 2
    red_blockade_2.state = PieceState.TRACK
    red_blockade_2.position = 2

    # Attempt to move the piece by rolling a 4 (would pass the 'blockade')
    roll = 4
    legal_moves = Rules.get_legal_moves(game.state, roll, use_blocking_rule=True)

    # The move should be legal as it's not an opponent's blockade
    assert any(p == red_piece_to_move for p, d in legal_moves)


def test_piece_moves_from_track_to_home_column(game):
    """
    Tests that a piece correctly enters the home column from the main track.
    """
    red_player = game.state.players[0]
    red_piece = red_player.pieces[0]

    # Position the piece near the home entry (pos 50 for red)
    red_piece.state = PieceState.TRACK
    red_piece.position = 50

    # --- Case 1: Enter the middle of the home column ---
    roll_enter = 3
    legal_moves_enter = Rules.get_legal_moves(game.state, roll_enter)
    assert any(p == red_piece for p, d in legal_moves_enter)

    # Check destination
    move = next(m for m in legal_moves_enter if m[0] == red_piece)
    assert move[1] == 54  # 52 (base) + (50+3-51) = 54

    # --- Case 2: Land exactly in the HOME state from the track ---
    roll_win = 6
    legal_moves_win = Rules.get_legal_moves(game.state, roll_win)
    assert any(p == red_piece for p, d in legal_moves_win)

    move = next(m for m in legal_moves_win if m[0] == red_piece)
    assert move[1] == 57  # 52 (base) + (50+6-51) = 57


def test_home_column_exact_roll(game):
    """
    Tests that a piece can move within the home column.
    """
    red_player = game.state.players[0]
    red_piece = red_player.pieces[0]

    # Position the piece 2 steps away from HOME (pos 55)
    red_piece.state = PieceState.HOME_COLUMN
    red_piece.position = 55  # Needs a roll of 2 to win

    # Attempt to move with a roll of 1
    roll = 1
    legal_moves = Rules.get_legal_moves(game.state, roll)
    assert any(p == red_piece for p, d in legal_moves)

    move = next(m for m in legal_moves if m[0] == red_piece)
    assert move[1] == 56  # 55 + 1 = 56

    # Attempt to move with a roll that is too high
    too_high_roll = 3
    legal_moves_bad = Rules.get_legal_moves(game.state, too_high_roll)

    # The move should be illegal as it overshoots
    assert not any(p == red_piece for p, d in legal_moves_bad)


def test_move_is_not_blocked_by_single_opponent_piece(game):
    """
    Tests that a single opponent piece does not constitute a blockade.
    """
    # Player 1 (red) is at the start
    red_player = game.state.players[0]
    red_piece = red_player.pieces[0]
    red_piece.state = PieceState.TRACK
    red_piece.position = 0

    # Player 2 (green) has a single piece at position 2
    green_player = game.state.players[1]
    green_piece1 = green_player.pieces[0]
    green_piece1.state = PieceState.TRACK
    green_piece1.position = 2

    # Attempt to move the red piece by rolling a 4 (would pass the piece)
    roll = 4
    legal_moves = Rules.get_legal_moves(game.state, roll, use_blocking_rule=True)

    # The move should be legal
    assert any(p == red_piece for p, d in legal_moves)


def test_move_lands_on_blockade(game):
    """
    Tests that a piece can land on a square that has a blockade.
    The rule is that you cannot *pass* a blockade.
    """
    # Player 1 (red) is at the start
    red_player = game.state.players[0]
    red_piece = red_player.pieces[0]
    red_piece.state = PieceState.TRACK
    red_piece.position = 0

    # Player 2 (green) has a blockade at position 2
    green_player = game.state.players[1]
    green_piece1 = green_player.pieces[0]
    green_piece2 = green_player.pieces[1]
    green_piece1.state = PieceState.TRACK
    green_piece1.position = 2
    green_piece2.state = PieceState.TRACK
    green_piece2.position = 2

    # Attempt to move the red piece by rolling a 2 (lands on the blockade)
    roll = 2
    legal_moves = Rules.get_legal_moves(game.state, roll, use_blocking_rule=True)

    # The move should be legal
    assert any(p == red_piece for p, d in legal_moves)
