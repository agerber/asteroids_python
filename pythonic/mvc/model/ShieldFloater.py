

from pythonic.mvc.model.Floater import Floater

from pythonic.mvc.model.prime.Color import Color
class ShieldFloater(Floater):
    def __init__(self):
        super().__init__()

        self.color = Color.CYAN
        self.expiry = 260
