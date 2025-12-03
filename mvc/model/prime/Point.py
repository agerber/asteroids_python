from dataclasses import dataclass
import math



@dataclass
class Point:

    x: int
    y: int

    def distance(self, other):
        p1x, p2x = self.x, other.x
        p1y, p2y = self.y, other.y
        dist = math.sqrt(math.pow(p1x - p2x, 2) + math.pow(p1y - p2y, 2))
        return dist

    def clone(self):
        # Create and return a new instance of Point with the same x and y values; effectively a clone
        return Point(self.x, self.y)