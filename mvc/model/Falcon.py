from dataclasses import dataclass
import random
from typing import Dict
from PIL import Image, ImageDraw

from mvc.model.Movable import Movable
from mvc.model.Sprite import Sprite
from mvc.model.prime.Color import Color
from enum import Enum
import math

from mvc.model.prime.Constants import INITIAL_SPAWN_TIME, DIM
from mvc.model.prime.Point import Point
from mvc.controller import ImageLoader


class TurnState(Enum):
    IDLE = 0
    LEFT = 1
    RIGHT = 2


class ImageState(Enum):
    FALCON_INVISIBLE = 0  # for pre-spawning
    FALCON = 1  # normal ship
    FALCON_THR = 2  # normal ship thrusting
    FALCON_PRO = 3  # protected ship (green)
    FALCON_PRO_THR = 4  # protected ship (green) thrusting


@dataclass
class Falcon(Sprite):
    # number of degrees the falcon will turn at each animation cycle if the turnState is LEFT or RIGHT
    TURN_STEP = 11
    MIN_RADIUS = 28

    def __init__(self):
        super().__init__()
        self.shield = 0
        self.nukeMeter = 0
        self.invisible = 0
        self.maxSpeedAttained = False
        self.showLevel = 0

        # TODO The enum TurnState as well as the boolean thrusting are examples of the State design pattern. This pattern
        # allows an object to change its behavior when its internal state changes. In this case, the boolean thrusting and
        # the TurnState (with values IDLE, LEFT, and RIGHT) affect how the Falcon moves and draws itself.
        self.thrusting = False
        self.turnState = TurnState.IDLE

        self.team = Movable.Team.FRIEND
        self.radius = Falcon.MIN_RADIUS
        # We use a dictionary that has a seek-time of O(1)
        # Using enums as keys is safer b/c we know the value exists when we reference the consts later in code.
        #avoid circular import
        #from pythonic.mvc.controller.CommandCenter import CommandCenter
        self.rasterMap: Dict[ImageState, Image.Image] = {
            ImageState.FALCON_INVISIBLE: None,
            ImageState.FALCON: ImageLoader.ImageLoader.getInstance().IMAGES['falcon125'],
            ImageState.FALCON_THR: ImageLoader.ImageLoader.getInstance().IMAGES['falcon125_thr'],
            ImageState.FALCON_PRO: ImageLoader.ImageLoader.getInstance().IMAGES['falcon125_PRO'],
            ImageState.FALCON_PRO_THR: ImageLoader.ImageLoader.getInstance().IMAGES['falcon125_PRO_thr']
        }

    # METHODS

    def move(self):
        from mvc.controller.CommandCenter import CommandCenter

        if not CommandCenter.getInstance().isFalconPositionFixed():
            super().move()

        if self.invisible > 0: self.invisible -= 1
        if self.shield > 0: self.shield -= 1
        if self.nukeMeter > 0: self.nukeMeter -= 1
        # The falcon is a convenient place to decrement the showLevel variable as the falcon
        # move() method is being called every frame (~40ms); and the falcon reference is never null.
        if self.showLevel > 0: self.showLevel -= 1

        # adjust orientation
        adjustOr = self.orientation

        if self.turnState == TurnState.LEFT:
            adjustOr = 360 - Falcon.TURN_STEP if self.orientation <= 0 else self.orientation - Falcon.TURN_STEP

        elif self.turnState == TurnState.RIGHT:
            adjustOr = Falcon.TURN_STEP if self.orientation >= 360 else self.orientation + Falcon.TURN_STEP

        self.orientation = adjustOr

        # apply thrust if thrusting
        THRUST = 0.85
        MAX_VELOCITY = 40

        # apply some thrust vectors using trig.
        if self.thrusting:
            vectorX = math.cos(math.radians(self.orientation)) * THRUST
            vectorY = math.sin(math.radians(self.orientation)) * THRUST

            # Absolute velocity is the hypotenuse of deltaX and deltaY
            absVelocity = int(
                math.sqrt(math.pow(self.deltaX + vectorX, 2) + math.pow(self.deltaY + vectorY, 2)))

            # only accelerate (or adjust radius) if we are below the maximum absVelocity.
            if absVelocity < MAX_VELOCITY:
                # accelerate
                self.deltaX = self.deltaX + vectorX
                self.deltaY = self.deltaY + vectorY
                self.radius = int(Falcon.MIN_RADIUS + absVelocity / 3.0)
                self.maxSpeedAttained = False
            else:
                self.maxSpeedAttained = True

    def draw(self, imgOff):


        imageState = None
        if self.invisible > 0:
            imageState = ImageState.FALCON_INVISIBLE
        elif self.shield > 0:
            imageState = ImageState.FALCON_PRO_THR if self.thrusting else ImageState.FALCON_PRO
        else:
            imageState = ImageState.FALCON_THR if self.thrusting else ImageState.FALCON

        self.renderRaster(imgOff, self.rasterMap[imageState])
        # draw vector shield on top of raster
        if self.shield > 0 and imageState != ImageState.FALCON_INVISIBLE:
            self.drawShield(ImageDraw.Draw(imgOff))

        if (self.nukeMeter > 0):  self.drawNukeHalo(ImageDraw.Draw(imgOff))

    def drawShield(self, g):
        g.ellipse((self.getCenter().x - self.getRadius(), self.getCenter().y - self.getRadius(),
                   self.getCenter().x + self.getRadius(), self.getCenter().y + self.getRadius())
                  , outline=Color.CYAN)
    def drawNukeHalo(self, g):
        if (self.invisible > 0): return
        g.ellipse((self.getCenter().x - self.getRadius()+10, self.getCenter().y - self.getRadius()+10,
                   self.getCenter().x + self.getRadius()-10, self.getCenter().y + self.getRadius()-10)
                  , outline=Color.YELLOW)

    def removeFromGame(self, list):
        # The falcon is never actually removed from the game-space; instead we decrement numFalcons
        # only execute the decrementFalconNumAndSpawn() method if shield is down.
        if (self.shield == 0):
            self.decrementFalconNumAndSpawn()

    # this method is called when a falcon dies. It allows you to re-initialize the falcon settings without
    # removing him from the movFriends list. Therefore, falcon is never null, which is a good thing.
    def decrementFalconNumAndSpawn(self):
        # import locally to avoid circular import
        from mvc.controller.CommandCenter import CommandCenter
        from mvc.controller.Sound import Sound
        CommandCenter.getInstance().numFalcons -= 1
        if CommandCenter.getInstance().isGameOver(): return
        Sound.playSound( "shipspawn.wav")
        self.shield = INITIAL_SPAWN_TIME
        self.invisible = INITIAL_SPAWN_TIME / 4
        self.center = Point(DIM.width / 2, DIM.height / 2)
        self.orientation = random.randint(
            0, int(360 / Falcon.TURN_STEP)) * Falcon.TURN_STEP
        self.deltaX = 0
        self.deltaY = 0
        self.radius = Falcon.MIN_RADIUS
        self.maxSpeedAttained = False
        self.nukeMeter = 0
