import pytest
from ludo.game import Game
from ludo.dice import Dice
from ludo.utils.constants import PlayerColor, PieceState


def test_game_initialization():
    """
    Tests that the game is initialized with the correct
    number of players and pieces in the correct initial state.
    """
    game = Game(players=["red", "green", "yellow", "blue"], dice=Dice())
    state = game.state

    # Check for 4 players
    assert len(state.players) == 4
    assert state.players[0].color == PlayerColor.RED
    assert state.players[1].color == PlayerColor.GREEN
    assert state.players[2].color == PlayerColor.YELLOW
    assert state.players[3].color == PlayerColor.BLUE

    # Check that each player has 4 pieces
    for player in state.players:
        assert len(player.pieces) == 4
        # Check that all pieces are in the YARD
        for piece in player.pieces:
            assert piece.state == PieceState.YARD
            assert piece.position == -1
