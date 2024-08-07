class AspectRatio:
    width = 0.0
    height = 0.0

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def scale(self, scale):
        self.width = self.width * scale
        self.height = self.height * scale
        return self
