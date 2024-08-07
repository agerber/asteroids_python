from pythonic.mvc.model.AspectDim import AspectDim
from pythonic.mvc.model.Sprite import Sprite
from pythonic.mvc.model.Movable import Movable
from pythonic.mvc.model.prime.Color import Color
from pythonic.mvc.model.prime.Constants import DIM, BIG_UNIVERSAL_SCALER
from pythonic.mvc.model.prime.Point import Point
from pythonic.mvc.model.prime.LinkedList import LinkedList
from PIL import ImageDraw


class MiniMap(Sprite):
    MINI_MAP_PERCENT = 0.31

    def __init__(self):
        super().__init__()
        self.team = Movable.Team.DEBRIS
        self.center = Point(0, 0)
        self.pumpkin = Color.from_RGB(200, 100, 50)

    def move(self):
        pass

    def draw(self, imgOff):

        from pythonic.mvc.controller.CommandCenter import CommandCenter, Universe

        if CommandCenter.getInstance().universe == Universe.FREE_FLY:    return

        aspectDim = self.aspectAdjustedDimension(CommandCenter.getInstance().getUniDim())

        g = ImageDraw.Draw(imgOff)
        miniWidth = int(round(self.MINI_MAP_PERCENT * DIM.width * aspectDim.width))
        miniHeight = int(round(self.MINI_MAP_PERCENT * DIM.height * aspectDim.height))

        if CommandCenter.getInstance().universe == Universe.BIG:
            g.rectangle((0, 0, miniWidth, miniHeight), fill=Color.BLACK)
            g.rectangle((0, 0, miniWidth, miniHeight), outline=Color.GREY)

        miniViewPortWidth = miniWidth / CommandCenter.getInstance().getUniDim().width
        miniViewPortHeight = miniHeight / CommandCenter.getInstance().getUniDim().height

        g.rectangle((0, 1, miniViewPortWidth,
                     miniViewPortHeight), outline=Color.GREY)

        for mov in CommandCenter.getInstance().movDebris:
            scaledPoint = self.scalePoint(mov.getCenter())
            g.ellipse((scaledPoint.x - 1, scaledPoint.y - 1, 2, 2), fill=Color.GREY)

        for mov in CommandCenter.getInstance().movFoes:
            scaledPoint = self.scalePoint(mov.getCenter())
            g.ellipse((scaledPoint.x - 2, scaledPoint.y - 2, 4, 4), fill=Color.WHITE)

        for mov in CommandCenter.getInstance().movFloaters:
            scaledPoint = self.scalePoint(mov.getCenter())
            g.ellipse((scaledPoint.x - 2, scaledPoint.y - 2, 4, 4), fill=Color.YELLOW)

        for mov in CommandCenter.getInstance().movFriends:
            scaledPoint = self.scalePoint(mov.getCenter())
            g.ellipse((scaledPoint.x - 2, scaledPoint.y - 2, 4, 4), fill=Color.CYAN)

    def scalePoint(self, mov):
        from pythonic.mvc.controller.CommandCenter import CommandCenter, Universe
        aspectDim = self.aspectAdjustedDimension(CommandCenter.getInstance().getUniDim())

        return Point(int(round(self.MINI_MAP_PERCENT * mov.x / CommandCenter.getInstance().getUniDim().width * aspectDim.width)),
                     int(round(self.MINI_MAP_PERCENT * mov.y / CommandCenter.getInstance().getUniDim().height * aspectDim.height)))

    def aspectAdjustedDimension(self, universeDim):
        if universeDim.width == universeDim.height:
            return AspectDim(1.0,1.0)
        elif universeDim.width > universeDim.height:
            wMultiple = float(universeDim.width/universeDim.height)
            return AspectDim(wMultiple, 1.0).scale(0.5)
        else:
            hMultiple = float(universeDim.height / universeDim.width)
            return AspectDim(1.0, hMultiple).scale(0.5)