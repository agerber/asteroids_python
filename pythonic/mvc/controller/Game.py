import os
import time
import threading
from pythonic.mvc.model.Movable import Movable
from pythonic.mvc.model.NewWallFloater import NewWallFloater
from pythonic.mvc.model.Nuke import Nuke
from pythonic.mvc.model.NukeFloater import NukeFloater
from pythonic.mvc.model.ShieldFloater import ShieldFloater
from pythonic.mvc.view.GamePanel import GamePanel
from pythonic.mvc.controller.CommandCenter import CommandCenter
from pythonic.mvc.model import Falcon, Brick
from pythonic.mvc.model.Bullet import Bullet
from pythonic.mvc.model.Brick import Brick
from functional import seq
import gc

from pythonic.mvc.controller.Sound import Sound
from pythonic.mvc.model.Asteroid import Asteroid
from pythonic.mvc.controller.GameOp import GameOp
from pythonic.mvc.model.prime.Color import Color
from pythonic.mvc.model.prime.Point import Point
from pythonic.mvc.model.WhiteCloudDebris import WhiteCloudDebris
from pythonic.mvc.model.prime.Constants import DIM, SPAWN_SHIELD_FLOATER, SPAWN_NUKE_FLOATER, SPAWN_NEW_WALL_FLOATER, MAX_SHIELD,MAX_NUKE, INITIAL_SPAWN_TIME
from PIL import Image
import sys



#todo: refactor the code so that its in python style, and clean-up
class Game (threading.Thread):
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
    NUKE = 'n'  # m-key mute

    # for possible future use
    # HYPER = 68 # D key
    # ALIEN = 65 # A key
    # SPECIAL = 70 # fire special weapon;  F key

    # ===============================================
    # ==CONSTRUCTOR
    # ===============================================

    def __init__(self):
        super().__init__()
        self.gamePanel = GamePanel(DIM)
        self.gamePanel.gameFrame.bind("<KeyPress>", self.keyPressed)
        self.gamePanel.gameFrame.bind("<KeyRelease>", self.keyReleased)
        self.cwd = "/".join(os.getcwd().split("/")[:-2])+"/resources/sounds/"
        # self.soundThrust = Sound.clipForLoopFactory(self.cwd+"whitenoise.wav")
        # self.soundBackground = Sound.clipForLoopFactory(self.cwd+"music-background.wav")
        self.animationThread = self
        self.animationThread.daemon = True ## kills thread with main thread
        self.animationThread.start()
        self.main()

    def run(self):
        startTime = time.time()*1000.0
        while threading.current_thread() == self.animationThread:
            # we use a double-buffered off-screen image called imgOff
            imgOff = Image.new(
                "RGB", (DIM.width, DIM.height), Color.BLACK)

            self.gamePanel.update(imgOff)
            self.checkCollisions()
            self.checkNewLevel()
            self.checkFloaters()

            try:
                startTime += Game.ANIMATION_DELAY
                time.sleep(
                    max(0.0, round(startTime - time.time() * 1000)/1000))
            except:
                pass

    def checkCollisions(self):

        for movFriend in CommandCenter.getInstance().movFriends:
            if not movFriend.alive: continue
            for movFoe in CommandCenter.getInstance().movFoes:
                if not movFoe.alive: continue
                pntFriendCenter = movFriend.getCenter()
                pntFoeCenter = movFoe.getCenter()
                radFriend = movFriend.getRadius()
                radFoe = movFoe.getRadius()
                if pntFriendCenter.distance(pntFoeCenter) < (radFoe + radFriend):
                    CommandCenter.getInstance().opsQueue.enqueue(movFriend, GameOp.Action.REMOVE)


                    CommandCenter.getInstance().opsQueue.enqueue(movFoe, GameOp.Action.REMOVE)
                    if isinstance(movFoe,Brick):
                        CommandCenter.getInstance().score += + 1000
                        Sound.playSound(self.cwd+"rock.wav")
                    else:
                        CommandCenter.getInstance().score += + 10
                        Sound.playSound(self.cwd+"kapow.wav")


        pntFalcon = CommandCenter.getInstance().falcon.center
        radFalcon = CommandCenter.getInstance().falcon.getRadius()
        for movFloater in CommandCenter.getInstance().movFloaters:
            if not movFloater.alive: continue
            pntFloaterCenter = movFloater.getCenter()
            radFloater = movFloater.getRadius()

            if (pntFalcon.distance(pntFloaterCenter) < (radFalcon + radFloater)):
                if isinstance(movFloater, ShieldFloater):
                    Sound.playSound(self.cwd+"shieldup.wav")
                    CommandCenter.getInstance().falcon.shield = MAX_SHIELD
                elif isinstance(movFloater, NewWallFloater):
                    Sound.playSound(self.cwd+"insect.wav")
                    self.buildWall()
                #the only other kind of floater is a nukeFloater
                else:
                    CommandCenter.getInstance().falcon.nukeMeter = MAX_NUKE
                    Sound.playSound(self.cwd + "nuke-up.wav")

                CommandCenter.getInstance().opsQueue.enqueue(movFloater, GameOp.Action.REMOVE)


        self.processAddsAndMarkRemoves()
        self.processRemoves()


    def processAddsAndMarkRemoves(self):
        # deferred mutation: these operations are done AFTER we have completed our collision detection to avoid
        # mutating the movable linkedlists while iterating them above.
        while len(CommandCenter.getInstance().opsQueue) > 0:
            gameOp = CommandCenter.getInstance().opsQueue.dequeue()
            mov = gameOp.movable
            action = gameOp.action

            if mov.getTeam() == Movable.Team.FOE:
                if action == GameOp.Action.ADD:
                    CommandCenter.getInstance().movFoes.append(mov)
                else:  # GameOp.Operation.REMOVE
                    mov.alive = False
                    if isinstance(mov, Asteroid):
                        self.spawnSmallerAsteroidOrDebris(mov)

            elif mov.getTeam() == Movable.Team.FRIEND:
                if action == GameOp.Action.ADD:
                    CommandCenter.getInstance().movFriends.append(mov)
                else:  # GameOp.Operation.REMOVE
                    if isinstance(mov, Falcon.Falcon):
                        CommandCenter.getInstance().initFalconAndDecrementFalconNum()
                    else:
                        mov.alive = False


            elif mov.getTeam() == Movable.Team.FLOATER:
                if action == GameOp.Action.ADD:
                    CommandCenter.getInstance().movFloaters.append(mov)
                else:  # GameOp.Operation.REMOVE
                    mov.alive = False
            elif mov.getTeam() == Movable.Team.DEBRIS:
                if action == GameOp.Action.ADD:
                    CommandCenter.getInstance().movDebris.append(mov)
                else:  # GameOp.Operation.REMOVE
                    mov.alive = False


    def processRemoves(self):
        CommandCenter.getInstance().purgeDeadMovables()


    def buildWall(self):
        BRICK_SIZE = int(DIM.width / 30)
        ROWS = 2
        COLS = 20
        X_OFFSET = int(BRICK_SIZE * 5)
        Y_OFFSET = 50

        for nCol in range(0, COLS):
            for nRow in range(0, ROWS):
                    CommandCenter.getInstance().opsQueue.enqueue(Brick(Point(int(nCol * BRICK_SIZE + X_OFFSET), int(nRow * BRICK_SIZE + Y_OFFSET)), BRICK_SIZE), GameOp.Action.ADD)


    def main(self):
        self.gamePanel.gameFrame.mainloop()

    def checkNewLevel(self):
        if self.isLevelClear():
            level = CommandCenter.getInstance().level
            CommandCenter.getInstance().score += 10_000 * level
            level += 1
            CommandCenter.getInstance().level = level
            self.spawnBigAsteroids(level)
            CommandCenter.getInstance().falcon.shield = INITIAL_SPAWN_TIME
            CommandCenter.getInstance().falcon.showLevel = INITIAL_SPAWN_TIME



    def isLevelClear(self):
        asteroidFree = True
        for movFoe in CommandCenter.getInstance().movFoes:
            if isinstance(movFoe, Asteroid):
                asteroidFree = False
                break
        return asteroidFree


    def isBrickFree(self):
        brickFree = True
        for movFoe in CommandCenter.getInstance().movFoes:
            if isinstance(movFoe, Brick):
                brickFree = False
                break
        return brickFree

    def spawnBigAsteroids(self, num):
        while num > 0:
            CommandCenter.getInstance().opsQueue.enqueue(Asteroid(0), GameOp.Action.ADD)
            num -= 1


    def checkFloaters(self):
        self.spawnShieldFloater()
        self.spawnNewWallFloater()
        self.spawnNukeFloater()

    def spawnNewWallFloater(self):
        if CommandCenter.getInstance().frame % SPAWN_NEW_WALL_FLOATER == 0 and self.isBrickFree():
            CommandCenter.getInstance().opsQueue.enqueue(NewWallFloater(), GameOp.Action.ADD)
    def spawnNukeFloater(self):
        if CommandCenter.getInstance().frame % SPAWN_NUKE_FLOATER == 0:
            CommandCenter.getInstance().opsQueue.enqueue(NukeFloater(), GameOp.Action.ADD)

    def spawnShieldFloater(self):
        if CommandCenter.getInstance().frame % SPAWN_SHIELD_FLOATER == 0:
            CommandCenter.getInstance().opsQueue.enqueue(ShieldFloater(), GameOp.Action.ADD)

    def spawnSmallerAsteroidOrDebris(self, originalAsteroid: Asteroid):
        size = originalAsteroid.getSize()
        if size > 1:
            CommandCenter.getInstance(). \
                opsQueue. \
                enqueue(WhiteCloudDebris(originalAsteroid), GameOp.Action.ADD)
        else:
            size += 2
            while size > 0:
                CommandCenter.getInstance().opsQueue \
                    .enqueue(Asteroid(originalAsteroid), GameOp.Action.ADD)
                size -= 1

    def stopLoopingSounds(self,*sounds):
        [sound.stop() for sound in sounds if hasattr(sound, "stop") ]

    def keyPressed(self, event):
        falcon = CommandCenter.getInstance().falcon
        keyCode = event.keysym
        print(keyCode)
        if keyCode == Game.START and CommandCenter.getInstance().isGameOver():
            CommandCenter.getInstance().initGame()
            return

        if keyCode == Game.PAUSE:
            CommandCenter.getInstance().paused = not CommandCenter.getInstance().paused

        elif keyCode == Game.QUIT:
            sys.exit(0)
        elif keyCode == Game.UP:
            falcon.thrusting = True

        elif keyCode == Game.LEFT:
            falcon.turnState = Falcon.TurnState.LEFT
        elif keyCode == Game.RIGHT:
            falcon.turnState = Falcon.TurnState.RIGHT

    def keyReleased(self, event):
        falcon = CommandCenter.getInstance().falcon
        keyCode = event.keysym
        if keyCode == Game.FIRE:
            CommandCenter.getInstance().opsQueue.enqueue(Bullet(falcon), GameOp.Action.ADD)
            Sound.playSound(self.cwd+"thump.wav")

        elif keyCode == Game.NUKE:
            if (CommandCenter.getInstance().falcon.nukeMeter > 0):
                CommandCenter.getInstance().opsQueue.enqueue(Nuke(falcon), GameOp.Action.ADD)
                CommandCenter.getInstance().falcon.nukeMeter = 0
                Sound.playSound(self.cwd + "nuke.wav")


        elif keyCode == Game.RIGHT or keyCode == Game.LEFT:
            falcon.turnState = Falcon.TurnState.IDLE
        elif keyCode == Game.UP:
            falcon.thrusting = False

        elif keyCode == Game.MUTE:
            CommandCenter.getInstance().getInstance().muted = not CommandCenter.getInstance().muted


if __name__ == "__main__":
    game = Game()

