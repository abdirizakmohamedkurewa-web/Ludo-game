"""
Dataclasses for GameState, TurnState, etc.
"""
from dataclasses import dataclass
from typing import List, Optional
from ludo.player import Player


@dataclass
class GameState:
    """Represents the complete state of the game at a point in time."""
    players: List[Player]
    current_player_index: int = 0
    dice_roll: Optional[int] = None
    is_game_over: bool = False
