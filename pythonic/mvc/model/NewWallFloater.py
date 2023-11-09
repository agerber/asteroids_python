from pythonic.mvc.controller.CommandCenter import CommandCenter
from pythonic.mvc.controller.GameOp import GameOp
from pythonic.mvc.model.Brick import Brick
from pythonic.mvc.model.Floater import Floater
from pythonic.mvc.model.prime.Color import Color
from pythonic.mvc.model.prime.Point import Point


class NewWallFloater(Floater):

    def __init__(self):
        super().__init__()

        self.color = Color.from_RGB(186, 0, 22)
        self.expiry = 230
    def add(self, list):
        list.append(self)


    def remove(self, list):
        self.alive = False
        self.buildWall()


    def buildWall(self):
        BRICK_SIZE = int(DIM.width / 30)
        ROWS = 2
        COLS = 20
        X_OFFSET = int(BRICK_SIZE * 5)
        Y_OFFSET = 50

        for nCol in range(0, COLS):
            for nRow in range(0, ROWS):
                CommandCenter.getInstance().opsQueue.enqueue(
                    Brick(Point(int(nCol * BRICK_SIZE + X_OFFSET), int(nRow * BRICK_SIZE + Y_OFFSET)), BRICK_SIZE),
                    GameOp.Action.ADD)
