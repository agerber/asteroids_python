from pythonic.mvc.model.Sprite import Sprite
from pythonic.mvc.model.Movable import Movable
from pythonic.mvc.model.prime.Color import Color
from pythonic.mvc.model.prime.Constants import DIM, BIG_UNIVERSAL_SCALER
from pythonic.mvc.model.prime.Point import Point
from pythonic.mvc.model.prime.LinkedList import LinkedList
from PIL import ImageDraw


class MiniMap(Sprite):
    MINI_MAP_PERCENT = 0.42

    def __init__(self):
        super().__init__()
        self.team = Movable.Team.DEBRIS
        self.center = Point(0,0)

    def move(self):
        pass

    def draw(self, imgOff):

        from pythonic.mvc.controller.CommandCenter import CommandCenter,Universe

        if CommandCenter.getInstance().universe == Universe.SMALL:    return

        g = ImageDraw.Draw(imgOff)
        width = int(round(self.MINI_MAP_PERCENT * DIM.width))
        height = int(round(self.MINI_MAP_PERCENT * DIM.height))

        if CommandCenter.getInstance().universe == Universe.BIG:
            g.rectangle((0, 1, width, height), fill=Color.BLACK)
            g.rectangle((0, 1, width, height), outline=Color.GREY)

        miniViewPortWidth = width / BIG_UNIVERSAL_SCALER
        miniViewPortHeight = height / BIG_UNIVERSAL_SCALER

        g.rectangle((0, 1, miniViewPortWidth,
                     miniViewPortHeight), outline=Color.GREY)

        self.drawRadarBlips(imgOff, Color.WHITE, CommandCenter.getInstance().movFoes)
        self.drawRadarBlips(imgOff, Color.CYAN, CommandCenter.getInstance().movFloaters)
        self.drawRadarBlips(imgOff, Color.ORANGE, CommandCenter.getInstance().movFriends)
        self.drawRadarBlips(imgOff, Color.GREY, CommandCenter.getInstance().movDebris)

    def drawRadarBlips(self, imgOff, color: Color, movables):
        g = ImageDraw.Draw(imgOff)
        for mov in movables:
            print(mov.getCenter().x, " ", mov.getCenter().x)
            scaledPoint = Point(int(round(self.MINI_MAP_PERCENT * mov.getCenter().x / BIG_UNIVERSAL_SCALER)),
                                int(round(self.MINI_MAP_PERCENT * mov.getCenter().y / BIG_UNIVERSAL_SCALER)))
            g.ellipse((scaledPoint.x - 2, scaledPoint.y - 2, 10, 10), fill=color)
