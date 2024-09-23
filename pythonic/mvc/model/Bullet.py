import os
from math import cos, sin, radians

from pythonic.mvc.controller.CommandCenter import CommandCenter
from pythonic.mvc.controller.Sound import Sound
from pythonic.mvc.model.Falcon import Falcon
from pythonic.mvc.model.Movable import Movable
from pythonic.mvc.model.Sprite import Sprite
from pythonic.mvc.model.prime.Point import Point
from pythonic.mvc.model.prime.Color import Color


class Bullet(Sprite):
    def __init__(self, falcon: Falcon):
        super().__init__()
        self.team = Movable.Team.FRIEND
        self.color = Color.ORANGE  # orange

        # a bullet expires after 20 frames.
        self.expiry = 20
        self.radius = 6

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

        # we have a reference to the falcon passed into the constructor. Let's create some kick-back.
        # fire kick-back on the falcon: inertia - fire-vector / some arbitrary divisor
        KICK_BACK_DIVISOR = 36.0
        falcon.deltaX = falcon.deltaX - vectorX / KICK_BACK_DIVISOR
        falcon.deltaY = falcon.deltaY - vectorY / KICK_BACK_DIVISOR

        # define the points on a cartesian grid
        points = [
            Point(0, 3),  # top point
            Point(1, -1),  # right bottom
            Point(0, 0),
            Point(-1, -1),  # left bottom
        ]

        self.cartesians = points

    def draw(self, imgOff):
        self.renderVector(imgOff)

    def addToGame(self, list):
        super().addToGame(list)
        Sound.playSound("thump.wav")
