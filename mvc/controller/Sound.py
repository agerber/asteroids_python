import simpleaudio as sa
import pygame
from mvc.controller.CommandCenter import CommandCenter
from concurrent.futures import ThreadPoolExecutor


class Sound:
    # static member
    soundExecutor = ThreadPoolExecutor(max_workers=5)

    # use pygame to play/stop loops
    pygame.mixer.init()

    # load looping clips
    thrustClip = pygame.mixer.Sound(CommandCenter.getInstance().snd + "whitenoise_loop.wav")
    backgroundClip = pygame.mixer.Sound(CommandCenter.getInstance().snd + "dr_loop.wav")
    # put them into dictionary
    soundDictionary = {"whitenoise_loop.wav": thrustClip, "dr_loop.wav": backgroundClip}

    @classmethod
    def playLoopSound(cls, name):
        cls.soundDictionary.get(name).play(loops=-1)

    @classmethod
    def stopLoopSound(cls, name):
        cls.soundDictionary.get(name).stop()

    @classmethod
    def playSound(cls, name):

        def run(fileName):
            try:
                wavSound = sa.WaveObject.from_wave_file(CommandCenter.getInstance().snd + fileName)
                wavSound.play()
            except Exception as e:
                pass

        # pass the above lambda to thread-pool, along with the path to file
        cls.soundExecutor.submit(run, name)

# if __name__ == "__main__":
#     cwd = "/".join(os.getcwd().split('/')[:-2])
#     Sound.clipForLoopFactory(cwd+"/resources/sounds/whitenoise.wav")
