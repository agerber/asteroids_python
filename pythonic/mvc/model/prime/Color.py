from dataclasses import dataclass
from typing import Tuple


class Color:
    ## static colors
    RED: Tuple[int, int, int] = (255, 0, 0)
    GREEN: Tuple[int, int, int] = (0, 255, 0)
    BLUE: Tuple[int, int, int] = (0, 0, 255)
    CYAN: Tuple[int, int, int] = (0, 200, 200)
    ORANGE: Tuple[int, int, int] = (255, 165, 0)
    WHITE: Tuple[int, int, int] = (255, 255, 255)
    BLACK: Tuple[int, int, int] = (0, 0, 0)
    GREY: Tuple[int, int, int] = (128, 128, 128)
    YELLOW: Tuple[int, int, int] = (255, 255, 0)

    @staticmethod
    def from_RGB(r, g, b):
        return (r, g, b)
