import os
import random
import math

from pythonic.mvc.controller.CommandCenter import CommandCenter
from pythonic.mvc.controller.GameOp import GameOp
from pythonic.mvc.controller.Sound import Sound
from pythonic.mvc.model.Sprite import Sprite
from pythonic.mvc.model.Movable import Movable
from pythonic.mvc.model.WhiteCloudDebris import WhiteCloudDebris
from pythonic.mvc.model.prime.Color import Color
from pythonic.mvc.model.prime.Point import Point
from pythonic.mvc.model.prime.PolarPoint import PolarPoint
from functional import seq


class Asteroid(Sprite):

    def __init__(self, value):
        super().__init__()
        self.value = value
        self.LARGE_RADIUS = 110
        # There is no method overloading in python. We must check the parameter type to differentiate the calls
        # and then use conditional logic to call the appropriate logic within the constructor
        if isinstance(value, int):
            if value == 0:
                self.radius = self.LARGE_RADIUS
            else:
                self.radius = self.LARGE_RADIUS / (value * 2)

            self.team = Movable.Team.FOE
            self.color = Color.WHITE

            self.spin = self.somePosNegValue(10)
            self.deltaX = self.somePosNegValue(10)
            self.deltaY = self.somePosNegValue(10)

            self.cartesians = self.generateVertices()
        else:
            ast_exploded = value
            self.__init__(ast_exploded.getSize() + 1)
            self.center = ast_exploded.getCenter().clone()
            new_smaller_size = ast_exploded.getSize() + 1
            self.deltaX = ast_exploded.deltaX / 1.5 + self.somePosNegValue(5 + new_smaller_size * 2)
            self.deltaY = ast_exploded.deltaY / 1.5 + self.somePosNegValue(5 + new_smaller_size * 2)

    def getSize(self) -> int:
        value = 0
        if self.radius == self.LARGE_RADIUS:
            value = 0
        elif self.radius == self.LARGE_RADIUS / 2:
            value = 1
        elif self.radius == self.LARGE_RADIUS / 4:
            value = 2
        return value

    def draw(self, imgOff):
        self.renderVector(imgOff)

    def removeFromGame(self, list):
        super().removeFromGame(list)
        self.spawnSmallerAsteroidOrDebris(self)
        CommandCenter.getInstance().score += 10

        if self.getSize() > 1:
            Sound.playSound("pillow.wav")
        else:
            Sound.playSound("kapow.wav")

    def spawnSmallerAsteroidOrDebris(self, originalAsteroid):
        size = originalAsteroid.getSize()
        if size > 1:
            CommandCenter.getInstance(). \
                opsQueue. \
                enqueue(WhiteCloudDebris(originalAsteroid), GameOp.Action.ADD)
        else:
            size += 2
            while size > 0:
                CommandCenter.getInstance().opsQueue \
                    .enqueue(Asteroid(originalAsteroid), GameOp.Action.ADD)
                size -= 1

    def __str__(self):
        return "Asteroid(" + str(self.value) + ")"

    def generateVertices(self):
        # 6.283 is the max radians
        MAX_RADIANS_X1000 = 6283
        # When casting from double to int, we truncate and lose precision, so best to be generous with the
        # precision factor as this will create a more normal distribution of vertices. Precision is a proxy for
        # radius in the absence of a predefined radius.
        PRECISION = 1000.0


        # this is the lambda version of below
        # polarPointSupplier = lambda : PolarPoint(
        #     (800 + random.randint(0, 199)) / 1000.0,
        #     random.randint(0, MAX_RADIANS_X1000 - 1) / 1000.0
        # )

        def polarPointSupplier():
            r = (800 + random.randint(0, 199)) / PRECISION  # number between 0.8 and 0.999
            theta = random.randint(0, MAX_RADIANS_X1000 - 1) / PRECISION  # number between 0 and 6.282
            return PolarPoint(r, theta)



        # this is the lambda version of below
        #sortByTheta = lambda pp: pp.theta

        # given PolarPoint pp, return theta
        def sortByTheta(pp: PolarPoint):
            return pp.theta

        # this is the lambda version of below
        # polarToCartesian = lambda pp: Point(
        #     int(pp.r * PRECISION * math.sin(pp.theta)),
        #     int(pp.r * PRECISION * math.cos(pp.theta))
        # )
        def polarToCartesian(pp: PolarPoint):
            return Point(
                int(pp.r * PRECISION * math.sin(pp.theta)),
                int(pp.r * PRECISION * math.cos(pp.theta))
            )

        # random number of vertices
        VERTICES = random.randint(25, 31)

        return seq(polarPointSupplier() for _ in range(VERTICES)) \
            .sorted(key=sortByTheta) \
            .map(polarToCartesian) \
            .list()
