from unittest.mock import patch

from ludo.bots.human_bot import HumanBot
from ludo.piece import Piece
from ludo.state import GameState
from ludo.utils.constants import PlayerColor


@patch("builtins.input", side_effect=["1"])
def test_human_bot_chooses_first_move(mock_input):
    """
    Tests that the human bot correctly chooses the first move.
    """
    bot = HumanBot()
    piece1 = Piece(id=0, color=PlayerColor.RED)
    piece2 = Piece(id=1, color=PlayerColor.RED)
    legal_moves = [(piece1, 1), (piece2, 2)]
    mock_game_state = GameState(players=[])

    chosen_move = bot.choose_move(legal_moves, mock_game_state)

    assert chosen_move == legal_moves[0]


@patch("builtins.input", side_effect=["2"])
def test_human_bot_chooses_second_move(mock_input):
    """
    Tests that the human bot correctly chooses the second move.
    """
    bot = HumanBot()
    piece1 = Piece(id=0, color=PlayerColor.RED)
    piece2 = Piece(id=1, color=PlayerColor.RED)
    legal_moves = [(piece1, 1), (piece2, 2)]
    mock_game_state = GameState(players=[])

    chosen_move = bot.choose_move(legal_moves, mock_game_state)

    assert chosen_move == legal_moves[1]


@patch("builtins.input", side_effect=["abc", "3", "1"])
def test_human_bot_handles_invalid_input(mock_input):
    """
    Tests that the human bot handles invalid input and re-prompts.
    """
    bot = HumanBot()
    piece1 = Piece(id=0, color=PlayerColor.RED)
    piece2 = Piece(id=1, color=PlayerColor.RED)
    legal_moves = [(piece1, 1), (piece2, 2)]
    mock_game_state = GameState(players=[])

    chosen_move = bot.choose_move(legal_moves, mock_game_state)

    assert chosen_move == legal_moves[0]
