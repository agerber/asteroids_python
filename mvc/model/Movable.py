from enum import Enum
from abc import ABC, abstractmethod

from mvc.model.prime.Point import Point

# TODO This ABC is an example of the Facade design pattern which provides a simplified
# interface to a complex subsystem or set of classes. It hides the complexity by offering a more straightforward and unified API.
# The goal is to make subsystems easier to use by providing a higher-level interface that clients can interact with.

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
    def addToGame(self, list):
        pass


    @abstractmethod
    def removeFromGame(self, list):
        pass


