from pythonic.mvc.model.prime.AspectRatio import AspectRatio
from pythonic.mvc.model.Falcon import Falcon

from pythonic.mvc.model.Sprite import Sprite
from pythonic.mvc.model.Movable import Movable
from pythonic.mvc.model.prime.Color import Color
from pythonic.mvc.model.prime.Constants import DIM
from pythonic.mvc.model.prime.Point import Point
from PIL import ImageDraw


class MiniMap(Sprite):
    MINI_MAP_PERCENT = 0.31
    PUMPKIN = Color.from_RGB(200, 100, 50)
    LIGHT_GRAY = Color.from_RGB(200, 200, 200)

    def __init__(self):
        super().__init__()
        self.team = Movable.Team.DEBRIS
        self.center = Point(0, 0)
        self.PUMPKIN = Color.from_RGB(200, 100, 50)
        self.aspectRatio = AspectRatio(1, 1)

    def move(self):
        pass

    def draw(self, imgOff):

        from pythonic.mvc.model.Nuke import Nuke
        from pythonic.mvc.model.NukeFloater import NukeFloater
        from pythonic.mvc.controller.CommandCenter import CommandCenter
        from pythonic.mvc.model.Asteroid import Asteroid


        if not (CommandCenter.getInstance().radar): return

        self.aspectRatio = self.aspectAdjustedRatio(CommandCenter.getInstance().getUniDim())

        # get the graphic context
        g = ImageDraw.Draw(imgOff)

        miniWidth = int(round(self.MINI_MAP_PERCENT * DIM.width * self.aspectRatio.width))
        miniHeight = int(round(self.MINI_MAP_PERCENT * DIM.height * self.aspectRatio.height))


        # draw the entire universe bounding box
        g.rectangle((0, 0, miniWidth, miniHeight), outline=Color.GREY, fill=Color.BLACK)

        miniViewPortWidth = miniWidth / CommandCenter.getInstance().getUniDim().width
        miniViewPortHeight = miniHeight / CommandCenter.getInstance().getUniDim().height

        # draw the portal bounding box
        g.rectangle((0, 0, miniViewPortWidth,
                     miniViewPortHeight), outline=Color.GREY,fill=Color.BLACK)

        # draw foes blips
        for mov in CommandCenter.getInstance().movFoes:
            translatedPoint = self.translatePoint(mov.getCenter())
            asteroid: Asteroid = mov

            if asteroid.getSize() == 0:
                # large
                g.ellipse((translatedPoint.x - 3, translatedPoint.y - 3, translatedPoint.x + 3, translatedPoint.y + 3), fill=Color.WHITE)
            elif asteroid.getSize() == 1:
                # medium
                g.ellipse((translatedPoint.x - 3, translatedPoint.y - 3, translatedPoint.x + 3, translatedPoint.y + 3))
            else:
                # small or default
                g.ellipse((translatedPoint.x - 2, translatedPoint.y - 2, translatedPoint.x + 2, translatedPoint.y + 2))


        # draw floaters blips
        for mov in CommandCenter.getInstance().movFloaters:
            translatedPoint = self.translatePoint(mov.getCenter())
            color = Color.YELLOW if isinstance(mov, NukeFloater) else Color.CYAN
            g.ellipse((translatedPoint.x - 2, translatedPoint.y - 2, translatedPoint.x + 2, translatedPoint.y + 2), fill=color)

        # draw freinds blips
        for mov in CommandCenter.getInstance().movFriends:
            if isinstance(mov, Falcon) and CommandCenter.getInstance().falcon.shield > 0:
                color = Color.CYAN
            elif isinstance(mov, Nuke):
                color = Color.YELLOW
            else:
                color = self.PUMPKIN
            translatedPoint = self.translatePoint(mov.getCenter())
            g.ellipse((translatedPoint.x - 2, translatedPoint.y - 2, translatedPoint.x + 2, translatedPoint.y + 2), fill=color)

    def translatePoint(self, mov):
        from pythonic.mvc.controller.CommandCenter import CommandCenter

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