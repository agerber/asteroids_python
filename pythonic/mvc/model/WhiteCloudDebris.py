from pythonic.mvc.model.Sprite import Sprite
from pythonic.mvc.model.Movable import Movable
import os

class WhiteCloudDebris(Sprite):

    def __init__(self, explodingSprite: Sprite):
        super().__init__()
        self.team = Movable.Team.DEBRIS

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

        self.expiry = len(self.rasterMap)
        self.spin = explodingSprite.spin
        self.center = explodingSprite.center
        self.deltaX = explodingSprite.deltaX
        self.deltaY = explodingSprite.deltaY
        self.radius = int(explodingSprite.radius *1.3)

    def draw(self, imgOff):
        index = len(self.rasterMap) - self.expiry - 1
        self.renderRaster(imgOff, self.rasterMap[index])

    def add(self, list):
        list.append(self)


    def remove(self, list):
        list.remove(self)