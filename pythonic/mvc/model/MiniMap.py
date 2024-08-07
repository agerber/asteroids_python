from pythonic.mvc.model.Sprite import Sprite
from pythonic.mvc.model.Movable import Movable
from pythonic.mvc.model.prime.Color import Color
from pythonic.mvc.model.prime.Constants import DIM, UNIVERSAL_SCALER
from pythonic.mvc.model.prime.Point import Point
from pythonic.mvc.model.prime.LinkedList import LinkedList
from PIL import ImageDraw


class MiniMap(Sprite):
    MINI_MAP_PERCENT = 0.42

    def __init__(self):
        super().__init__()
        self.team = Movable.Team.DEBRIS

    def move(self):
        pass

    def draw(self, imgOff):

        from pythonic.mvc.controller.CommandCenter import CommandCenter,Universe

        if CommandCenter.getInstance().universe != Universe.BIG:    return

        g = ImageDraw.Draw(imgOff)
        miniWidth = int(round(self.MINI_MAP_PERCENT * DIM.width))
        miniHeight = int(round(self.MINI_MAP_PERCENT * DIM.height))

        miniViewPortWidth = miniWidth / UNIVERSAL_SCALER
        miniViewPortHeight = miniHeight / UNIVERSAL_SCALER

        g.rectangle((0, 1, miniWidth, miniHeight), fill=Color.BLACK)
        g.rectangle((0, 1, miniWidth, miniHeight), outline=Color.BLUE)
        g.rectangle((0, 1, miniViewPortWidth,
                     miniViewPortHeight), outline=Color.BLUE)


        from pythonic.mvc.controller.CommandCenter import CommandCenter

        self.drawRadarBlips(imgOff, Color.WHITE, CommandCenter.getInstance().movFoes)
        self.drawRadarBlips(imgOff, Color.CYAN, CommandCenter.getInstance().movFloaters)
        self.drawRadarBlips(imgOff, Color.ORANGE, CommandCenter.getInstance().movFriends)

    def drawRadarBlips(self, imgOff, color: Color, movables):
        g = ImageDraw.Draw(imgOff)
        for mov in movables:
            print(mov.getCenter().x, " ", mov.getCenter().x)
            scaledPoint = Point(int(round(self.MINI_MAP_PERCENT * mov.getCenter().x / UNIVERSAL_SCALER)),
                                int(round(self.MINI_MAP_PERCENT * mov.getCenter().y / UNIVERSAL_SCALER)))
            g.ellipse((scaledPoint.x - 2, scaledPoint.y - 2, 10, 10), fill=color)
