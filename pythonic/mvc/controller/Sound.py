import simpleaudio as sa
import os
import pygame
from pythonic.mvc.controller.CommandCenter import CommandCenter
from concurrent.futures import ThreadPoolExecutor
class Sound:
    #static member
    soundExecutor = ThreadPoolExecutor(max_workers=5)

    #use pygame to play/stop loops
    pygame.mixer.init()

    #load looping clips
    thrustClip = pygame.mixer.Sound(CommandCenter.getInstance().snd + "whitenoise.wav")
    backgroundClip = pygame.mixer.Sound(CommandCenter.getInstance().snd + "music-background.wav")
    #put them into dictionary
    soundDictionary = {"whitenoise.wav": thrustClip, "music-background.wav": backgroundClip}

    @classmethod
    def playLoopSound(cls, name):
        cls.soundDictionary.get(name).play(loops=-1)

    @classmethod
    def stopLoopSound(cls, name):
        cls.soundDictionary.get(name).stop()

    @staticmethod
    def playSound(strPath):

        def run(strPath):
            try:
                wavSound = sa.WaveObject.from_wave_file(strPath)
                wavSound.play()
            except Exception as e:
                pass

        #pass the above lambda to thread-pool, along with the path to file
        Sound.soundExecutor.submit(run, strPath)



# if __name__ == "__main__":
#     cwd = "/".join(os.getcwd().split('/')[:-2])
#     Sound.clipForLoopFactory(cwd+"/resources/sounds/whitenoise.wav")