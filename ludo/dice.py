"""
Dice abstraction (seedable for tests).
"""
import random


class Dice:
    """A standard 6-sided die."""
    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)

    def roll(self) -> int:
        """Rolls the die and returns a value between 1 and 6."""
        return random.randint(1, 6)
