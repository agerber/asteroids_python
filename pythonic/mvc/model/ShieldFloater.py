from pythonic.mvc.controller.Sound import Sound

from pythonic.mvc.model.prime.Constants import MAX_SHIELD
from pythonic.mvc.model.Floater import Floater

from pythonic.mvc.model.prime.Color import Color


class ShieldFloater(Floater):
    def __init__(self):
        super().__init__()
        self.color = Color.CYAN
        self.expiry = 260

    def removeFromGame(self, list):
        from pythonic.mvc.controller.CommandCenter import CommandCenter

        super().removeFromGame(list)
        # if expiry > 0, then this remove was the result of a collision w/Falcon, and not natural mortality.
        if (self.expiry > 0):
            Sound.playSound("shieldup.wav")
            CommandCenter.getInstance().falcon.shield = MAX_SHIELD
