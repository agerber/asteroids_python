import os
import sys
import traceback

from pythonic.mvc.model.Sprite import Sprite
from PIL import Image, ImageOps,ImageDraw

class ImageLoader:
    __instance = None
    IMAGES = {}

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

        self.IMAGES = localMap

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
            if dir.startswith('.'):
                continue
            currentPath = os.path.join(rootDirectory, dir)
            files = os.listdir(currentPath)
            for file in files:
                # Ignore hidden files

                split_text = os.path.splitext(file)
                if split_text[1] == '.png' and 'do_not_load' not in split_text[0]:
                    # print(os.path.join(currentPath,file))
                    pngImages[split_text[0]] = ImageLoader.loadGraphic(os.path.join(currentPath, file))

        return pngImages

    @staticmethod
    def loadGraphic(image_path: str) -> Image.Image:
        try:
            buffered_image = Image.open(image_path)
        except IOError as e:
            raise Exception(f"Cannot open image: {image_path}")
        return buffered_image