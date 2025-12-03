from mvc.model.Movable import Movable
from mvc.model.Sprite import Sprite
from mvc.model.prime.Point import Point
from mvc.model.prime.Color import Color


class Floater(Sprite):
    def __init__(self):
        super().__init__()

        self.team = Movable.Team.FLOATER
        self.color = Color.WHITE
        self.expiry = 250
        self.spin = self.somePosNegValue(10)
        self.deltaX = self.somePosNegValue(10)
        self.deltaY = self.somePosNegValue(10)
        self.radius = 50

        # define the points on a cartesian grid
        points = [
            Point(5, 5),
            Point(4, 0),
            Point(5, -5),
            Point(0, -4),
            Point(-5, -5),
            Point(-4, 0),
            Point(-5, 5),
            Point(0, 4)
        ]

        self.cartesians = points

    def draw(self, imgOff):
        self.renderVector(imgOff)
