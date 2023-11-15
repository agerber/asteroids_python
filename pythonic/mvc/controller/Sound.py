import simpleaudio as sa
import os
from pythonic.mvc.controller.CommandCenter import CommandCenter
from concurrent.futures import ThreadPoolExecutor
class Sound:
    #static member
    soundExecutor = ThreadPoolExecutor(max_workers=5)
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

    # todo: thrust and background music not looping properly.
    @staticmethod
    def clipForLoopFactory(fileName):
        try:
            wave_obj = sa.WaveObject.from_wave_file(fileName)
            return wave_obj
        except Exception as e:
            pass



if __name__ == "__main__":
    cwd = "/".join(os.getcwd().split('/')[:-2])
    Sound.clipForLoopFactory(cwd+"/resources/sounds/whitenoise.wav")