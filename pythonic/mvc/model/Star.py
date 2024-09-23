import random

from pythonic.mvc.model.prime.Point import Point
from pythonic.mvc.model.prime.Color import Color
from pythonic.mvc.model.prime.Constants import DIM
from pythonic.mvc.model.Movable import Movable
from PIL import ImageDraw


class Star(Movable):

    def __init__(self):
        self.center = Point(random.randint(0, DIM.width), random.randint(0, DIM.height))
        bright = random.randint(0, 225)
        self.color = Color.from_RGB(bright, bright, bright)  # some gray value. stars are muted from 0-225 / 255

    def move(self):
        from pythonic.mvc.controller.CommandCenter import CommandCenter, Universe

        if not CommandCenter.getInstance().isFalconPositionFixed():  return
            # right-bounds reached
        if self.center.x > DIM.width:
            self.center.x = 1
            # left-bounds reached
        elif self.center.x < 0:
            self.center.x = DIM.width - 1
            # bottom-bounds reached
        elif self.center.y > DIM.height:
            self.center.y = 1
            # top-bounds reached
        elif self.center.y < 0:
            self.center.y = DIM.height - 1
            # in-bounds
        else:
            # move star in opposite direction of falcon
            new_x_pos = self.center.x - CommandCenter.getInstance().falcon.deltaX
            new_y_pos = self.center.y - CommandCenter.getInstance().falcon.deltaY
            self.center = Point(int(round(new_x_pos)), int(round(new_y_pos)))

    def draw(self, imgOff):
        # get the graphics context of the off-screen-image and draw to it
        g = ImageDraw.Draw(imgOff)
        g.ellipse((self.center.x, self.center.y,
                   self.center.x + self.getRadius(), self.center.y + self.getRadius()), outline=self.color)

    def getRadius(self) -> int:
        return 1

    def getTeam(self) -> Movable.Team:
        return Movable.Team.DEBRIS

    def getCenter(self) -> Point:
        return self.center

    def addToGame(self, list):
        list.add(self)

    def removeFromGame(self, list):
        list.remove(self)
