import os
import sys
import traceback

from pythonic.mvc.model.Sprite import Sprite


class ImageLoader:
    __instance = None
    masterImageMap = {}

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(ImageLoader, cls).__new__(cls)
            return cls.__instance
        raise Exception(" one instance of CommandCenter is already created ")

    def __init__(self):
        from pythonic.mvc.controller.CommandCenter import CommandCenter
        rootDirectory = CommandCenter.getInstance().img
        localMap = {}
        try:
            localMap = self.loadPngImages(rootDirectory)
        except Exception:
            print(traceback.format_exc())

        self.masterImageMap = localMap

    @staticmethod
    def getInstance():
        # this is now a singleton
        if (ImageLoader.__instance is None):
            ImageLoader.__instance = ImageLoader()

        return ImageLoader.__instance

    @staticmethod
    def loadPngImages(rootDirectory):
        pngImages = {}
        dirs = os.listdir(rootDirectory)

        for dir in dirs:
            currentPath = rootDirectory + dir
            files = os.listdir(currentPath)
            for file in files:
                split_text = os.path.splitext(file)
                if split_text[1] == '.png':
                    # print(os.path.join(currentPath,file))
                    pngImages[split_text[0]] = Sprite.loadGraphic(os.path.join(currentPath,file))

        return pngImages
