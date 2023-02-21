import random
from collections import deque
from typing import Any, List, Union


def shuffle(lst: Union[List[Any], deque[Any]]) -> None:
    # Move through the list of cards backwards: start at last card, stop at
    # first card, -1 step.
    for i in range((len(lst) - 1), 0, -1):
        # Pick a random number to the left of our index position.
        r = random.randint(0, i)
        # Swap the two cards.
        lst[i], lst[r] = lst[r], lst[i]
