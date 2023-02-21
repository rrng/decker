from enum import Enum, auto
from functools import total_ordering
from typing import Union

from color import Color


@total_ordering
class Suit(Enum):
    CLUBS = (auto(), Color.BLACK)
    DIAMONDS = (auto(), Color.RED)
    HEARTS = (auto(), Color.RED)
    SPADES = (auto(), Color.BLACK)
    WANDS = (auto(), Color.BLACK)  # Clubs
    COINS = (auto(), Color.RED)  # Diamonds
    CUPS = (auto(), Color.RED)  # Hearts
    SWORDS = (auto(), Color.BLACK)  # Spades

    def __str__(self):
        return self.name.capitalize()

    @property
    def color(self) -> Enum:
        return self.value[1]

    @property
    def symbol(self) -> Union[str, None]:
        conversion = {
            "Clubs": "\u2663",
            "Diamonds": "\u2666",
            "Hearts": "\u2665",
            "Spades": "\u2660",
            "Wands": "\u269A",
            "Coins": "\u235F",  # Alternative: '\u272A'
            "Cups": "\u222A",
            "Swords": "\u2694",
        }
        return conversion.get(self.name.capitalize())

    def _is_valid_operand(self, other) -> bool:
        return hasattr(other, "value")

    def __eq__(self, other) -> bool:
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.value == other.value

    def __lt__(self, other) -> bool:
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.value < other.value
