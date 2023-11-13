from math import cos, sin, radians

from pythonic.mvc.controller.CommandCenter import CommandCenter
from pythonic.mvc.controller.Sound import Sound
from pythonic.mvc.model.Falcon import Falcon
from pythonic.mvc.model.Movable import Movable
from pythonic.mvc.model.Sprite import Sprite
from pythonic.mvc.model.prime.Point import Point
from pythonic.mvc.model.prime.Color import Color
from typing import Dict
from PIL import Image, ImageDraw

from pythonic.mvc.model.Movable import Movable
from pythonic.mvc.model.Sprite import Sprite
from pythonic.mvc.model.prime.Color import Color
from enum import Enum
import math
import os


class Brick(Sprite):

    BRICK_IMAGE = 0
    def __init__(self, upperLeftCorner: Point, size: int):
        super().__init__()
        self.team = Movable.Team.FOE
        self.center = Point(int(upperLeftCorner.x + size/2), int(upperLeftCorner.y + size/2))
        self.radius = int(size / 2)
        # We use a dictionary that has a seek-time of O(1)
        # Using enums as keys is safer b/c we know the value exists when we reference the consts later in code.
        self.rasterMap: Dict[int, Image.Image] = {
            Brick.BRICK_IMAGE: self.loadGraphic(CommandCenter.getInstance().img + "brick/Brick_Block100.png")
        }

    def draw(self, imgOff):
        self.renderRaster(imgOff, self.rasterMap[Brick.BRICK_IMAGE])

    def move(self):
        pass



    def remove(self, list):
        list.remove(self)
        CommandCenter.getInstance().score += 1000
        Sound.playSound(CommandCenter.getInstance().snd + "rock.wav")