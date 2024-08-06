from pythonic.mvc.model.Sprite import Sprite
from pythonic.mvc.model.Movable import Movable
from pythonic.mvc.model.prime.Color import Color
from pythonic.mvc.model.prime.Constants import DIM
from pythonic.mvc.model.prime.Point import Point
from PIL import ImageDraw
class MiniMap(Sprite):
    MAP_MARGIN = 20
    WIDTH_FACTOR = 5
    HEIGHT_FACTOR = 4

    def __init__(self):
        super().__init__()
        self.team = Movable.Team.DEBRIS

    def move(self):
        pass

    def draw(self, imgOff):
        g = ImageDraw.Draw(imgOff)

        g.rectangle((DIM.width - (DIM.width/self.WIDTH_FACTOR) - self.MAP_MARGIN, self.MAP_MARGIN, DIM.width/self.WIDTH_FACTOR + 4, DIM.height/self.HEIGHT_FACTOR + 4), outline=Color.BLACK)
        g.rectangle((DIM.width - (DIM.width / self.WIDTH_FACTOR) - self.MAP_MARGIN, self.MAP_MARGIN, DIM.width / self.WIDTH_FACTOR + 4,
                     DIM.height / self.HEIGHT_FACTOR + 4), outline=Color.BLUE)
        g.rectangle((DIM.width - (2 * DIM.width / (3*self.WIDTH_FACTOR)) - self.MAP_MARGIN, self.MAP_MARGIN + (DIM.height / (3 * self.HEIGHT_FACTOR)), DIM.width / (3 * self.WIDTH_FACTOR),
                     DIM.height / (3 * self.HEIGHT_FACTOR)), outline=Color.BLUE)
