"""
Tests for bot strategies.
"""
from typing import List
import pytest
from ludo.bots.base import Strategy
from ludo.piece import Piece
from ludo.state import GameState
from ludo.utils.constants import PlayerColor


class FirstMoveBot:
    """A bot that always chooses the first legal move."""
    def choose_move(self, legal_moves: List[Piece], game_state: GameState) -> Piece:
        if not legal_moves:
            raise ValueError("No legal moves available to choose from.")
        return legal_moves[0]


def test_strategy_protocol_adherence():
    """
    Tests that a class implementing the `choose_move` method
    implicitly satisfies the `Strategy` protocol.
    """
    bot = FirstMoveBot()
    assert isinstance(bot, Strategy)


def test_first_move_bot():
    """
    Tests that the FirstMoveBot correctly chooses the first piece.
    """
    # Create mock pieces. We don't need them to be fully-featured.
    # Using pytest-mock's mocker fixture could be an alternative for more complex cases.
    piece1 = Piece(id=0, color=PlayerColor.RED)
    piece2 = Piece(id=1, color=PlayerColor.RED)
    legal_moves = [piece1, piece2]

    # Create a mock GameState. It's not used by this simple bot, but is required by the signature.
    mock_game_state = GameState(players=[])

    bot = FirstMoveBot()
    chosen_move = bot.choose_move(legal_moves, mock_game_state)

    assert chosen_move is piece1
    assert chosen_move.id == 0


def test_first_move_bot_no_moves():
    """
    Tests that the bot handles the case where there are no legal moves.
    """
    bot = FirstMoveBot()
    mock_game_state = GameState(players=[])
    with pytest.raises(ValueError, match="No legal moves available"):
        bot.choose_move([], mock_game_state)


from ludo.bots.random_bot import RandomBot
from ludo.bots.greedy_bot import GreedyBot
from ludo.player import Player
from ludo.utils.constants import PieceState

def test_random_bot():
    """
    Tests that the RandomBot chooses a move from the legal options.
    """
    # Create mock pieces
    piece1 = Piece(id=0, color=PlayerColor.GREEN)
    piece2 = Piece(id=1, color=PlayerColor.GREEN)
    legal_moves = [piece1, piece2]

    # Create a mock GameState
    mock_game_state = GameState(players=[])

    bot = RandomBot()
    chosen_move = bot.choose_move(legal_moves, mock_game_state)

    assert chosen_move in legal_moves

def test_greedy_bot_chooses_win():
    """Test that the bot chooses a move that wins the game."""
    # Player RED has one piece close to home, another on the track
    p1 = Player(PlayerColor.RED)
    p1.pieces[0].state = PieceState.HOME_COLUMN
    p1.pieces[0].position = 56 # Needs a 1 to win
    p1.pieces[1].state = PieceState.TRACK
    p1.pieces[1].position = 10

    # All other pieces are HOME
    for i in range(2, 4):
        p1.pieces[i].state = PieceState.HOME

    game_state = GameState(players=[p1], dice_roll=1)

    # Legal moves are moving piece 0 or piece 1
    legal_moves = [p1.pieces[0], p1.pieces[1]]

    bot = GreedyBot()
    chosen_move = bot.choose_move(legal_moves, game_state)

    # Bot should choose the winning move
    assert chosen_move is p1.pieces[0]

def test_greedy_bot_chooses_capture():
    """Test that the bot chooses a move that captures an opponent."""
    # Player RED can either capture a GREEN piece or move another piece
    p1 = Player(PlayerColor.RED)
    p1.pieces[0].state = PieceState.TRACK
    p1.pieces[0].position = 10 # Will land on 14
    p1.pieces[1].state = PieceState.TRACK
    p1.pieces[1].position = 20 # Moves to 24

    p2 = Player(PlayerColor.GREEN)
    p2.pieces[0].state = PieceState.TRACK
    p2.pieces[0].position = 14 # Capture target

    game_state = GameState(players=[p1, p2], dice_roll=4)
    legal_moves = [p1.pieces[0], p1.pieces[1]]

    bot = GreedyBot()
    chosen_move = bot.choose_move(legal_moves, game_state)

    # Bot should choose the capture
    assert chosen_move is p1.pieces[0]


def test_greedy_bot_chooses_enter_from_yard():
    """Test that the bot chooses to move a piece from the yard on a 6."""
    p1 = Player(PlayerColor.RED)
    p1.pieces[0].state = PieceState.YARD
    p1.pieces[1].state = PieceState.TRACK
    p1.pieces[1].position = 10

    game_state = GameState(players=[p1], dice_roll=6)
    legal_moves = [p1.pieces[0], p1.pieces[1]]

    bot = GreedyBot()
    chosen_move = bot.choose_move(legal_moves, game_state)

    # Bot should choose to move from the yard
    assert chosen_move is p1.pieces[0]


def test_greedy_bot_chooses_furthest_piece():
    """Test that the bot chooses to move the piece furthest on the track."""
    p1 = Player(PlayerColor.RED)
    p1.pieces[0].state = PieceState.TRACK
    p1.pieces[0].position = 10 # less far
    p1.pieces[1].state = PieceState.TRACK
    p1.pieces[1].position = 30 # more far

    game_state = GameState(players=[p1], dice_roll=2)
    legal_moves = [p1.pieces[0], p1.pieces[1]]

    bot = GreedyBot()
    chosen_move = bot.choose_move(legal_moves, game_state)

    # Bot should choose the piece that is further along
    assert chosen_move is p1.pieces[1]


def test_greedy_bot_capture_tie_break():
    """
    Test that the bot chooses the capture that moves its piece further.
    """
    # Player RED can capture one of two pieces
    p1 = Player(PlayerColor.RED)
    p1.pieces[0].state = PieceState.TRACK
    p1.pieces[0].position = 10 # Will land on 14
    p1.pieces[1].state = PieceState.TRACK
    p1.pieces[1].position = 20 # Will land on 24

    # Opponent pieces to be captured
    p2 = Player(PlayerColor.GREEN)
    p2.pieces[0].state = PieceState.TRACK
    p2.pieces[0].position = 14 # Target 1
    p3 = Player(PlayerColor.BLUE)
    p3.pieces[0].state = PieceState.TRACK
    p3.pieces[0].position = 24 # Target 2

    game_state = GameState(players=[p1, p2, p3], dice_roll=4)
    legal_moves = [p1.pieces[0], p1.pieces[1]]

    bot = GreedyBot()
    chosen_move = bot.choose_move(legal_moves, game_state)

    # Bot should choose the capture that results in a more advanced position
    assert chosen_move is p1.pieces[1]
