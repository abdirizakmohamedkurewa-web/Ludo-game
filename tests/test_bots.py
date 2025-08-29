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
