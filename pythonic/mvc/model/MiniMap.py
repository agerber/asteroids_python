from pythonic.mvc.controller import Game
from pythonic.mvc.model.Movable import Movable
from pythonic.mvc.model.Sprite import Sprite
from pythonic.mvc.model.prime.Color import Color
from pythonic.mvc.model.prime.Point import Point
from pythonic.mvc.controller.CommandCenter import CommandCenter


class MiniMap(Sprite):
    # size of mini-map as percentage of view-port
    MINI_MAP_PERCENT = 0.42

    def __init__(self):
        self.team = Movable.Team.DEBRIS

    def move(self):
        pass

    def draw(self, g):


        from pythonic.mvc.model.prime.Universe import Universe

        if CommandCenter.getInstance().universe == Universe.SMALL:
            return

        width = round(self.MINI_MAP_PERCENT * Game.DIM.width)
        height = round(self.MINI_MAP_PERCENT * Game.DIM.height)

        # if BIG - show entire universe.
        if CommandCenter.getUniverse() == Universe.BIG:
            g.setColor(Color.BLACK)
            g.fillRect(0, 1, width, height)

            # gray bounding box (entire universe)
            g.setColor(Color.DARK_GRAY)
            g.drawRect(0, 1, width, height)

        # mini-view-port gray bounding box (player's view of universe)
        g.setColor(Color.DARK_GRAY)
        miniViewPortWidth = width // Game.BIG_UNIVERSE_SCALAR
        miniViewPortHeight = height // Game.BIG_UNIVERSE_SCALAR
        g.drawRect(0, 1, miniViewPortWidth, miniViewPortHeight)

        # draw the non-debris movables
        self.drawRadarBlips(g, Color.WHITE, CommandCenter.getMovFoes())
        self.drawRadarBlips(g, Color.CYAN, CommandCenter.getMovFloaters())
        self.drawRadarBlips(g, Color.ORANGE, CommandCenter.getMovFriends())

    def drawRadarBlips(self, g, color, movables):
        from pythonic.mvc.controller.Game import Game
        g.setColor(color)
        for mov in movables:
            scaledPoint = Point(
                round(self.MINI_MAP_PERCENT * mov.getCenter().x / Game.BIG_UNIVERSE_SCALAR),
                round(self.MINI_MAP_PERCENT * mov.getCenter().y / Game.BIG_UNIVERSE_SCALAR)
            )
            g.fillOval(scaledPoint.x - 2, scaledPoint.y - 2, 4, 4)
