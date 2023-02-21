from collections import deque
from typing import Dict, List, Optional, Union

from card import Card, PlayingCard
from suit import Suit
from utils import shuffle


class Deck:
    def __init__(self) -> None:
        # TODO: Is a deque really the best data structure for this?
        # Concerns: shuffling involves a lot of look-ups by index, which
        # approximate O(n) toward the middle of the deque.
        self.cards = deque()

    def __len__(self) -> int:
        return len(self.cards)

    def show(self) -> None:
        print(" ".join({str(c) for c in self.cards}))

    def shuffle(self) -> None:
        shuffle(self.cards)

    def peek(self) -> None:
        self.cards[0].show()

    def peek_bottom(self) -> None:
        self.cards[-1].show()

    def deal(self, n: int = 1) -> list:
        cards = []
        while n > 0:
            cards.append(self.cards.popleft())
            n -= 1
        return cards

    def take(self, card: Card) -> Union[Card, None]:
        try:
            i = self.cards.index(card)
        except ValueError:
            return None
        found_card = self.cards[i]
        self.remove(card)
        return found_card

    def remove(self, card: Card) -> None:
        self.cards.remove(card)


class PlayingCardDeck(Deck):
    def __init__(
        self,
        suits: Optional[List[Suit]] = None,
        court_mapping: Optional[Dict[int, str]] = None,
        aces_high: bool = True,
        include_jokers: bool = False,
    ):
        if not suits:
            self.suits = [
                Suit[name.upper()] for name in ["Clubs", "Diamonds", "Hearts", "Spades"]
            ]
        else:
            self.suits = suits
        if not court_mapping:
            self.court_mapping = PlayingCard.default_court_mapping(aces_high)
        else:
            self.court_mapping = court_mapping
        self.aces_high = aces_high
        self.include_jokers = include_jokers
        super().__init__()
        self._build()

    def __repr__(self):
        return (
            f"Deck of {len(self.cards)} cards. "
            f"Suits: {self.suits} - "
            f"Court mapping: {self.court_mapping} - "
            f"Aces high? {self.aces_high} - "
            f"Include jokers? {self.include_jokers}"
        )

    def _build(self):
        min_range = 2 if self.aces_high else 1
        max_range = min_range + 13
        for suit in self.suits:
            for value in range(min_range, max_range):
                self.cards.append(PlayingCard(suit, value, self.court_mapping))
        if self.include_jokers:
            self.cards.extend(
                [PlayingCard(Suit.JOKERS, 100), PlayingCard(Suit.JOKERS, 100)]
            )
