class AspectDim:
    w = 0.0
    h = 0.0

    def __init__(self, width, height):
        self.w = width
        self.h = height

    def scale(self, scale):
        return AspectDim(self.w * scale, self.h * scale)
