import os
import random
from enum import Enum


from pythonic.mvc.model.Falcon import Falcon
from pythonic.mvc.controller.GameOpsQueue import GameOpsQueue
from pythonic.mvc.controller.GameOp import GameOp
from pythonic.mvc.model.Radar import MiniMap
from pythonic.mvc.model.Star import Star
from pythonic.mvc.model.prime.Dimension import Dimension
from pythonic.mvc.model.prime.LinkedList import LinkedList
from pythonic.mvc.model.prime.Point import Point
from pythonic.mvc.model.prime.Constants import DIM

from concurrent.futures import ThreadPoolExecutor
import sys


class Universe(Enum):
    FREE_FLY = 0,
    CENTER = 1,
    BIG = 2,
    HORIZONTAL = 3,
    VERTICAL = 4,
    DARK = 5


class CommandCenter:
    __instance = None

    # the following code ensures that you can only call the constructor ONCE
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(CommandCenter, cls).__new__(cls)
            return cls.__instance
        raise Exception(" one instance of CommandCenter is already created ")

    def __init__(self):

        self.numFalcons = 0
        self.level = 0
        self.score = 0
        self.paused = False
        self.muted = True
        self.frame = 0
        self.radar = False

        base_path = os.path.sep.join(os.getcwd().split(os.path.sep)[:-2])
        self.snd = os.path.join(base_path, "resources", "sounds") + os.path.sep
        self.img = os.path.join(base_path, "resources", "imgs") + os.path.sep

        self.falcon = Falcon()
        self.minimap = MiniMap()

        # TODO The following LinkedList<Movable> are examples of the Composite design pattern which is used to allow
        # compositions of objects to be treated uniformly. Here are the elements of the Composite design pattern:
        #
        # Component: Movable serves as the component interface. It defines common methods (move(), draw(Graphics g), etc.)
        # that all concrete implementing classes must provide.
        #
        # Leaf: Concrete classes that implement Movable (e.g., Bullet, Asteroid) are the leaf nodes. They implement the
        # Movable interface and provide specific behavior.
        #
        # Composite: The LinkedLists below that aggregate Movable objects (e.g., movFriends, movFoes) act as
        # composites. They manage collections of Movable objects and provide a way to iterate over and operate on them as a
        # group.

        self.movDebris = LinkedList()
        self.movFriends = LinkedList()
        self.movFoes = LinkedList()
        self.movFloaters = LinkedList()

        self.falconCentered = True
        self.opsQueue = GameOpsQueue()
        self.diffX = 0
        self.diffY = 0
        self.universe = Universe.FREE_FLY
        self.miniDimHash = {}

    # TODO This is an example of the Singleton design pattern. The Singleton ensures that a class has one (and only
    # one) instance on the heap and provides a global point of access at instance. This is useful when you need to
    # coordinate actions among objects in your system or manage state. CommandCenter manages the state of the game.

    @staticmethod
    def getInstance():
        # this is now a singleton
        if (CommandCenter.__instance is None):
            CommandCenter.__instance = CommandCenter()

        return CommandCenter.__instance

    def initGame(self):
        self.clearAll()
        self.level = 0
        self.score = 0
        self.paused = False
        self.radar = True
        self.numFalcons = 4
        self.falcon.decrementFalconNumAndSpawn()
        self.opsQueue.enqueue(self.falcon, GameOp.Action.ADD)
        self.opsQueue.enqueue(self.minimap, GameOp.Action.ADD)
        self.miniDimHash[Universe.FREE_FLY] = Dimension(1, 1)
        self.miniDimHash[Universe.CENTER] = Dimension(1,1)
        self.miniDimHash[Universe.BIG] = Dimension(3,3)
        self.miniDimHash[Universe.HORIZONTAL] = Dimension(3,1)
        self.miniDimHash[Universe.VERTICAL] = Dimension(1, 3)
        self.miniDimHash[Universe.DARK] = Dimension(4, 4)
        self.createStarField()

    def clearAll(self):
        self.movDebris.clear()
        self.movFriends.clear()
        self.movFoes.clear()
        self.movFloaters.clear()

    def createStarField(self):
        count = 100
        while (count > 0):
            self.opsQueue.enqueue(Star(), GameOp.Action.ADD)
            count -= 1

    def incrementFrame(self):
        # use of ternary expression to simplify the logic to one line
        self.frame = self.frame + 1 if self.frame < sys.maxsize else 0

    def isGameOver(self) -> bool:  # //if the number of falcons is zero, then game over
        return self.numFalcons < 1

    # def getUniScaler(self):
    #     localScaler=1
    #     if self.universe == Universe.BIG:
    #         localScaler = BIG_UNIVERSAL_SCALER
    #     else:
    #         localScaler = 1
    #     return localScaler

    def cycleUniverse(self):
        if self.universe == Universe.FREE_FLY:
            self.universe = Universe.CENTER
        elif self.universe == Universe.CENTER:
            self.universe = Universe.BIG
        elif self.universe == Universe.BIG:
            self.universe = Universe.HORIZONTAL
        elif self.universe == Universe.HORIZONTAL:
            self.universe = Universe.VERTICAL
        elif self.universe == Universe.VERTICAL:
            self.universe = Universe.DARK
        elif self.universe == Universe.DARK:
            self.universe = Universe.FREE_FLY

    def isFalconPositionFixed(self):
        return CommandCenter.getInstance().universe != Universe.FREE_FLY

    def getUniDim(self):
        return self.miniDimHash[self.universe]
# if __name__ == "__main__":
#     comand1 = CommandCenter()
#     #print(comand1.getInstance().__dict__)
#     comand2 = CommandCenter()
#
#     print(comand1 is comand2)
