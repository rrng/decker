from enum import Enum
from typing import Tuple

class Color(Enum):
    RED = (1, (255,0,0), "#FF0000")
    BLACK = (2, (0,0,0), "#000000")

    def __str__(self):
        return self.name.capitalize()

    @property
    def rgb(self) -> Tuple:
        return self.value[1]

    @property
    def hex(self) -> str:
        return self.value[2]
