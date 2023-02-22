import sys
from enum import Enum, auto
from typing import Any, List, Optional, Tuple

from card import Card, PlayingCard
from deck import Deck, PlayingCardDeck
from suit import Suit
from utils import shuffle


class Direction(Enum):
    N = auto()
    NW = auto()
    NE = auto()
    S = auto()
    SW = auto()
    SE = auto()
    W = auto()
    E = auto()
    Q = 100
    QUIT = 100
    EXIT = 100

    def __str__(self):
        return self.name


class CartaBoard:
    CartaGrid = List[List[Card]]

    @staticmethod
    def create_empty_grid(rows: int, columns: int) -> List[List[Any]]:
        grid: List[List[Any]] = []
        for _i in range(rows):
            row = []
            for _j in range(columns):
                row.append(True)
            grid.append(row)
        return grid

    @staticmethod
    def is_valid_empty_grid(grid: List[List[Any]]) -> bool:
        # TODO: Fully validate grid with holes (Nones) -- make sure that player
        # can move from card to card (need to know allowed directions).
        first_row_len = len(grid[0])
        for row in grid:
            if len(row) != first_row_len:
                return False
            for elm in row:
                if not isinstance(elm, (bool, type(None))):
                    return False
        return True

    def __init__(
        self,
        deck: Deck,
        grid: CartaGrid,
        goal_card: Card,
        starting_card: Card,
        allowed_directions: Optional[List[Direction]] = None,
    ) -> None:
        if not self.is_valid_empty_grid(grid):
            raise ValueError(f"Invalid empty grid: {grid}")
        self.grid = grid
        self.goal_card = goal_card
        self.starting_card = starting_card
        self.starting_card.is_face_up = True
        if not allowed_directions:
            self.allowed_diections = [
                Direction.N,
                Direction.S,
                Direction.W,
                Direction.E,
                Direction.NW,
                Direction.NE,
                Direction.SW,
                Direction.SE,
            ]
        else:
            self.allowed_diections = allowed_directions
        self._build(deck)

    def _available_slots_in_grid(self) -> int:
        return sum(sum(bool(elm) for elm in row) for row in self.grid)

    def _build(self, deck: Deck):
        deck.remove(self.starting_card)
        deck.remove(self.goal_card)
        deck.shuffle()
        grid_cards: List[Card] = deck.deal((self._available_slots_in_grid() - 2))
        grid_cards.append(self.goal_card)
        shuffle(grid_cards)
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] is True:
                    if grid_cards:
                        self.grid[i][j] = grid_cards.pop()
                    else:
                        self.grid[i][j] = self.starting_card
                        self.player_location = (i, j)

    @property
    def player_card(self) -> Card:
        i, j = self.player_location
        return self.grid[i][j]

    def _show_in_grid(self, card: Optional[Card]) -> str:
        if not isinstance(card, Card):
            return "  "
        if card.is_face_up:
            return str(card)
        else:
            return "XX"

    def show(self) -> None:
        print(
            "\n".join(
                "".join(self._show_in_grid(i).center(4) for i in row)
                for row in self.grid
            )
        )

    def show_player_location(self) -> None:
        print(f"You are at: {self.player_card}")
        if self.player_card.description:
            print(self.player_card.description)

    def start(self) -> None:
        self.show()
        self.show_player_location()
        while self.player_card != self.goal_card:
            self._move()
        print("You have reached your goal!")

    def _move(self) -> None:
        while True:
            try:
                direction = self._parse_input_direction(
                    input("Which direction do you want to move in? ")
                )
                if self._is_valid_move(direction):
                    self.player_location = self._new_location(direction)
                    i, j = self.player_location
                    self.grid[i][j].is_face_up = True
            except ValueError as e:
                # _parse_input_direction() or _is_valid_move() may raise a
                # ValueError; print it and re-prompt player to enter direction.
                print(e)
                continue
            break
        self.show()
        self.show_player_location()

    def _parse_input_direction(self, input: str) -> Direction:
        try:
            direction = Direction[input.upper()]
            if direction == Direction.Q:
                print("Goodbye!")
                sys.exit()
            assert direction in self.allowed_diections
            return direction
        except (KeyError, AssertionError) as e:
            raise ValueError(
                f"Direction must be one of: {[d.name for d in self.allowed_diections]}"
            ) from e

    def _new_location(self, direction: Direction) -> Tuple[int, int]:
        ns, we = self.player_location
        if direction == Direction.N:
            ns -= 1
        elif direction == Direction.S:
            ns += 1
        elif direction == Direction.W:
            we -= 1
        elif direction == Direction.E:
            we += 1
        elif direction == Direction.NW:
            ns -= 1
            we -= 1
        elif direction == Direction.NE:
            ns -= 1
            we += 1
        elif direction == Direction.SW:
            ns += 1
            we -= 1
        elif direction == Direction.SE:
            ns += 1
            we += 1
        else:
            raise NotImplementedError
        return (ns, we)

    def _is_valid_move(self, direction: Direction) -> bool:
        ns, we = self._new_location(direction)
        try:
            self.grid[ns][we]
            assert (ns >= 0) and (we >= 0)
            assert isinstance(self.grid[ns][we], Card)
        except (IndexError, AssertionError) as e:
            raise ValueError("You can't go off the map.") from e
        return True


if __name__ == "__main__":
    deck = PlayingCardDeck()
    # Grid with holes.
    # grid = [[None, True, None], [True, None, True], [None, True, None]]
    grid = CartaBoard.create_empty_grid(4, 3)
    goal_card = PlayingCard(Suit.HEARTS, 2)
    starting_card = PlayingCard(Suit.CLUBS, 2)
    board = CartaBoard(deck, grid, goal_card, starting_card)
    board.start()
