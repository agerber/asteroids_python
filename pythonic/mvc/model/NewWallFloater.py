from pythonic.mvc.model.Floater import Floater
from pythonic.mvc.model.prime.Color import Color


class NewWallFloater(Floater):

    def __init__(self):
        super().__init__()

        self.color = Color.from_RGB(186, 0, 22)
        self.expiry = 230
