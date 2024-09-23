import os
from math import cos, sin, radians
from PIL import ImageDraw
from pythonic.mvc.controller.CommandCenter import CommandCenter
from pythonic.mvc.controller.Sound import Sound
from pythonic.mvc.model.Falcon import Falcon
from pythonic.mvc.model.Movable import Movable
from pythonic.mvc.model.Sprite import Sprite
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

    # TODO The following overrides are examples of the Observer design pattern (Lifecycle Callbacks). Lifecycle
    # Callbacks allow an object to perform specific actions at well-defined stages of its lifecycle. Lifecycle Callbacks encapsulate
    # logic that would otherwise be scattered throughout other classes, thereby making the code more organized and easier to manage.
    #
    # Subject (Game): The Game class acts as the subject that triggers changes in the state of Movable objects in the
    # processGameOpsQueue() method.
    #
    # Observer (Movable): Each Movable object implements the lifecycle methods (addToGame, removeFromGame). These methods are
    # called by the Game's processGameOpsQueue() method to notify the Movable objects about their state changes (e.g.,
    # being added to or removed from the game).

    def addToGame(self, list):
        if (CommandCenter.getInstance().falcon.nukeMeter > 0):
            list.add(self)
            CommandCenter.getInstance().falcon.nukeMeter = 0
            Sound.playSound("nuke.wav")

    def removeFromGame(self, list):
        if (self.expiry == 0):
            list.remove(self)
