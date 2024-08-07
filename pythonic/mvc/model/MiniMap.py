from pythonic.mvc.model.Sprite import Sprite
from pythonic.mvc.model.Movable import Movable
from pythonic.mvc.model.prime.Color import Color
from pythonic.mvc.model.prime.Constants import DIM, BIG_UNIVERSAL_SCALER
from pythonic.mvc.model.prime.Point import Point
from pythonic.mvc.model.prime.LinkedList import LinkedList
from PIL import ImageDraw


class MiniMap(Sprite):
    MINI_MAP_PERCENT = 0.23

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
        miniWidth = int(round(self.MINI_MAP_PERCENT * DIM.width))
        miniHeight = int(round(self.MINI_MAP_PERCENT * DIM.height))

        if CommandCenter.getInstance().universe == Universe.BIG_CENTERED:
            g.rectangle((0, 1, miniWidth, miniHeight), fill=Color.BLACK)
            g.rectangle((0, 1, miniWidth, miniHeight), outline=Color.GREY)

        miniViewPortWidth = miniWidth / BIG_UNIVERSAL_SCALER
        miniViewPortHeight = miniHeight / BIG_UNIVERSAL_SCALER

        g.rectangle((0, 1, miniViewPortWidth,
                     miniViewPortHeight), outline=Color.GREY)

        for mov in CommandCenter.getInstance().movDebris:
            scaledPoint = Point(int(round(self.MINI_MAP_PERCENT * mov.getCenter().x / BIG_UNIVERSAL_SCALER)),
                                int(round(self.MINI_MAP_PERCENT * mov.getCenter().y / BIG_UNIVERSAL_SCALER)))
            g.ellipse((scaledPoint.x - 1, scaledPoint.y - 1, 2, 2), fill=Color.GREY)

        for mov in CommandCenter.getInstance().movFoes:
            scaledPoint = Point(int(round(self.MINI_MAP_PERCENT * mov.getCenter().x / BIG_UNIVERSAL_SCALER)),
                                int(round(self.MINI_MAP_PERCENT * mov.getCenter().y / BIG_UNIVERSAL_SCALER)))
            g.ellipse((scaledPoint.x - 2, scaledPoint.y - 2, 4, 4), fill=Color.WHITE)

        for mov in CommandCenter.getInstance().movFloaters:
            scaledPoint = Point(int(round(self.MINI_MAP_PERCENT * mov.getCenter().x / BIG_UNIVERSAL_SCALER)),
                                int(round(self.MINI_MAP_PERCENT * mov.getCenter().y / BIG_UNIVERSAL_SCALER)))
            g.ellipse((scaledPoint.x - 2, scaledPoint.y - 2, 4, 4), fill=Color.YELLOW)

        for mov in CommandCenter.getInstance().movFriends:
            scaledPoint = Point(int(round(self.MINI_MAP_PERCENT * mov.getCenter().x / BIG_UNIVERSAL_SCALER)),
                                int(round(self.MINI_MAP_PERCENT * mov.getCenter().y / BIG_UNIVERSAL_SCALER)))
            g.ellipse((scaledPoint.x - 2, scaledPoint.y - 2, 4, 4), fill=Color.CYAN)


