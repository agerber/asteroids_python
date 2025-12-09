from math import cos, sin, radians
from PIL import ImageDraw
from mvc.controller.CommandCenter import CommandCenter
from mvc.controller.SoundLoader import SoundLoader
from mvc.model.Falcon import Falcon
from mvc.model.Movable import Movable
from mvc.model.Sprite import Sprite
from mvc.model.prime.Color import Color


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
        self.center = falcon.center.clone()

        self.orientation = falcon.orientation

        FIRE_POWER = 11.0
        vectorX = cos(radians(self.orientation)) * FIRE_POWER
        vectorY = sin(radians(self.orientation)) * FIRE_POWER

        # fire force: falcon inertia + fire-vector
        self.deltaX = falcon.deltaX + vectorX
        self.deltaY = falcon.deltaY + vectorY

    def draw(self, imgOff):
        # get the graphics context of the imgOff
        g = ImageDraw.Draw(imgOff)
        g.ellipse((self.getCenter().x - self.getRadius(), self.getCenter().y - self.getRadius(),
                   self.getCenter().x + self.getRadius(), self.getCenter().y + self.getRadius())
                  , outline=Color.YELLOW)

    def move(self) -> None:
        super().move()
        if self.expiry % (Nuke.EXPIRE / 6) == 0:
            self.nukeState = self.nukeState + 1

        if self.nukeState == 0:
            self.radius = 17
        elif self.nukeState < 4:
            self.radius = self.radius + 8
        else:
            self.radius = self.radius - 11


    def addToGame(self, list):
        if (CommandCenter.getInstance().falcon.nukeMeter > 0):
            list.add(self)
            CommandCenter.getInstance().falcon.nukeMeter = 0
            SoundLoader.playSound("nuke.wav")

    def removeFromGame(self, list):
        if (self.expiry == 0):
            list.remove(self)
