import os
import time
import threading
from tkinter import TclError

from pythonic.mvc.model.Movable import Movable
from pythonic.mvc.model.Asteroid import Asteroid
from pythonic.mvc.model.Nuke import Nuke
from pythonic.mvc.model.NukeFloater import NukeFloater
from pythonic.mvc.model.ShieldFloater import ShieldFloater
#from pythonic.mvc.model.prime.Dimension import Dimension
from pythonic.mvc.view.GamePanel import GamePanel
from pythonic.mvc.controller.CommandCenter import CommandCenter, Universe
from pythonic.mvc.model import Falcon
from pythonic.mvc.model.Bullet import Bullet
from pythonic.mvc.controller.GameOp import GameOp
from pythonic.mvc.model.prime.Color import Color
from pythonic.mvc.model.prime.Constants import DIM, SPAWN_SHIELD_FLOATER, SPAWN_NUKE_FLOATER, SPAWN_NEW_WALL_FLOATER, \
    MAX_SHIELD, MAX_NUKE, INITIAL_SPAWN_TIME
from pythonic.mvc.model.prime.Point import Point
from PIL import Image
from Sound import Sound
import sys, gc


# todo: refactor the code so that its in python style, and clean-up
class Game(threading.Thread):
    # ===============================================
    # FIELDS
    # ===============================================

    ANIMATION_DELAY = 40  # milliseconds between frames
    FRAMES_PER_SECOND = 1000 // ANIMATION_DELAY

    # key-codes
    PAUSE = 'p'  # p key
    QUIT = 'q'  # q key
    LEFT = 'Left'  # rotate left; left arrow
    RIGHT = 'Right'  # rotate right; right arrow
    UP = 'Up'  # thrust; up arrow
    START = 's'  # s key
    FIRE = 'space'  # space key
    MUTE = 'm'  # m-key mute
    NUKE = 'f'  # f-key
    RADAR = 'a'

    # for possible future use
    # HYPER = 68 # D key
    # ALIEN = 65 # A key
    # SPECIAL = 70 # fire special weapon;  F key

    # ===============================================
    # ==CONSTRUCTOR
    # ===============================================

    def __init__(self):
        super().__init__()
        #self.DIM = self.setDimFromEnv()
        self.gamePanel = GamePanel(DIM)
        self.gamePanel.gameFrame.bind("<KeyPress>", self.keyPressed)
        self.gamePanel.gameFrame.bind("<KeyRelease>", self.keyReleased)
        self.animationThread = self
        self.animationThread.daemon = True  ## kills thread with main thread
        self.animationThread.start()
        self.main()

    def run(self):
        startTime = time.time() * 1000.0
        while threading.current_thread() == self.animationThread and self.gamePanel.gameFrame.running:
            try:
                # we use a double-buffered off-screen image called imgOff
                imgOff = Image.new(
                    "RGB", (DIM.width, DIM.height), Color.BLACK)
                self.gamePanel.update(imgOff)

                self.checkCollisions()
                self.checkNewLevel()
                self.checkFloaters()
                # this method will execute add() and remove() callbacks on Movable objects
                self.processGameOpsQueue()
                startTime += Game.ANIMATION_DELAY
                time.sleep(
                    max(0.0, round(startTime - time.time() * 1000) / 1000))
            except:
                pass

    def checkCollisions(self):

        # this has an order of growth of O(FRIENDS * FOES)
        for movFriend in CommandCenter.getInstance().movFriends:
            for movFoe in CommandCenter.getInstance().movFoes:
                pntFriendCenter = movFriend.getCenter()
                pntFoeCenter = movFoe.getCenter()
                radFriend = movFriend.getRadius()
                radFoe = movFoe.getRadius()
                if pntFriendCenter.distance(pntFoeCenter) < (radFoe + radFriend):
                    CommandCenter.getInstance().opsQueue.enqueue(movFriend, GameOp.Action.REMOVE)
                    CommandCenter.getInstance().opsQueue.enqueue(movFoe, GameOp.Action.REMOVE)

        pntFalcon = CommandCenter.getInstance().falcon.center
        radFalcon = CommandCenter.getInstance().falcon.getRadius()
        # this has an order of growth of O(FLOATERS)
        for movFloater in CommandCenter.getInstance().movFloaters:
            pntFloaterCenter = movFloater.getCenter()
            radFloater = movFloater.getRadius()
            if (pntFalcon.distance(pntFloaterCenter) < (radFalcon + radFloater)):
                CommandCenter.getInstance().opsQueue.enqueue(movFloater, GameOp.Action.REMOVE)

    def processGameOpsQueue(self):
        # deferred mutation: these operations are done AFTER we have completed our collision detection to avoid
        # mutating the movable linkedlists while iterating them above.
        while len(CommandCenter.getInstance().opsQueue) > 0:
            gameOp = CommandCenter.getInstance().opsQueue.dequeue()
            mov = gameOp.movable
            action = gameOp.action
            list = None

            if mov.getTeam() == Movable.Team.FOE:
                list = CommandCenter.getInstance().movFoes
            elif mov.getTeam() == Movable.Team.FRIEND:
                list = CommandCenter.getInstance().movFriends
            elif mov.getTeam() == Movable.Team.FLOATER:
                list = CommandCenter.getInstance().movFloaters
            else: # mov.getTeam() == Movable.Team.DEBRIS:
                list = CommandCenter.getInstance().movDebris

            # the following block executes the callbacks
            if action == GameOp.Action.ADD:
                mov.addToGame(list)
            else:
                mov.removeFromGame(list)

    def main(self):
        self.gamePanel.gameFrame.mainloop()

    def checkNewLevel(self):

        if not self.isLevelClear(): return

        level = CommandCenter.getInstance().level
        CommandCenter.getInstance().score += 10_000 * level

        # CommandCenter.getInstance().setUniverse(universe)
        ordinal = level % len(Universe)
        key = list(Universe)[ordinal]
        CommandCenter.getInstance().universe = key

        level += 1
        CommandCenter.getInstance().level = level

        #recenter the falcon at level clears
        CommandCenter.getInstance().falcon.center = Point(int(round(DIM.width / 2.0)), int(round(DIM.height / 2.0)))

        self.spawnBigAsteroids(level)
        if (CommandCenter.getInstance().falcon.shield < INITIAL_SPAWN_TIME):
            CommandCenter.getInstance().falcon.shield = INITIAL_SPAWN_TIME

        CommandCenter.getInstance().falcon.showLevel = INITIAL_SPAWN_TIME

    def isLevelClear(self):
        asteroidFree = True
        for movFoe in CommandCenter.getInstance().movFoes:
            if isinstance(movFoe, Asteroid):
                asteroidFree = False
                break
        return asteroidFree

    def spawnBigAsteroids(self, num):
         # num += 10
        while num > 0:
            CommandCenter.getInstance().opsQueue.enqueue(Asteroid(0), GameOp.Action.ADD)
            num -= 1

    def checkFloaters(self):
        self.spawnShieldFloater()
        # self.spawnNewWallFloater()
        self.spawnNukeFloater()

    def spawnNukeFloater(self):
        if CommandCenter.getInstance().frame % SPAWN_NUKE_FLOATER == 0:
            CommandCenter.getInstance().opsQueue.enqueue(NukeFloater(), GameOp.Action.ADD)

    def spawnShieldFloater(self):
        if CommandCenter.getInstance().frame % SPAWN_SHIELD_FLOATER == 0:
            CommandCenter.getInstance().opsQueue.enqueue(ShieldFloater(), GameOp.Action.ADD)

    def stopLoopingSounds(self, *sounds):
        [sound.stop() for sound in sounds if hasattr(sound, "stop")]

    def keyPressed(self, event):
        falcon = CommandCenter.getInstance().falcon
        keyCode = event.keysym
        # print(keyCode)
        if keyCode == Game.START and CommandCenter.getInstance().isGameOver():
            CommandCenter.getInstance().initGame()
            return
        if keyCode == Game.PAUSE:
            CommandCenter.getInstance().isPaused = not CommandCenter.getInstance().isPaused
        elif keyCode == Game.QUIT:
            sys.exit(0)
        elif keyCode == Game.UP:
            falcon.thrusting = True
            Sound.playLoopSound("whitenoise_loop.wav")
        elif keyCode == Game.LEFT:
            falcon.turnState = Falcon.TurnState.LEFT
        elif keyCode == Game.RIGHT:
            falcon.turnState = Falcon.TurnState.RIGHT

    def keyReleased(self, event):
        falcon = CommandCenter.getInstance().falcon
        keyCode = event.keysym
        if keyCode == Game.FIRE:
            CommandCenter.getInstance().opsQueue.enqueue(Bullet(falcon), GameOp.Action.ADD)
        elif keyCode == Game.NUKE:
            CommandCenter.getInstance().opsQueue.enqueue(Nuke(falcon), GameOp.Action.ADD)
        elif keyCode == Game.RIGHT or keyCode == Game.LEFT:
            falcon.turnState = Falcon.TurnState.IDLE
        elif keyCode == Game.UP:
            falcon.thrusting = False
            Sound.stopLoopSound("whitenoise_loop.wav")
        elif keyCode == Game.MUTE:
            CommandCenter.getInstance().getInstance().isMuted = not CommandCenter.getInstance().isMuted
            if CommandCenter.getInstance().getInstance().isMuted:
                Sound.stopLoopSound("dr_loop.wav")
            else:
                Sound.playLoopSound("dr_loop.wav")
        elif keyCode == Game.RADAR:
            CommandCenter.getInstance().isRadar = not CommandCenter.getInstance().isRadar

if __name__ == "__main__":
    game = Game()
