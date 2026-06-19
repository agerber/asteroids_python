import simpleaudio as sa
import pygame
from concurrent.futures import ThreadPoolExecutor


class SoundLoader:
    # static member
    soundExecutor = ThreadPoolExecutor(max_workers=5)
    soundDictionary = {}
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

    @classmethod
    def playSound(cls, name):
        from mvc.controller.CommandCenter import CommandCenter

        def run(fileName):
            try:
                wavSound = sa.WaveObject.from_wave_file(CommandCenter.getInstance().snd + fileName)
                wavSound.play()
            except Exception as e:
                pass

        # pass the above lambda to thread-pool, along with the path to file
        cls.soundExecutor.submit(run, name)
