from enum import Enum
from abc import ABC, abstractmethod

from pythonic.mvc.model.prime.Point import Point


class Movable(ABC):
    alive = True

    class Team(Enum):
        FRIEND = 0
        FOE = 1
        FLOATER = 2
        DEBRIS = 3

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def draw(self, imgOff):
        pass

    @abstractmethod
    def getRadius(self) -> int:
        pass

    @abstractmethod
    def getTeam(self) -> Team:
        pass

    @abstractmethod
    def getCenter(self) -> Point:
        pass

    @abstractmethod
    def add(self, *list):
        pass


    @abstractmethod
    def remove(self, *list):
        pass


