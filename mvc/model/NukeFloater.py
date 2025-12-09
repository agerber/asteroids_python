
from mvc.controller.CommandCenter import CommandCenter
from mvc.controller.SoundLoader import SoundLoader
from mvc.model.Floater import Floater
from mvc.model.prime.Color import Color
from mvc.model.prime.Constants import MAX_NUKE


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
            SoundLoader.playSound("nuke-up.wav")