from enum import Enum, auto
from functools import total_ordering
from typing import Union

from color import Color


@total_ordering
class Suit(Enum):
    CLUBS = auto()
    DIAMONDS = auto()
    HEARTS = auto()
    SPADES = auto()
    WANDS = auto()
    COINS = auto()
    CUPS = auto()
    SWORDS = auto()

    def __str__(self):
        return self.name.capitalize()

    @property
    def color(self) -> Union[Enum, None]:
        conversion = {
            "Clubs": Color.BLACK,
            "Diamonds": Color.RED,
            "Hearts": Color.RED,
            "Spades": Color.BLACK,
        }
        return conversion.get(self.name.capitalize())

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
