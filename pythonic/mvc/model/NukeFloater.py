from pythonic.mvc.model.Floater import Floater
from pythonic.mvc.model.prime.Color import Color


class NukeFloater(Floater):

    def __init__(self):
        super().__init__()

        #yellow
        self.color = Color.YELLOW
        self.expiry = 350
    def add(self, list):
        list.append(self)


    def remove(self, list):
        self.alive = False