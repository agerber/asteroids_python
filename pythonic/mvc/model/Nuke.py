from math import cos, sin, radians

from PIL import Image, ImageOps,ImageDraw

from pythonic.mvc.model.Falcon import Falcon
from pythonic.mvc.model.Movable import Movable
from pythonic.mvc.model.Sprite import Sprite
from pythonic.mvc.model.prime.Point import Point
from pythonic.mvc.model.prime.Color import Color
class Nuke(Sprite):

    EXPIRE = 60
    def __init__(self, falcon: Falcon):
        super().__init__()

        self.nukeState = 0

        self.team = Movable.Team.FRIEND
        self.color = Color.YELLOW


        self.expiry = Nuke.EXPIRE
        self.radius = 0

        # everything is relative to the falcon ship that fired the bullet
        self.center = falcon.center

        self.orientation = falcon.orientation


        FIRE_POWER = 11.0
        vectorX = cos(radians(self.orientation)) * FIRE_POWER
        vectorY = sin(radians(self.orientation)) * FIRE_POWER

        # fire force: falcon inertia + fire-vector
        self.deltaX = falcon.deltaX + vectorX
        self.deltaY = falcon.deltaY + vectorY

    # a nuke is invincible while it is alive
    def isProtected(self) -> bool:
        return True

    def draw(self, imgOff):
        #get the graphics context of the imgOff
        g = ImageDraw.Draw(imgOff)
        g.ellipse((self.getCenter().x - self.getRadius(), self.getCenter().y - self.getRadius(),
                   self.getCenter().x + self.getRadius(), self.getCenter().y + self.getRadius())
                  , outline=Color.YELLOW)





    def move(self) -> None:
        super().move()
        if self.expiry % (Nuke.EXPIRE/6) == 0:
            self.nukeState = self.nukeState + 1

        if self.nukeState  == 0:
            self.radius = 2
        elif self.nukeState < 4:
            self.radius = self.radius + 16
        else:
            self.radius = self.radius -22