import os


from pythonic.mvc.controller.Sound import Sound

from pythonic.mvc.model.prime.Constants import MAX_SHIELD
from pythonic.mvc.model.Floater import Floater

from pythonic.mvc.model.prime.Color import Color
class ShieldFloater(Floater):
    def __init__(self):
        super().__init__()
        self.cwd = "/".join(os.getcwd().split("/")[:-2]) + "/resources/sounds/"
        self.color = Color.CYAN
        self.expiry = 260
    def add(self, list):
        list.append(self)



    def remove(self, list):
        from pythonic.mvc.controller.CommandCenter import CommandCenter
        self.alive = False
        if (self.expiry > 0):
            Sound.playSound(self.cwd + "shieldup.wav")
            CommandCenter.getInstance().falcon.shield = MAX_SHIELD