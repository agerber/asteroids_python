from math import cos, sin, radians

from mvc.controller.SoundLoader import SoundLoader
from mvc.model.Falcon import Falcon
from mvc.model.Movable import Movable
from mvc.model.Sprite import Sprite
from mvc.model.prime.Point import Point
from mvc.model.prime.Color import Color


class Bullet(Sprite):
    def __init__(self, falcon: Falcon):
        super().__init__()
        self.team = Movable.Team.FRIEND
        self.color = Color.ORANGE  # orange

        # a bullet expires after 20 frames.
        self.expiry = 20
        self.radius = 11

        # everything is relative to the falcon ship that fired the bullet
        self.center = falcon.center.clone()

        # set the bullet orientation to the falcon (ship) orientation
        self.orientation = falcon.orientation

        FIRE_POWER = 35.0
        vectorX = cos(radians(self.orientation)) * FIRE_POWER
        vectorY = sin(radians(self.orientation)) * FIRE_POWER

        # fire force: falcon inertia + fire-vector
        self.deltaX = falcon.deltaX + vectorX
        self.deltaY = falcon.deltaY + vectorY

        # define the points on a cartesian grid
        self.cartesians = [
            Point(0, 3),  # top point
            Point(1, -1),  # right bottom
            Point(0, 0),
            Point(-1, -1),  # left bottom
        ]


    def draw(self, imgOff):
        self.renderVector(imgOff)

    def addToGame(self, list):
        super().addToGame(list)
        SoundLoader.playSound("thump.wav")
