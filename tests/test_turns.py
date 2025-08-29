import unittest
from unittest.mock import MagicMock, patch
from ludo.game import Game
from ludo.dice import Dice
from ludo.state import GameState
from ludo.player import Player
from ludo.utils.constants import PlayerColor

class TestTurnRules(unittest.TestCase):
    def setUp(self):
        """Set up a fresh game instance for each test."""
        self.dice = Dice(seed=1)
        self.players = [Player(PlayerColor.RED), Player(PlayerColor.GREEN)]
        self.game = Game(players=[p.color.value for p in self.players], dice=self.dice)
        self.game.state.players = self.players

    @patch('ludo.game.Game.next_player')
    @patch('ludo.rules.Rules.get_legal_moves', return_value=[])
    def test_extra_turn_on_six(self, mock_get_legal_moves, mock_next_player):
        """Test that a player gets an extra turn upon rolling a 6."""
        self.dice.roll = MagicMock(side_effect=[6, StopIteration])

        with patch('builtins.print'):
            try:
                self.game.loop_cli()
            except StopIteration:
                pass

        mock_next_player.assert_not_called()
        self.assertEqual(self.game.state.consecutive_sixes, 1)
        self.assertEqual(self.game.state.current_player_index, 0)

    @patch('ludo.game.Game.next_player')
    @patch('ludo.rules.Rules.get_legal_moves', return_value=[])
    def test_turn_advances_on_non_six(self, mock_get_legal_moves, mock_next_player):
        """Test that the turn advances to the next player on a non-6 roll."""
        self.dice.roll = MagicMock(side_effect=[5, StopIteration])

        with patch('builtins.print'):
            try:
                self.game.loop_cli()
            except StopIteration:
                pass

        mock_next_player.assert_called_once()

    @patch('ludo.game.Game.next_player')
    @patch('ludo.rules.Rules.get_legal_moves', return_value=[])
    def test_forfeit_on_three_consecutive_sixes(self, mock_get_legal_moves, mock_next_player):
        """Test that a player's turn is forfeited after three consecutive 6s."""
        self.dice.roll = MagicMock(side_effect=[6, StopIteration])
        self.game.state.consecutive_sixes = 2  # Set up the state before the third 6

        with patch('builtins.print'):
            try:
                self.game.loop_cli()
            except StopIteration:
                pass

        mock_next_player.assert_called_once()
        self.assertEqual(self.game.state.consecutive_sixes, 0)

    @patch('ludo.game.Game.next_player')
    @patch('ludo.rules.Rules.get_legal_moves', return_value=[])
    def test_two_sixes_then_non_six_advances_turn(self, mock_get_legal_moves, mock_next_player):
        """Test that two 6s give extra turns, and the third non-6 roll advances the player."""
        self.dice.roll = MagicMock(side_effect=[6, 6, 5, StopIteration])

        with patch('builtins.print'):
            try:
                self.game.loop_cli()
            except StopIteration:
                pass

        # next_player should only be called once, after the non-6 roll.
        mock_next_player.assert_called_once()
        self.assertEqual(self.game.state.consecutive_sixes, 0)

    @patch('ludo.game.Game.next_player')
    @patch('ludo.rules.Rules.get_legal_moves', return_value=[])
    def test_three_sixes_does_not_forfeit_if_disabled(self, mock_get_legal_moves, mock_next_player):
        """Test that three 6s do NOT forfeit the turn if the rule is disabled."""
        # Re-initialize game with the forfeit rule disabled
        self.game = Game(
            players=[p.color.value for p in self.players],
            dice=self.dice,
            three_six_forfeit=False
        )
        self.game.state.players = self.players
        self.dice.roll = MagicMock(side_effect=[6, StopIteration])
        self.game.state.consecutive_sixes = 2  # Set up the state before the third 6

        with patch('builtins.print'):
            try:
                self.game.loop_cli()
            except StopIteration:
                pass

        # The player should get an extra turn, so next_player is not called
        mock_next_player.assert_not_called()
        self.assertEqual(self.game.state.consecutive_sixes, 3)

if __name__ == '__main__':
    unittest.main()
