import dataclasses
from typing import List, Dict, Any
from PIL import Image, ImageOps,ImageDraw
import math
from scipy import ndimage as ndi

from mvc.controller.Utils import Utils
from mvc.model.Movable import Movable
from mvc.model.prime.Point import Point
from mvc.model.prime.PolarPoint import PolarPoint
from functional import seq
from abc import abstractmethod
from mvc.model.prime.Color import Color
from mvc.model.prime.Constants import DIM
from mvc.controller.GameOp import GameOp

import random

@dataclasses.dataclass
class Sprite(Movable):

    def __init__(self):


        self.center: Point = Point(random.randint(0, DIM.width), random.randint(0, DIM.height))
        self.deltaX: float = 0
        self.deltaY: float = 0
        self.team: Movable.Team = Movable.Team.DEBRIS
        self.radius: int = 0
        self.orientation: int = 0
        self.expiry: int = 0
        self.spin: int = 0

        # members used for vector sprites
        self.cartesians: List[Point] = []
        self.color: Color.WHITE

        # raster map for raster sprites
        self.rasterMap: Dict[Any, Image.Image] = {}



    # contract methods - required overriding in extending classes
    def getRadius(self) -> int:
        return self.radius

    def getTeam(self) -> Movable.Team:
        return self.team

    def getCenter(self):
        return self.center


    def addToGame(self, list):
        list.add(self)

    def removeFromGame(self, list):
        list.remove(self)



    @abstractmethod
    def draw(self, g):
        pass

    # TODO The following methods are an example of the Template_Method design pattern. The Sprite class provides
    # the common framework for Movable, such as move(), expire(), somePosNegValue(), renderRaster(), renderVector(), etc.
    # while delegating certain details to its subclasses. Also note that Sprite passes draw() and this contract debt
    # (inherited from Movable) is passed to Sprite's subclasses,
    # which must satisfy the contract by providing implementations for draw(), and this will depend on whether the
    # subclass renders as raster or vector.

    def move(self) -> None:
        from mvc.controller.CommandCenter import CommandCenter

        scalerX = CommandCenter.getInstance().getUniDim().width
        scalerY = CommandCenter.getInstance().getUniDim().height

        # right - bounds reached
        if self.center.x > scalerX * DIM.width:
            self.center.x = 1
        # left - bounds reached
        elif self.center.x < 0:
            self.center.x = scalerX * DIM.width - 1
        # bottom - bounds reached
        elif self.center.y > scalerY * DIM.height:
            self.center.y = 1
        # top - bounds reached
        elif self.center.y < 0:
            self.center.y = scalerY * DIM.height - 1
        else:
            new_x_pos = self.center.x + self.deltaX
            new_y_pos = self.center.y + self.deltaY

            if CommandCenter.getInstance().isFalconPositionFixed():
                new_x_pos -= CommandCenter.getInstance().falcon.deltaX
                new_y_pos -= CommandCenter.getInstance().falcon.deltaY

            self.center.x = new_x_pos
            self.center.y = new_y_pos


        if self.expiry > 0: self.expire()
        if self.spin != 0: self.orientation += self.spin

    def somePosNegValue(self, seed: int) -> int:
        random_number = random.randint(0, seed - 1)
        return random_number if random_number % 2 == 0 else -random_number

    def expire(self):
        # imported in function to avoid circular import
        from mvc.controller.CommandCenter import CommandCenter
        if self.expiry == 1:
            CommandCenter.getInstance().opsQueue.enqueue(self, GameOp.Action.REMOVE)

        self.expiry -= 1

    def renderRaster(self, imgOff, bufferedImage):

        if bufferedImage is None:
            return

        width = self.radius * 2
        height = self.radius * 2

        try:
            scaleX = width * 1.0 / bufferedImage.size[0]
            scaleY = height * 1.0 / bufferedImage.size[1]
            transformed = bufferedImage
            transformed = transformed.resize((int(bufferedImage.size[0] * scaleX),
                                              int(bufferedImage.size[1] * scaleY)))

            if self.orientation != 0:
                transformed = ndi.rotate(transformed, self.orientation, reshape=False)

            if not isinstance(transformed, Image.Image):
                transformed = Image.fromarray(transformed.astype("uint8"), "RGBA")

            transformed = ImageOps.flip(transformed)
            transformed = Utils.transparent(transformed)
            imgOff.paste(transformed, (round(self.center.x - width / 2.0), round(self.center.y - height / 2.0)))
        except Exception as e:
            print(e.args)

    def renderVector(self, imgOff):

        g = ImageDraw.Draw(imgOff) # get graphics context from the off-screen-image

        # To render this Sprite in vector mode, we need to, 1: convert raw cartesians to raw polars, 2: rotate polars
        # for orientation of sprite. 3: Convert back to cartesians 4: adjust for center-point (location).
        # and 5: pass the points, along with color, to g.polygon().

        # 1: convert raw cartesians to raw polars (used later in seq below).
        # The reason we convert cartesian-points to polar-points is that it's much easier to rotate polar-points
        polars = Utils.cartesiansToPolar(self.cartesians)

        # 2: rotate raw polars given the orientation of the sprite.

        rotatePolarByOrientation = lambda pp: PolarPoint(
            pp.r,
            pp.theta + math.radians(self.orientation)  # rotated Theta
        )

        # 3: convert the rotated polars back to cartesians
        polarToCartesian = lambda pp: Point(
            int(pp.r * self.radius * math.sin(pp.theta)),
            int(pp.r * self.radius * math.cos(pp.theta))
        )

        # 4: adjust the cartesians for the location (center-point) of the sprite.
        # the reason we subtract the y-value has to do with how Python plots the vertical axis for
        # graphics (from top to bottom)
        adjustForLocation = lambda pnt: Point(
            self.center.x + pnt.x,
            self.center.y - pnt.y
        )

        # 5: draw the polygon using the List of raw polars from above, applying mapping transforms as required

        # TODO The following is an example of the Pipeline design pattern, which is a way of chaining a series of operations
        # where the output of one operation becomes the input for the next, forming a "pipeline" of transformations and
        # processing steps. This is a key concept in functional programming.

        g.polygon(
            seq(polars)\
                .map(rotatePolarByOrientation)\
                .map(polarToCartesian)\
                .map(adjustForLocation)\
                .map(lambda point: (point.x, point.y))\
                .list(),
            outline=self.color)
