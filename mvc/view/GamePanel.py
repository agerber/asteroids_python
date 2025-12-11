from typing import Tuple

from PIL import ImageFont, ImageTk, ImageDraw

from mvc.controller.CommandCenter import CommandCenter
from mvc.controller.Utils import Utils
from mvc.model.prime.Constants import DIM
from mvc.model.prime.PolarPoint import PolarPoint
from mvc.model.prime.Point import Point
from mvc.view.GameFrame import GameFrame
from mvc.model.prime.Color import Color
from functional import seq
import math
import os
from PIL import ImageFont


class GamePanel:
    def __init__(self, dim):

        base_dir = os.path.dirname(os.path.abspath(__file__))
        FONT_PATH = os.path.join(base_dir, "..", "..", "resources", "font", "OpenSans-Bold.ttf")
        self.fontNormal = ImageFont.truetype(FONT_PATH, 14)
        self.fontBig = ImageFont.truetype(FONT_PATH, 22)

        self.fontWidth = 0
        self.fontHeight = 0

        self.pntShipsRemaining = None
        self.gameFrame = GameFrame()

        self.pntShipsRemaining = []
        self.pntShipsRemaining.append(Point(0, 9))
        self.pntShipsRemaining.append(Point(-1, 6))
        self.pntShipsRemaining.append(Point(-1, 3))
        self.pntShipsRemaining.append(Point(-4, 1))
        self.pntShipsRemaining.append(Point(4, 1))
        self.pntShipsRemaining.append(Point(-4, 1))
        self.pntShipsRemaining.append(Point(-4, -2))
        self.pntShipsRemaining.append(Point(-1, -2))
        self.pntShipsRemaining.append(Point(-1, -9))
        self.pntShipsRemaining.append(Point(-1, -2))
        self.pntShipsRemaining.append(Point(-4, -2))
        self.pntShipsRemaining.append(Point(-10, -8))
        self.pntShipsRemaining.append(Point(-5, -9))
        self.pntShipsRemaining.append(Point(-7, -11))
        self.pntShipsRemaining.append(Point(-4, -11))
        self.pntShipsRemaining.append(Point(-2, -9))
        self.pntShipsRemaining.append(Point(-2, -10))
        self.pntShipsRemaining.append(Point(-1, -10))
        self.pntShipsRemaining.append(Point(-1, -9))
        self.pntShipsRemaining.append(Point(1, -9))
        self.pntShipsRemaining.append(Point(1, -10))
        self.pntShipsRemaining.append(Point(2, -10))
        self.pntShipsRemaining.append(Point(2, -9))
        self.pntShipsRemaining.append(Point(4, -11))
        self.pntShipsRemaining.append(Point(7, -11))
        self.pntShipsRemaining.append(Point(5, -9))
        self.pntShipsRemaining.append(Point(10, -8))
        self.pntShipsRemaining.append(Point(4, -2))
        self.pntShipsRemaining.append(Point(1, -2))
        self.pntShipsRemaining.append(Point(1, -9))
        self.pntShipsRemaining.append(Point(1, -2))
        self.pntShipsRemaining.append(Point(4, -2))
        self.pntShipsRemaining.append(Point(4, 1))
        self.pntShipsRemaining.append(Point(1, 3))
        self.pntShipsRemaining.append(Point(1, 6))
        self.pntShipsRemaining.append(Point(0, 9))

        self.gameFrame.geometry(
            str(dim.width) + 'x' + str(dim.height))  # instead of setsize
        self.gameFrame.title("Game Base")
        self.gameFrame.resizable = False

    def drawFalconStatus(self, imgOff):
        g = ImageDraw.Draw(imgOff)
        OFFSET_LEFT = 220

        universe_str = CommandCenter.getInstance().universe.name
        formatted_uni = universe_str.replace('_', ' ')
        levelText = f"Level: [{CommandCenter.getInstance().level}] {formatted_uni}"

        g.text((DIM.width - OFFSET_LEFT, 10 ), levelText, font=self.fontNormal,
               fill=Color.WHITE)  # white color
        formatted_score = "{:,}".format(CommandCenter.getInstance().score)
        g.text((DIM.width - OFFSET_LEFT, 30), f"Score: {formatted_score}",
               font=self.fontNormal,
               fill=Color.WHITE)  # white color


        statusArray = []

        if CommandCenter.getInstance().falcon.showLevel > 0:
            statusArray.append(levelText)

        if CommandCenter.getInstance().falcon.nukeMeter > 0:
            statusArray.append("Press 'F' for Nuke")

        if CommandCenter.getInstance().falcon.maxSpeedAttained:
            statusArray.append("WARNING - SLOW DOWN")

        # draw the statusArray strings to middle of screen. unpack the list to satisfy the var-args definition.
        if statusArray:
            self.displayTextOnScreen(imgOff, *statusArray)

        # draw PYTHON VERSION and the frame number to bottom left screen
        g.text((self.fontWidth + 10, DIM.height - (self.fontHeight + 22)),
               f"FRAME[PYTHON]:{CommandCenter.getInstance().frame}",
               font=self.fontNormal,
               fill=Color.WHITE)  # white color

    def update(self, imgOff):

        CommandCenter.getInstance().incrementFrame()

        if CommandCenter.getInstance().isGameOver():
            self.displayTextOnScreen(imgOff,
                                     "GAME OVER",
                                     "use the arrow keys to turn and thrust",
                                     "use the space bar to fire",
                                     "'S' to Start",
                                     "'P' to Pause",
                                     "'Q' to Quit",
                                     "'M' to toggle music",
                                     "'A' to toggle radar"
                                     )

        elif CommandCenter.getInstance().isPaused:
            self.displayTextOnScreen(imgOff, "Game Paused")
        else:
            self.moveDrawMovables(imgOff,
                                  CommandCenter.getInstance().movDebris,
                                  CommandCenter.getInstance().movFloaters,
                                  CommandCenter.getInstance().movFoes,
                                  CommandCenter.getInstance().movFriends)

            self.drawMeters(imgOff)
            self.drawFalconStatus(imgOff)
            self.drawNumberShipsRemaining(imgOff)

        # in one fell-swoop, we copy the off-screen-image to a new on-screen-image and show it for ~40ms. This is the
        # double-buffering. If you attempt to draw directly on the gameFrame, you will see flickering.
        imgOnScreen = ImageTk.PhotoImage(imgOff)
        self.gameFrame.contentFrame.configure(image=imgOnScreen)
        self.gameFrame.contentFrame.image = imgOnScreen
        self.gameFrame.contentFrame.pack()

    def drawNumberShipsRemaining(self, imgOff):
        from mvc.controller.CommandCenter import CommandCenter
        numFalcons = CommandCenter.getInstance().numFalcons
        while numFalcons > 1:
            self.drawOneShip(imgOff, numFalcons)
            numFalcons -= 1

    def drawOneShip(self, imgOff, offSet):

        g = ImageDraw.Draw(imgOff)  # get graphics context from the off-screen-image

        # rotate the ship 90 degrees
        DEGREES_90 = -90
        RADIUS = 15
        X_POS = DIM.width - (27 * offSet)
        Y_POS = DIM.height - 20

        # the reason we convert to polar-points is that it's much easier to rotate polar-points.
        polars = Utils.cartesiansToPolar(self.pntShipsRemaining)

        # 2: rotate raw polars given the orientation of the sprite.
        rotatePolarByOrientation = lambda pp: PolarPoint(
            pp.r,
            pp.theta + math.radians(DEGREES_90)
        )

        # 3: convert the rotated polars back to cartesians
        polarToCartesian = lambda pp: Point(
            int(pp.r * RADIUS * math.sin(pp.theta)),
            int(pp.r * RADIUS * math.cos(pp.theta))
        )

        # 4: adjust the cartesians for the location (center-point) of the sprite.
        # the reason we subtract the y-value has to do with how python plots the vertical axis for
        # graphics (from top to bottom)
        adjustForLocation = lambda pnt: Point(
            X_POS + pnt.x,
            Y_POS - pnt.y
        )

        # 5: draw the polygon using the List of raw polars from above, applying mapping transforms as required

        g.polygon(
            seq(polars)\
                .map(rotatePolarByOrientation)\
                .map(polarToCartesian)\
                .map(adjustForLocation)\
                .map(lambda point: (point.x, point.y))\
                .list(),
            outline=Color.ORANGE)


    def drawOneMeter(self, imgOff, color: Tuple, offSet: int, percent: int):
        # get the graphics (g) context of the off-screen-image
        g = ImageDraw.Draw(imgOff)

        xValBase = DIM.width - (100 + 120 * offSet)
        yValBase = DIM.height - 10

        upperLeftPoint = (xValBase, yValBase - 10)
        bottomRightFillPoint = ((xValBase + percent), yValBase)
        bottomRightStrokePoint = ((xValBase + 100), yValBase)

        g.rectangle((upperLeftPoint, bottomRightFillPoint), fill=color)
        g.rectangle((upperLeftPoint, bottomRightStrokePoint), outline=Color.GREY)

    def drawMeters(self, imgOff):

        sheildValue = CommandCenter.getInstance().falcon.shield // 2
        nukeValue = CommandCenter.getInstance().falcon.nukeMeter // 6
        self.drawOneMeter(imgOff, color=Color.CYAN, offSet=1, percent=sheildValue)
        self.drawOneMeter(imgOff, color=Color.YELLOW, offSet=2, percent=nukeValue)

    def moveDrawMovables(self, imgOff, *teams):
        for team in teams:
            for mov in team:
                mov.move()
                mov.draw(imgOff)

    # var-args as lines
    def displayTextOnScreen(self, imgOff, *lines):
        yVal = 0
        for line in lines:
            ImageDraw.Draw(imgOff).text((DIM.width // 2 - len(line) * 2.5 - 10, 200 + yVal), line, font=self.fontNormal,
                                        fill=Color.WHITE, align="center")
            yVal += 40
