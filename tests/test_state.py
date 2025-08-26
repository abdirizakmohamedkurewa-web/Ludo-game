"""
Tests for the state dataclasses.
"""
from ludo.state import PlayerState, PieceState


def test_can_instantiate_state_stubs():
    """
    Tests that the stub dataclasses can be instantiated.
    """
    player_state = PlayerState()
    piece_state = PieceState()

    assert player_state is not None
    assert piece_state is not None
