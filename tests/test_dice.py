"""
Tests for the Dice class.
"""

from ludo.dice import Dice


def test_dice_roll_is_within_range():
    """Tests that a dice roll is always between 1 and 6."""
    dice = Dice()
    for _ in range(100):
        roll = dice.roll()
        assert 1 <= roll <= 6


def test_dice_seeding_is_reproducible():
    """Tests that a seeded die produces a predictable sequence of rolls."""
    # Re-seed to ensure this test is independent
    dice1 = Dice(seed=42)
    sequence1 = [dice1.roll() for _ in range(20)]

    # A second die with the same seed should produce the exact same sequence
    dice2 = Dice(seed=42)
    sequence2 = [dice2.roll() for _ in range(20)]

    assert sequence1 == sequence2

    # A third die with a different seed should produce a different sequence
    dice3 = Dice(seed=99)
    sequence3 = [dice3.roll() for _ in range(20)]

    assert sequence1 != sequence3
