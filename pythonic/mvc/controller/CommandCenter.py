import os
import random


from pythonic.mvc.model.Falcon import Falcon
from pythonic.mvc.controller.GameOpsQueue import GameOpsQueue
from pythonic.mvc.controller.GameOp import GameOp
from pythonic.mvc.model.Star import Star
from pythonic.mvc.model.prime.LinkedList import LinkedList
from pythonic.mvc.model.prime.Point import Point
from pythonic.mvc.model.prime.Stack import Stack
from functional import seq
from pythonic.mvc.model.prime.Constants import DIM, MAX_SHIELD, INITIAL_SPAWN_TIME
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
        self.muted = False
        self.frame = 0
        self.falcon = Falcon()
        self.cwd = "/".join(os.getcwd().split("/")[:-2]) + "/resources/sounds/"

        self.movDebris = LinkedList()
        self.movFriends = LinkedList()
        self.movFoes = LinkedList()
        self.movFloaters = LinkedList()

        self.opsQueue = GameOpsQueue()
        self.soundExecutor = ThreadPoolExecutor(max_workers=5)

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

    def purgeDeadMovables(self):

        isAlive = lambda mov: mov.alive

        self.movDebris = seq(self.movDebris).filter(isAlive).list()
        self.movFriends = seq(self.movFriends).filter(isAlive).list()
        self.movFoes = seq(self.movFoes).filter(isAlive).list()
        self.movFloaters = seq(self.movFloaters).filter(isAlive).list()


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
