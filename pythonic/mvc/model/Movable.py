from enum import Enum
from abc import ABC, abstractmethod

from pythonic.mvc.model.prime.Point import Point


class Movable(ABC):

    class Team(Enum):
        FRIEND = 0
        FOE = 1
        FLOATER = 2
        DEBRIS = 3

    # for movables to move and draw themselves. See GamePanel class.
    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def draw(self, imgOff):
        pass


    # for collision detection
    @abstractmethod
    def getRadius(self) -> int:
        pass

    @abstractmethod
    def getTeam(self) -> Team:
        pass

    @abstractmethod
    def getCenter(self) -> Point:
        pass

    # lifecycle callbacks when a movable object is added or removed from the game-space. This is your opportunity
    # to add sounds or other side effects.
    @abstractmethod
    def start(self, list):
        pass


    @abstractmethod
    def finish(self, list):
        pass


