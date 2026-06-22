import pygame

from mvc.model.Movable import Movable
from mvc.model.Asteroid import Asteroid
from mvc.model.Nuke import Nuke
from mvc.model.NukeFloater import NukeFloater
from mvc.model.ShieldFloater import ShieldFloater
#from pythonic.mvc.model.prime.Dimension import Dimension
from mvc.view.GamePanel import GamePanel
from mvc.controller.CommandCenter import CommandCenter, Universe
from mvc.model import Falcon
from mvc.model.Bullet import Bullet
from mvc.controller.GameOp import GameOp
from mvc.model.prime.Constants import DIM, SPAWN_SHIELD_FLOATER, SPAWN_NUKE_FLOATER, INITIAL_SPAWN_TIME
from mvc.model.prime.Point import Point
from mvc.controller.SoundLoader import SoundLoader

# todo: refactor the code so that its in python style, and clean-up
class Game:
    # ===============================================
    # FIELDS
    # ===============================================

    ANIMATION_DELAY = 40  # milliseconds between frames
    FRAMES_PER_SECOND = 1000 // ANIMATION_DELAY

    # key-codes (pygame key constants)
    PAUSE = pygame.K_p  # p key
    QUIT = pygame.K_q  # q key
    LEFT = pygame.K_LEFT  # rotate left; left arrow
    RIGHT = pygame.K_RIGHT  # rotate right; right arrow
    UP = pygame.K_UP  # thrust; up arrow
    START = pygame.K_s  # s key
    FIRE = pygame.K_SPACE  # space key
    MUTE = pygame.K_m  # m-key mute
    NUKE = pygame.K_f  # f-key
    RADAR = pygame.K_a
    SMART = pygame.K_v

    # for possible future use
    # HYPER = 68 # D key
    # ALIEN = 65 # A key
    # SPECIAL = 70 # fire special weapon;  F key

    # ===============================================
    # ==CONSTRUCTOR
    # ===============================================

    def __init__(self):
        # one-shot pygame/mixer bootstrap; needs CommandCenter constructed first.
        CommandCenter.getInstance()
        SoundLoader.init()
        #self.DIM = self.setDimFromEnv()
        self.gamePanel = GamePanel(DIM)

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
            action = gameOp.action
            if action == GameOp.Action.ADD:
                mov.addToGame(list)
            else:
                mov.removeFromGame(list)

    # The frame loop is driven by pygame: poll input events, advance and
    # draw one frame, then sleep to cap the rate at FRAMES_PER_SECOND.
    def main(self):
        # start the theme music
        SoundLoader.playLoopSound("dr_loop.wav")
        CommandCenter.getInstance().getInstance().isMuted = False

        clock = pygame.time.Clock()
        gameFrame = self.gamePanel.gameFrame

        while gameFrame.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameFrame.running = False
                elif event.type == pygame.KEYDOWN:
                    self.keyPressed(event.key)
                elif event.type == pygame.KEYUP:
                    self.keyReleased(event.key)

            if not gameFrame.running:
                break

            try:
                self.gamePanel.update()
                self.checkCollisions()
                self.checkNewLevel()
                self.checkFloaters()
                self.processGameOpsQueue()
            except Exception as e:
                import traceback
                print("Animation loop error:", e)
                traceback.print_exc()
                break

            clock.tick(Game.FRAMES_PER_SECOND)

        pygame.quit()

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
        while num > 0:
            CommandCenter.getInstance().opsQueue.enqueue(Asteroid(0), GameOp.Action.ADD)
            num -= 1

    def checkFloaters(self):
        self.spawnShieldFloater()
        self.spawnNukeFloater()

    def spawnNukeFloater(self):
        if CommandCenter.getInstance().frame % SPAWN_NUKE_FLOATER == 0:
            CommandCenter.getInstance().opsQueue.enqueue(NukeFloater(), GameOp.Action.ADD)

    def spawnShieldFloater(self):
        if CommandCenter.getInstance().frame % SPAWN_SHIELD_FLOATER == 0:
            CommandCenter.getInstance().opsQueue.enqueue(ShieldFloater(), GameOp.Action.ADD)

    def stopLoopingSounds(self, *sounds):
        [sound.stop() for sound in sounds if hasattr(sound, "stop")]

    def keyPressed(self, keyCode):
        falcon = CommandCenter.getInstance().falcon
        # print(keyCode)
        if keyCode == Game.START and CommandCenter.getInstance().isGameOver():
            CommandCenter.getInstance().initGame()
            return
        if keyCode == Game.PAUSE:
            CommandCenter.getInstance().isPaused = not CommandCenter.getInstance().isPaused
        elif keyCode == Game.QUIT:
            self.gamePanel.gameFrame.running = False
        elif keyCode == Game.UP:
            falcon.thrusting = True
            SoundLoader.playLoopSound("whitenoise_loop.wav")
        elif keyCode == Game.LEFT:
            falcon.turnState = Falcon.TurnState.LEFT
        elif keyCode == Game.RIGHT:
            falcon.turnState = Falcon.TurnState.RIGHT

    def keyReleased(self, keyCode):
        falcon = CommandCenter.getInstance().falcon
        if keyCode == Game.FIRE:
            CommandCenter.getInstance().opsQueue.enqueue(Bullet(falcon), GameOp.Action.ADD)
        elif keyCode == Game.NUKE:
            CommandCenter.getInstance().opsQueue.enqueue(Nuke(falcon), GameOp.Action.ADD)
        elif keyCode == Game.RIGHT or keyCode == Game.LEFT:
            falcon.turnState = Falcon.TurnState.IDLE
        elif keyCode == Game.UP:
            falcon.thrusting = False
            SoundLoader.stopLoopSound("whitenoise_loop.wav")

        elif keyCode == Game.SMART:
            CommandCenter.getInstance().killAll()

        elif keyCode == Game.MUTE:
            if not CommandCenter.getInstance().getInstance().isMuted:
                SoundLoader.stopLoopSound("dr_loop.wav")
                CommandCenter.getInstance().getInstance().isMuted = True
            else:
                SoundLoader.playLoopSound("dr_loop.wav")
                CommandCenter.getInstance().getInstance().isMuted = False

        elif keyCode == Game.RADAR:
            CommandCenter.getInstance().isRadar = not CommandCenter.getInstance().isRadar

if __name__ == "__main__":
    game = Game()
    game.main()