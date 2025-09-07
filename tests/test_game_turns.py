import unittest.mock

from ludo.bots.human_bot import HumanBot
from ludo.dice import Dice
from ludo.game import Game
from ludo.player import Player
from ludo.utils.constants import PieceState, PlayerColor


def test_play_turn_no_legal_moves_non_6_roll():
    """
    Tests that the turn advances if a non-6 is rolled and there are no legal moves.
    """
    players = [
        Player(color=PlayerColor.RED, role="human"),
        Player(color=PlayerColor.GREEN, role="human"),
    ]
    strategies = [HumanBot(), HumanBot()]
    game = Game(players=players, strategies=strategies, dice=Dice())

    # Mock Rules.get_legal_moves to return an empty list
    game.state.current_player_index = 0
    with unittest.mock.patch(
        "ludo.rules.Rules.get_legal_moves", return_value=[]
    ) as mock_get_legal_moves:
        game.play_turn(5)
        mock_get_legal_moves.assert_called_once()

    assert game.state.current_player_index == 1


def test_play_turn_no_legal_moves_real_scenario():
    """
    Tests that the turn advances if a non-6 is rolled and there are no legal moves
    in a realistic scenario.
    """
    players = [
        Player(color=PlayerColor.RED, role="human"),
        Player(color=PlayerColor.GREEN, role="human"),
    ]
    strategies = [HumanBot(), HumanBot()]
    game = Game(players=players, strategies=strategies, dice=Dice())

    # Set up a state where the current player has no legal moves
    current_player = game.state.players[0]
    for piece in current_player.pieces:
        piece.state = PieceState.HOME_COLUMN
        piece.position = 55  # Needs a 2 to win

    game.state.current_player_index = 0
    game.play_turn(5)  # Roll a 5, which is too high to move any piece

    assert game.state.current_player_index == 1
