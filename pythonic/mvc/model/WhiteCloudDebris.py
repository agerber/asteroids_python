from pythonic.mvc.model.Sprite import Sprite
from pythonic.mvc.model.Movable import Movable
import os

class WhiteCloudDebris(Sprite):


    def __init__(self, explodingSprite: Sprite):
        super().__init__()
        self.team = Movable.Team.DEBRIS
        self.index = 0

        root_path = "/".join(os.getcwd().split("/")[:-2])+"/"+"resources"
        self.rasterMap[0] = self.loadGraphic(root_path+"/imgs/exp/row-1-column-1.png")
        self.rasterMap[1] = self.loadGraphic(root_path+"/imgs/exp/row-1-column-2.png")
        self.rasterMap[2] = self.loadGraphic(root_path+"/imgs/exp/row-1-column-3.png")
        self.rasterMap[3] = self.loadGraphic(root_path+"/imgs/exp/row-2-column-1.png")
        self.rasterMap[4] = self.loadGraphic(root_path+"/imgs/exp/row-2-column-2.png")
        self.rasterMap[5] = self.loadGraphic(root_path+"/imgs/exp/row-2-column-3.png")
        self.rasterMap[6] = self.loadGraphic(root_path+"/imgs/exp/row-3-column-1.png")
        self.rasterMap[7] = self.loadGraphic(root_path+"/imgs/exp/row-3-column-2.png")
        self.rasterMap[8] = self.loadGraphic(root_path+"/imgs/exp/row-3-column-3.png")

        #expire it out after it has done its animation. Multiply by 2 to slow down the animation
        self.expiry = len(self.rasterMap) * 2
        self.spin = explodingSprite.spin
        self.center = explodingSprite.center
        self.deltaX = explodingSprite.deltaX
        self.deltaY = explodingSprite.deltaY
        self.radius = int(explodingSprite.radius *1.3)

    def draw(self, imgOff):
        self.renderRaster(imgOff, self.rasterMap[self.index])
        #hold the image for two frames to slow down the dust cloud animation
        #we already have a simple decrement-to-zero counter with expiry; see move() method of Sprite.
        if self.expiry % 2 == 0:
            self.index = self.index + 1

    def add(self, list):
        list.append(self)


    def remove(self, list):
        self.alive = False