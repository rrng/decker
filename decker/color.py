from enum import Enum, auto
from typing import Tuple


class Color(Enum):
    RED = (auto(), (255, 0, 0), "#FF0000")
    BLACK = (auto(), (0, 0, 0), "#000000")

    def __str__(self):
        return self.name.capitalize()

    @property
    def rgb(self) -> Tuple:
        return self.value[1]

    @property
    def hex(self) -> str:
        return self.value[2]
