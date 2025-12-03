from enum import Enum
from dataclasses import dataclass

from mvc.model.Movable import Movable

@dataclass
class GameOp:

    class Action(Enum):
        ADD = 1
        REMOVE = 2

    movable: Movable
    action: Action

