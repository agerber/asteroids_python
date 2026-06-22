from typing import Tuple

from PIL import Image, ImageFont

from mvc.controller.CommandCenter import CommandCenter
from mvc.controller.Utils import Utils
from mvc.model.prime.Constants import DIM
from mvc.model.prime.PolarPoint import PolarPoint
from mvc.model.prime.Point import Point
from mvc.view.GameFrame import GameFrame
from mvc.view.Graphics import Graphics
from mvc.model.prime.Color import Color
from functional import seq
import math
import os


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

        self.gameFrame.setup(dim.width, dim.height, "Game Base")

    def drawFalconStatus(self, g):
        OFFSET_LEFT = 220

        universe_str = CommandCenter.getInstance().universe.name
        formatted_uni = universe_str.replace('_', ' ')
        levelText = f"Level: [{CommandCenter.getInstance().level}] {formatted_uni}"

        g.setColor(Color.WHITE)
        g.setFont(self.fontNormal)
        g.drawString(levelText, DIM.width - OFFSET_LEFT, 10)
        formatted_score = "{:,}".format(CommandCenter.getInstance().score)
        g.drawString(f"Score: {formatted_score}", DIM.width - OFFSET_LEFT, 30)


        statusArray = []

        if CommandCenter.getInstance().falcon.showLevel > 0:
            statusArray.append(levelText)

        if CommandCenter.getInstance().falcon.nukeMeter > 0:
            statusArray.append("Press 'F' for Nuke")

        if CommandCenter.getInstance().falcon.maxSpeedAttained:
            statusArray.append("WARNING - SLOW DOWN")

        # draw the statusArray strings to middle of screen. unpack the list to satisfy the var-args definition.
        if statusArray:
            self.displayTextOnScreen(g, *statusArray)

        # draw PYTHON VERSION and the frame number to bottom left screen
        g.drawString(f"FRAME[PYTHON]:{CommandCenter.getInstance().frame}",
                     self.fontWidth + 10,
                     DIM.height - (self.fontHeight + 22))

    # mirrors Java's GamePanel.update(Graphics g): creates an off-screen
    # double-buffer, draws into its Graphics context, then blits the
    # finished image to the on-screen tk Label in one swoop to avoid
    # flickering.
    def update(self):

        imgOff = Image.new("RGB", (DIM.width, DIM.height), Color.BLACK)
        g = Graphics(imgOff)

        CommandCenter.getInstance().incrementFrame()

        if CommandCenter.getInstance().isGameOver():
            self.displayTextOnScreen(g,
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
            self.displayTextOnScreen(g, "Game Paused")
        else:
            self.moveDrawMovables(g,
                                  CommandCenter.getInstance().movDebris,
                                  CommandCenter.getInstance().movFloaters,
                                  CommandCenter.getInstance().movFoes,
                                  CommandCenter.getInstance().movFriends)

            self.drawMeters(g)
            self.drawFalconStatus(g)
            self.drawNumberShipsRemaining(g)

        # blit the finished off-screen image onto the screen in one swoop.
        self.gameFrame.blit(g.image)

    def drawNumberShipsRemaining(self, g):
        numFalcons = CommandCenter.getInstance().numFalcons
        while numFalcons > 1:
            self.drawOneShip(g, numFalcons)
            numFalcons -= 1

    def drawOneShip(self, g, offSet):

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

        g.setColor(Color.ORANGE)
        g.drawPolygon(
            seq(polars)\
                .map(rotatePolarByOrientation)\
                .map(polarToCartesian)\
                .map(adjustForLocation)\
                .map(lambda point: (point.x, point.y))\
                .list())


    def drawOneMeter(self, g, color: Tuple, offSet: int, percent: int):
        xValBase = DIM.width - (100 + 120 * offSet)
        yValBase = DIM.height - 20

        g.setColor(color)
        g.fillRect(xValBase, yValBase, percent, 10)
        g.setColor(Color.GREY)
        g.drawRect(xValBase, yValBase, 100, 10)

    def drawMeters(self, g):

        sheildValue = CommandCenter.getInstance().falcon.shield // 2
        nukeValue = CommandCenter.getInstance().falcon.nukeMeter // 6
        self.drawOneMeter(g, color=Color.CYAN, offSet=1, percent=sheildValue)
        self.drawOneMeter(g, color=Color.YELLOW, offSet=2, percent=nukeValue)

    def moveDrawMovables(self, g, *teams):
        for team in teams:
            for mov in team:
                mov.move()
                mov.draw(g)

    # var-args as lines
    def displayTextOnScreen(self, g, *lines):
        g.setColor(Color.WHITE)
        g.setFont(self.fontNormal)
        yVal = 0
        for line in lines:
            g.drawString(line, DIM.width // 2 - len(line) * 2.5 - 10, 200 + yVal)
            yVal += 40
