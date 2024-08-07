from pythonic.mvc.model.Sprite import Sprite
from pythonic.mvc.model.Movable import Movable
from pythonic.mvc.model.prime.Color import Color
from pythonic.mvc.model.prime.Constants import DIM, UNIVERSAL_SCALER
from pythonic.mvc.model.prime.Point import Point
from pythonic.mvc.model.prime.LinkedList import LinkedList
from PIL import ImageDraw


class MiniMap(Sprite):
    MINI_MAP_PERCENT = 0.31

    def __init__(self):
        super().__init__()
        self.team = Movable.Team.DEBRIS

    def move(self):
        pass

    def draw(self, imgOff):
        g = ImageDraw.Draw(imgOff)
        miniWidth = int(round(self.MINI_MAP_PERCENT * DIM.width))
        miniHeight = int(round(self.MINI_MAP_PERCENT * DIM.height))

        g.rectangle((0,0,miniWidth,miniHeight), fill=Color.BLACK)
        g.rectangle((0,0,miniWidth,miniHeight),outline=Color.BLUE)
        centerOfMiniMap = Point(int(miniWidth / 2), int(miniHeight / 2))
        g.rectangle((centerOfMiniMap.x - (miniWidth / UNIVERSAL_SCALER/2), centerOfMiniMap.y - (miniHeight / UNIVERSAL_SCALER/2), miniWidth / UNIVERSAL_SCALER, miniHeight / UNIVERSAL_SCALER),outline=Color.BLUE)

        from pythonic.mvc.controller.CommandCenter import CommandCenter

        self.drawRadarBlips(imgOff, Color.RED, CommandCenter.getInstance().movFoes)

    def drawRadarBlips(self, imgOff, color : Color, movables):
        g = ImageDraw.Draw(imgOff)
        for mov in movables:
            scaledPoint = Point(int(round(self.MINI_MAP_PERCENT * mov.getCenter().x / UNIVERSAL_SCALER)),
                                int(round(self.MINI_MAP_PERCENT * mov.getCenter().y / UNIVERSAL_SCALER)))
            g.ellipse((scaledPoint.x -2, scaledPoint.y -2,4,4),fill=color)