from functools import total_ordering
from typing import Dict, Optional, Union

from suit import Suit


class Card:
    def __init__(self) -> None:
        self.is_face_up = False

    def flip(self) -> None:
        self.is_face_up = not self.is_face_up

    def show(self) -> None:
        print(self)


@total_ordering
class PlayingCard(Card):
    def __init__(
        self,
        suit: Suit,
        value: int,
        court_mapping: Optional[Dict[int, str]] = None,
        aces_high: bool = True,
    ) -> None:
        self.suit = suit
        self.value = int(value)
        self.character_value = self._value_to_char(court_mapping, aces_high)
        super().__init__()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(suit=Suit.{self.suit.name.upper()}, value={self.value})>"

    def __str__(self) -> str:
        value = self.character_value if self.character_value else str(self.value)
        if self.suit.symbol:
            suit = self.suit.symbol
        elif self.suit.name == Suit.JOKERS.name:
            return "Jkr"
        else:
            suit = f" {self.suit.name.capitalize()}"
        return f"{value}{suit}"

    def _value_to_char(
        self, court_mapping: Optional[Dict[int, str]], aces_high: bool = True,
    ) -> Union[str, None]:
        if not court_mapping:
            court_mapping = self.default_court_mapping(aces_high)
        return court_mapping.get(self.value)

    def _is_valid_operand(self, other) -> bool:
        return hasattr(other, "suit") and hasattr(other, "value")

    def __eq__(self, other) -> bool:
        if not self._is_valid_operand(other):
            return NotImplemented
        return (self.value, self.suit.value) == (other.value, other.suit.value)

    def __lt__(self, other) -> bool:
        if not self._is_valid_operand(other):
            return NotImplemented
        return (self.value, self.suit.value) < (other.value, other.suit.value)

    @staticmethod
    def default_court_mapping(aces_high: bool = True) -> Dict[int, str]:
        court_mapping = {11: "J", 12: "Q", 13: "K"}
        if aces_high:
            court_mapping[14] = "A"
        else:
            court_mapping[1] = "A"
        return court_mapping
