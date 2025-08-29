"""
Bot that chooses moves based on a simple greedy scoring function.
"""
from typing import List

import copy
from typing import List

from ludo.bots.base import Strategy
from ludo.move import move_piece
from ludo.piece import Piece, PieceState
from ludo.state import GameState


class GreedyBot(Strategy):
    """A bot that uses a greedy algorithm to choose the best move."""

    def _get_move_score(self, move: Piece, game_state: GameState) -> tuple[int, int]:
        """Assigns a score to a move based on a set of greedy priorities."""
        original_piece = [p for p in game_state.players[game_state.current_player_index].pieces if p.id == move.id][0]

        # Create a deep copy of the game state to simulate the move
        sim_state = copy.deepcopy(game_state)
        piece_in_sim = [p for p in sim_state.players[sim_state.current_player_index].pieces if p.id == move.id][0]

        # Simulate the move
        move_piece(sim_state, piece_in_sim, sim_state.dice_roll)

        # 1. Prioritize moving a piece into the HOME position
        if piece_in_sim.state == PieceState.HOME:
            return 4, 0

        # 2. Prioritize capturing an opponent's piece
        # A capture happens if an opponent piece that was on the track is now in the yard
        for i, player in enumerate(game_state.players):
            if i == game_state.current_player_index:
                continue
            for j, original_opponent_piece in enumerate(player.pieces):
                sim_opponent_piece = sim_state.players[i].pieces[j]
                if original_opponent_piece.state == PieceState.TRACK and sim_opponent_piece.state == PieceState.YARD:
                    return 3, piece_in_sim.position

        # 3. Prioritize moving a piece out of the YARD
        if original_piece.state == PieceState.YARD and piece_in_sim.state == PieceState.TRACK:
            return 2, piece_in_sim.position

        # 4. Prioritize moving the piece that is furthest along the track
        if original_piece.state == PieceState.TRACK:
            # The "further" the piece is, the higher its position value
            # (considering wrap around for home entry)
            return 1, piece_in_sim.position

        # Default score
        return 0, 0

    def choose_move(self, legal_moves: List[Piece], game_state: GameState) -> Piece:
        """
        Selects a piece to move based on a greedy evaluation.

        Args:
            legal_moves: A list of `Piece` objects that can be legally moved.
            game_state: The current `GameState` of the game.

        Returns:
            The `Piece` object representing the chosen move.
        """
        if not legal_moves:
            raise ValueError("No legal moves available to choose from.")

        # Score each legal move
        scored_moves = [
            (move, self._get_move_score(move, game_state)) for move in legal_moves
        ]

        # Sort moves: higher score is better. For ties, higher position is better.
        scored_moves.sort(key=lambda item: (item[1][0], item[1][1]), reverse=True)

        # Return the best move
        return scored_moves[0][0]
