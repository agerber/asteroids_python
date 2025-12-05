import random
import math

from mvc.controller.CommandCenter import CommandCenter
from mvc.controller.GameOp import GameOp
from mvc.controller.Sound import Sound
from mvc.model.Sprite import Sprite
from mvc.model.Movable import Movable
from mvc.model.WhiteCloudDebris import WhiteCloudDebris
from mvc.model.prime.Color import Color
from mvc.model.prime.Point import Point
from mvc.model.prime.PolarPoint import PolarPoint
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

    # returns the log-base-2 of the ratio (1,2,4) , which is (0,1,2).... the size
    def getSize(self) -> int:
        return int(math.log2(self.LARGE_RADIUS / self.radius))

    def draw(self, imgOff):
        self.renderVector(imgOff)

    def removeFromGame(self, list):
        super().removeFromGame(list)
        self.spawnSmallerAsteroidOrDebris(self)
        CommandCenter.getInstance().score += 10


    def spawnSmallerAsteroidOrDebris(self, originalAsteroid):
        size = originalAsteroid.getSize()
        if size > 1:
            CommandCenter.getInstance(). \
                opsQueue. \
                enqueue(WhiteCloudDebris(originalAsteroid), GameOp.Action.ADD)
            Sound.playSound("pillow.wav")
        else:
            size += 2
            while size > 0:
                CommandCenter.getInstance().opsQueue \
                    .enqueue(Asteroid(originalAsteroid), GameOp.Action.ADD)
                size -= 1
            Sound.playSound("kapow.wav")

    def __str__(self):
        return "Asteroid(" + str(self.value) + ")"

    def generateVertices(self):
        MAX_RADIANS_X1000 = 6283
        PRECISION = 1000.0

        polarPointSupplier = lambda: PolarPoint(
            (800 + random.randint(0, 199)) / PRECISION,
            random.randint(0, MAX_RADIANS_X1000 - 1) / PRECISION
        )

        sortByTheta = lambda pp: pp.theta

        polarToCartesian = lambda pp: Point(
            int(pp.r * PRECISION * math.sin(pp.theta)),
            int(pp.r * PRECISION * math.cos(pp.theta))
        )

        NUM_VERTICES = random.randint(25, 31)

        return (
            seq.range(NUM_VERTICES)
            .map(lambda _: polarPointSupplier())
            .sorted(key=sortByTheta)
            .map(polarToCartesian)
            .list()
        )



