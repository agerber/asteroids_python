import os
import random

from pythonic.mvc.model.Falcon import Falcon
from pythonic.mvc.controller.GameOpsQueue import GameOpsQueue
from pythonic.mvc.controller.GameOp import GameOp
from pythonic.mvc.model.Star import Star
from pythonic.mvc.model.prime.LinkedList import LinkedList
from concurrent.futures import ThreadPoolExecutor
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
        self.paused = False
        self.muted = True
        self.frame = 0
        self.snd = "/".join(os.getcwd().split("/")[:-2]) + "/resources/sounds/"
        self.img = "/".join(os.getcwd().split("/")[:-2]) + "/resources/imgs/"
        self.falcon = Falcon()

        self.movDebris = LinkedList()
        self.movFriends = LinkedList()
        self.movFoes = LinkedList()
        self.movFloaters = LinkedList()

        self.opsQueue = GameOpsQueue()

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
        self.numFalcons = 4
        self.falcon.decrementFalconNumAndSpawn()
        self.opsQueue.enqueue(self.falcon, GameOp.Action.ADD)
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

# if __name__ == "__main__":
#     comand1 = CommandCenter()
#     #print(comand1.getInstance().__dict__)
#     comand2 = CommandCenter()
#
#     print(comand1 is comand2)
