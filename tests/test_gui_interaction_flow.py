import pytest
from ludo.game import Game
from ludo.dice import Dice
from ludo.utils.constants import PlayerColor, PieceState
from ludo.player import Player
from ludo.bots.human_bot import HumanBot
from ludo.rules import Rules
from ludo.move import move_piece


def test_gui_manual_move_flow():
    """
    Tests the sequence of operations that the GUI performs for a manual move,
    verifying the complete flow from roll to next turn.
    """
    # 1. Setup: Create a game with two players
    players = [
        Player(color=PlayerColor.RED, role="human"),
        Player(color=PlayerColor.GREEN, role="human")
    ]
    strategies = [HumanBot(), HumanBot()]
    # Use a fixed seed for a predictable dice roll if needed, though we'll hardcode it.
    game = Game(players=players, strategies=strategies, dice=Dice())

    # Manually place a RED piece on the board to ensure a move is possible.
    # This avoids depending on rolling a 6 to get out of the yard.
    game.state.players[0].pieces[0].state = PieceState.TRACK
    game.state.players[0].pieces[0].position = 10

    assert game.state.current_player_index == 0

    # 2. Simulate Dice Roll (as if the user clicked "Roll Dice")
    roll = 3
    game.state.dice_roll = roll # The GUI would store the roll in the state

    # 3. Get Legal Moves (as the GUI does after a roll)
    legal_moves = Rules.get_legal_moves(game.state, roll)

    # We expect one legal move: piece 0 moves from position 10 to 13.
    assert len(legal_moves) == 1
    piece_to_move, destination = legal_moves[0]
    assert piece_to_move.id == 0
    assert destination == 13

    # 4. Simulate User Clicking a Piece and a Destination
    # The GUI would identify the selected piece and destination from mouse coords.
    # Here, we use the legal move we just found.
    move_piece(game.state, piece_to_move, roll)

    # 5. Assert the piece's state has been updated correctly
    assert game.state.players[0].pieces[0].state == PieceState.TRACK
    assert game.state.players[0].pieces[0].position == 13

    # 6. Advance Turn (as the GUI does since the roll was not 6)
    game.next_player()

    # 7. Assert the turn has advanced to the next player
    assert game.state.current_player_index == 1

    # 8. Verify that the consecutive sixes count was reset for the new player
    assert game.state.consecutive_sixes == 0
