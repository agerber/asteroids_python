import pygame


class SoundLoader:
    # static member
    soundDictionary = {}
    # one-shot sounds, loaded lazily and cached (keyed by filename)
    _oneShotCache = {}
    _initialized = False

    # Eager pygame/mixer setup is deferred out of the class body so that
    # importing this module no longer forces CommandCenter to construct.
    # Call SoundLoader.init() once at startup, after CommandCenter exists.
    @classmethod
    def init(cls):
        if cls._initialized:
            return
        from mvc.controller.CommandCenter import CommandCenter
        pygame.mixer.init()
        # give one-shot effects (explosions, bullets, spawns) room to overlap
        pygame.mixer.set_num_channels(32)
        snd = CommandCenter.getInstance().snd
        cls.soundDictionary = {
            "whitenoise_loop.wav": pygame.mixer.Sound(snd + "whitenoise_loop.wav"),
            "dr_loop.wav":          pygame.mixer.Sound(snd + "dr_loop.wav"),
        }
        cls._initialized = True

    @classmethod
    def playLoopSound(cls, name):
        cls.soundDictionary.get(name).play(loops=-1)

    @classmethod
    def stopLoopSound(cls, name):
        cls.soundDictionary.get(name).stop()

    # Fire-and-forget one-shot effect. pygame.mixer.Sound.play() is
    # non-blocking and grabs a free channel on its own, so no thread pool is
    # needed; the Sound object is cached after first load.
    @classmethod
    def playSound(cls, name):
        from mvc.controller.CommandCenter import CommandCenter
        try:
            sound = cls._oneShotCache.get(name)
            if sound is None:
                sound = pygame.mixer.Sound(CommandCenter.getInstance().snd + name)
                cls._oneShotCache[name] = sound
            sound.play()
        except Exception:
            pass
