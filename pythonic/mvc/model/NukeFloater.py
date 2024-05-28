
from pythonic.mvc.controller.CommandCenter import CommandCenter
from pythonic.mvc.controller.Sound import Sound
from pythonic.mvc.model.Floater import Floater
from pythonic.mvc.model.prime.Color import Color
from pythonic.mvc.model.prime.Constants import MAX_NUKE


class NukeFloater(Floater):

    def __init__(self):
        super().__init__()
        #yellow
        self.color = Color.YELLOW
        self.expiry = 350



    def removeFromGame(self, list):
        super().removeFromGame(list)
        # if expiry > 0, then this remove was the result of a collision w/Falcon, and not natural mortality.
        if (self.expiry > 0):
            CommandCenter.getInstance().falcon.nukeMeter = MAX_NUKE
            Sound.playSound( "nuke-up.wav")