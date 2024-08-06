import os

from pythonic.mvc.controller.CommandCenter import CommandCenter
from pythonic.mvc.controller.GameOp import GameOp
from pythonic.mvc.controller.Sound import Sound
from pythonic.mvc.model.Brick import Brick
from pythonic.mvc.model.Floater import Floater
from pythonic.mvc.model.prime.Color import Color
from pythonic.mvc.model.prime.Constants import DIM
from pythonic.mvc.model.prime.Point import Point


class NewWallFloater(Floater):

    def __init__(self):
        super().__init__()
        self.color = Color.from_RGB(186, 0, 22)
        self.expiry = 230



    def removeFromGame(self, list):
        super().removeFromGame(list)
        # if expiry > 0, then this remove was the result of a collision w/Falcon, and not natural mortality.
        if (self.expiry > 0):
            self.buildWall()
            Sound.playSound( "insect.wav")


    def buildWall(self):
        BRICK_SIZE = int(DIM.width / 30)
        ROWS = 2
        COLS = 20
        X_OFFSET = int(BRICK_SIZE * 6)
        Y_OFFSET = 48

        for nCol in range(0, COLS):
            for nRow in range(0, ROWS):
                CommandCenter.getInstance().opsQueue.enqueue(
                    Brick(Point(int(nCol * BRICK_SIZE + X_OFFSET), int(nRow * BRICK_SIZE + Y_OFFSET)), BRICK_SIZE),
                    GameOp.Action.ADD)
