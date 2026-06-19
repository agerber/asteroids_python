
from mvc.model.Falcon import Falcon

from mvc.model.Sprite import Sprite
from mvc.model.Movable import Movable
from mvc.model.prime.Color import Color
from mvc.model.prime.Constants import DIM
from mvc.model.prime.Point import Point
from mvc.model.Nuke import Nuke
from mvc.model.NukeFloater import NukeFloater
from mvc.model.Asteroid import Asteroid
from mvc.controller.CommandCenter import CommandCenter


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

    def draw(self, g):
        if not (CommandCenter.getInstance().isRadar): return

        radarW = int(round(self.MINI_MAP_PERCENT * DIM.width ))
        radarH = int(round(self.MINI_MAP_PERCENT * DIM.height))


        # draw the entire universe bounding box (black fill, grey border)
        g.setColor(Color.BLACK)
        g.fillRect(0, 0, radarW, radarH)
        g.setColor(Color.GREY)
        g.drawRect(0, 0, radarW, radarH)

        viewPortWidth = int(radarW / CommandCenter.getInstance().getUniDim().width)
        viewPortHeight = int(radarH / CommandCenter.getInstance().getUniDim().height)

        # draw the portal bounding box
        g.setColor(Color.BLACK)
        g.fillRect(0, 0, viewPortWidth, viewPortHeight)
        g.setColor(Color.GREY)
        g.drawRect(0, 0, viewPortWidth, viewPortHeight)

        # draw foes blips
        for mov in CommandCenter.getInstance().movFoes:
            translatedPoint = self.translatePoint(mov.getCenter())
            asteroid: Asteroid = mov

            if asteroid.getSize() == 0:
                # large
                g.setColor(Color.WHITE)
                g.fillOval(translatedPoint.x - 3, translatedPoint.y - 3, 6, 6)
            elif asteroid.getSize() == 1:
                # medium
                g.setColor(Color.WHITE)
                g.drawOval(translatedPoint.x - 3, translatedPoint.y - 3, 6, 6)
            else:
                # small or default
                g.setColor(Color.WHITE)
                g.drawOval(translatedPoint.x - 2, translatedPoint.y - 2, 4, 4)


        # draw floaters blips
        for mov in CommandCenter.getInstance().movFloaters:
            translatedPoint = self.translatePoint(mov.getCenter())
            g.setColor(Color.YELLOW if isinstance(mov, NukeFloater) else Color.CYAN)
            g.fillOval(translatedPoint.x - 2, translatedPoint.y - 2, 4, 4)

        # draw friends blips
        for mov in CommandCenter.getInstance().movFriends:
            if isinstance(mov, Falcon) and CommandCenter.getInstance().falcon.shield > 0:
                color = Color.CYAN
            elif isinstance(mov, Nuke):
                color = Color.YELLOW
            else:
                color = self.PUMPKIN
            translatedPoint = self.translatePoint(mov.getCenter())
            g.setColor(color)
            g.fillOval(translatedPoint.x - 2, translatedPoint.y - 2, 4, 4)

    def translatePoint(self, mov):
        return Point(int(round(self.MINI_MAP_PERCENT * mov.x / CommandCenter.getInstance().getUniDim().width )),
                     int(round(self.MINI_MAP_PERCENT * mov.y / CommandCenter.getInstance().getUniDim().height )))

