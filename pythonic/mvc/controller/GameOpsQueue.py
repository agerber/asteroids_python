from threading import Lock
from pythonic.mvc.model.Movable import Movable
from pythonic.mvc.controller.GameOp import GameOp
from pythonic.mvc.model.prime.LinkedList import LinkedList


class GameOpsQueue:

    def __init__(self):
        super().__init__()
        # this linkedList is thread safe
        self.llist = LinkedList()

    def enqueue(self, mov: Movable, action: GameOp.Action):
        self.llist.enqueue(GameOp(mov, action))

    def dequeue(self) -> GameOp:
        return self.llist.dequeue()

    def __len__(self):
        return self.llist.count
