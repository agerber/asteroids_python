from pythonic.mvc.model.AspectRatio import AspectRatio
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
        self.aspectRatio = AspectRatio(1, 1)

    def move(self):
        pass

    def draw(self, imgOff):

        from pythonic.mvc.controller.CommandCenter import CommandCenter, Universe

        #if CommandCenter.getInstance().universe == Universe.FREE_FLY:    return

        self.aspectRatio = self.aspectAdjustedRatio(CommandCenter.getInstance().getUniDim())

        g = ImageDraw.Draw(imgOff)
        miniWidth = int(round(self.MINI_MAP_PERCENT * DIM.width * self.aspectRatio.width))
        miniHeight = int(round(self.MINI_MAP_PERCENT * DIM.height * self.aspectRatio.height))


        #g.rectangle((0, 0, miniWidth, miniHeight), fill=Color.BLACK)
        g.rectangle((0, 0, miniWidth, miniHeight), outline=Color.GREY)

        miniViewPortWidth = miniWidth / CommandCenter.getInstance().getUniDim().width
        miniViewPortHeight = miniHeight / CommandCenter.getInstance().getUniDim().height

        g.rectangle((0, 1, miniViewPortWidth,
                     miniViewPortHeight), outline=Color.GREY)

        for mov in CommandCenter.getInstance().movDebris:
            translatedPoint = self.translatePoint(mov.getCenter())
            g.ellipse((translatedPoint.x - 1, translatedPoint.y - 1, translatedPoint.x + 1, translatedPoint.y + 1), fill=Color.GREY)

        for mov in CommandCenter.getInstance().movFoes:
            translatedPoint = self.translatePoint(mov.getCenter())
            g.ellipse((translatedPoint.x - 2, translatedPoint.y - 2, translatedPoint.x + 2, translatedPoint.y + 2), fill=Color.WHITE)

        for mov in CommandCenter.getInstance().movFloaters:
            translatedPoint = self.translatePoint(mov.getCenter())
            g.ellipse((translatedPoint.x - 2, translatedPoint.y - 2, translatedPoint.x + 2, translatedPoint.y + 2), fill=Color.YELLOW)

        for mov in CommandCenter.getInstance().movFriends:
            translatedPoint = self.translatePoint(mov.getCenter())
            g.ellipse((translatedPoint.x - 2, translatedPoint.y - 2, translatedPoint.x + 2, translatedPoint.y + 2), fill=Color.CYAN)

    def translatePoint(self, mov):
        from pythonic.mvc.controller.CommandCenter import CommandCenter, Universe

        return Point(int(round(self.MINI_MAP_PERCENT * mov.x / CommandCenter.getInstance().getUniDim().width * self.aspectRatio.width)),
                     int(round(self.MINI_MAP_PERCENT * mov.y / CommandCenter.getInstance().getUniDim().height * self.aspectRatio.height)))

    def aspectAdjustedRatio(self, universeDim):
        if universeDim.width == universeDim.height:
            return AspectRatio(1.0,1.0)
        elif universeDim.width > universeDim.height:
            wMultiple = float(universeDim.width/universeDim.height)
            return AspectRatio(wMultiple, 1.0).scale(0.5)
        else:
            hMultiple = float(universeDim.height / universeDim.width)
            return AspectRatio(1.0, hMultiple).scale(0.5)