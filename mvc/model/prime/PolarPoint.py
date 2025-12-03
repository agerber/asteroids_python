from dataclasses import dataclass


@dataclass
class PolarPoint:
    """This class is used in conjunction with Point to render Sprites"""

    r: float
    theta: float
