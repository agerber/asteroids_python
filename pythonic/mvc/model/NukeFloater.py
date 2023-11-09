import os

from pythonic.mvc.controller.CommandCenter import CommandCenter
from pythonic.mvc.controller.Sound import Sound
from pythonic.mvc.model.Floater import Floater
from pythonic.mvc.model.prime.Color import Color
from pythonic.mvc.model.prime.Constants import MAX_NUKE


class NukeFloater(Floater):

    def __init__(self):
        super().__init__()
        self.cwd = "/".join(os.getcwd().split("/")[:-2]) + "/resources/sounds/"
        #yellow
        self.color = Color.YELLOW
        self.expiry = 350
    def add(self, list):
        list.append(self)


    def remove(self, list):
        self.alive = False
        if (self.expiry > 0):
            CommandCenter.getInstance().falcon.nukeMeter = MAX_NUKE
            Sound.playSound(self.cwd + "nuke-up.wav")