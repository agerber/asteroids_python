from mvc.model.Sprite import Sprite
from mvc.model.Movable import Movable
from mvc.controller.ImageLoader import ImageLoader


class WhiteCloudDebris(Sprite):
    # static variable
    SLOW_MO = 3

    def __init__(self, explodingSprite: Sprite):
        super().__init__()
        self.team = Movable.Team.DEBRIS
        self.index = 0
        self.rasterMap[0] = ImageLoader.getInstance().IMAGES['row-1-column-1']
        self.rasterMap[1] = ImageLoader.getInstance().IMAGES['row-1-column-2']
        self.rasterMap[2] = ImageLoader.getInstance().IMAGES['row-1-column-3']
        self.rasterMap[3] = ImageLoader.getInstance().IMAGES['row-2-column-1']
        self.rasterMap[4] = ImageLoader.getInstance().IMAGES['row-2-column-2']
        self.rasterMap[5] = ImageLoader.getInstance().IMAGES['row-2-column-3']
        self.rasterMap[6] = ImageLoader.getInstance().IMAGES['row-3-column-1']
        self.rasterMap[7] = ImageLoader.getInstance().IMAGES['row-3-column-2']
        self.rasterMap[8] = ImageLoader.getInstance().IMAGES['row-3-column-3']

        # expire it out after it has done its animation. Multiply by SLOW_MO to slow down the animation
        self.expiry = len(self.rasterMap) * WhiteCloudDebris.SLOW_MO
        self.spin = explodingSprite.spin
        self.center = explodingSprite.center
        self.deltaX = explodingSprite.deltaX
        self.deltaY = explodingSprite.deltaY
        self.radius = int(explodingSprite.radius * 1.3)

    def draw(self, imgOff):
        self.renderRaster(imgOff, self.rasterMap[self.index])
        # hold the image for SLOW_MO frames to slow down the dust cloud animation
        # we already have a simple decrement-to-zero counter with expiry; see move() method of Sprite.
        if self.expiry % WhiteCloudDebris.SLOW_MO == 0:
            self.index = self.index + 1
