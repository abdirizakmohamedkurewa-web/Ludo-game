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


@pytest.fixture
def game_two_players():
    """Returns a game instance with two players for turn-based tests."""
    return Game(players=["red", "green"], dice=Dice(seed=1))


def test_extra_turn_on_roll_6(game_two_players):
    """
    Tests that a player's turn is not advanced if they roll a 6.
    """
    game = game_two_players
    assert game.state.current_player_index == 0

    # Player 1 rolls a 6
    game.play_turn(6)

    # It should still be player 1's turn
    assert game.state.current_player_index == 0
    assert game.state.consecutive_sixes == 1


def test_turn_advances_on_non_6(game_two_players):
    """
    Tests that a player's turn advances if they roll a non-6.
    """
    game = game_two_players
    assert game.state.current_player_index == 0

    # Player 1 rolls a 5
    game.play_turn(5)

    # It should now be player 2's turn
    assert game.state.current_player_index == 1


def test_forfeit_on_three_consecutive_sixes(game_two_players):
    """
    Tests that a turn is forfeited and advanced after three consecutive 6s.
    """
    game = game_two_players
    game.state.consecutive_sixes = 2  # Simulate two previous 6s
    assert game.state.current_player_index == 0

    # Player 1 rolls a third 6
    game.play_turn(6)

    # The turn should be forfeited and passed to player 2
    assert game.state.current_player_index == 1
    # The consecutive sixes count should be reset for the new player
    assert game.state.consecutive_sixes == 0


def test_three_sixes_no_forfeit_if_disabled(game_two_players):
    """
    Tests that three 6s do not cause a forfeit if the rule is disabled.
    """
    game = game_two_players
    game.three_six_forfeit = False  # Disable the rule
    game.state.consecutive_sixes = 2
    assert game.state.current_player_index == 0

    # Player 1 rolls a third 6
    game.play_turn(6)

    # The player should get an extra turn, not forfeit
    assert game.state.current_player_index == 0
    assert game.state.consecutive_sixes == 3
