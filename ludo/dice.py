"""
Dice abstraction (seedable for tests).
"""

import random
from typing import Optional


class Dice:
    """A standard 6-sided die."""

    def __init__(self, seed: Optional[int] = None):
        self.seed = seed
        if self.seed is not None:
            random.seed(self.seed)

    def roll(self) -> int:
        """Rolls the die and returns a value between 1 and 6."""
        return random.randint(1, 6)
