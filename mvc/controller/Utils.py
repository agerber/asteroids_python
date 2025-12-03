from typing import List
import math

from mvc.model.prime.Point import Point
from mvc.model.prime.PolarPoint import PolarPoint
from functional import seq
from PIL import Image


class Utils:

    @staticmethod
    def cartesiansToPolar(pntCartesians: List[Point]) -> List[PolarPoint]:
        hypotenuseOfPoint = lambda pnt: math.sqrt(pnt.x ** 2 + pnt.y ** 2)
        largestHyp = max(map(hypotenuseOfPoint, pntCartesians), default=0.0)

        cart2polarTransform = lambda pnt, dbl: PolarPoint(
            hypotenuseOfPoint(pnt) / dbl,
            math.degrees(math.atan2(pnt.y, pnt.x)) * math.pi / 180
        )

        return seq(pntCartesians) \
            .map(lambda pnt: cart2polarTransform(pnt, largestHyp)) \
            .list()

    @staticmethod
    def transparent(img) -> Image:
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        transparent_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
        # Paste the original image onto the transparent image
        transparent_img.paste(img, (0, 0), img)
        return transparent_img
