
from mvc.model.Falcon import Falcon

from mvc.model.Sprite import Sprite
from mvc.model.Movable import Movable
from mvc.model.prime.Color import Color
from mvc.model.prime.Constants import DIM
from mvc.model.prime.Point import Point
from PIL import ImageDraw


class Radar(Sprite):
    MINI_MAP_PERCENT = 0.31
    PUMPKIN = Color.from_RGB(200, 100, 50)
    LIGHT_GRAY = Color.from_RGB(200, 200, 200)

    def __init__(self):
        super().__init__()
        self.team = Movable.Team.DEBRIS
        self.center = Point(0, 0)



    def move(self):
        pass

    def draw(self, imgOff):
        # import locally to avoid circ deps
        from mvc.model.Nuke import Nuke
        from mvc.model.NukeFloater import NukeFloater
        from mvc.controller.CommandCenter import CommandCenter
        from mvc.model.Asteroid import Asteroid


        if not (CommandCenter.getInstance().isRadar): return

        # get the graphic context
        g = ImageDraw.Draw(imgOff)

        radarW = int(round(self.MINI_MAP_PERCENT * DIM.width ))
        radarH = int(round(self.MINI_MAP_PERCENT * DIM.height))


        # draw the entire universe bounding box
        g.rectangle((0, 0, radarW, radarH), outline=Color.GREY, fill=Color.BLACK)

        viewPortWidth = radarW / CommandCenter.getInstance().getUniDim().width
        viewPortHeight = radarH / CommandCenter.getInstance().getUniDim().height

        # draw the portal bounding box
        g.rectangle((0, 0, viewPortWidth,
                     viewPortHeight), outline=Color.GREY,fill=Color.BLACK)

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
        from mvc.controller.CommandCenter import CommandCenter

        return Point(int(round(self.MINI_MAP_PERCENT * mov.x / CommandCenter.getInstance().getUniDim().width )),
                     int(round(self.MINI_MAP_PERCENT * mov.y / CommandCenter.getInstance().getUniDim().height )))

