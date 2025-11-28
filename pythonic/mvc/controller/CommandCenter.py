import os
import random
from enum import Enum
from typing import Optional

from pythonic.mvc.model.Falcon import Falcon
from pythonic.mvc.controller.GameOpsQueue import GameOpsQueue
from pythonic.mvc.controller.GameOp import GameOp
from pythonic.mvc.model.Radar import Radar
from pythonic.mvc.model.Star import Star
from pythonic.mvc.model.prime.Dimension import Dimension
from pythonic.mvc.model.prime.LinkedList import LinkedList

import sys


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
        self.isPaused = False
        self.isMuted = True
        self.frame = 0
        self.isRadar = False
        self.universes = list(Universe)


        base_path = os.path.sep.join(os.getcwd().split(os.path.sep)[:-2])
        self.snd = os.path.join(base_path, "resources", "sounds") + os.path.sep
        self.img = os.path.join(base_path, "resources", "imgs") + os.path.sep

        self.falcon = Falcon()
        self.radar = Radar()

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
        self.isPaused = False
        self.isRadar = True
        self.numFalcons = 4

        self.createStarField()
        self.opsQueue.enqueue(self.falcon, GameOp.Action.ADD)
        self.opsQueue.enqueue(self.radar, GameOp.Action.ADD)

        self.falcon.decrementFalconNumAndSpawn()

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

    def isFalconPositionFixed(self):
        return CommandCenter.getInstance().universe != Universe.FREE_FLY

    def optUni(self) -> Optional["Universe"]:
        if self.level == 0:
            return None
        index = (self.level - 1) % len(self.universes)
        return self.universes[index]

    def getUniDim(self):
        uni = self.optUni()
        return Dimension(1, 1) if uni is None else uni.dimension

    def getUniName(self):
        uni = self.optUni()
        return "" if uni is None else uni.label

class Universe(Enum):
    FREE_FLY   = ("FREE FLY",   Dimension(1, 1))
    CENTER     = ("CENTER",     Dimension(1, 1))
    BIG        = ("BIG",        Dimension(3, 3))
    HORIZONTAL = ("HORIZONTAL", Dimension(3, 1))
    VERTICAL   = ("VERTICAL",   Dimension(1, 3))
    DARK       = ("DARK",       Dimension(4, 4))

    def __init__(self, name, dimension):
        self.label = name            # string name
        self.dimension = dimension    # Dimension object

