class AspectRatio:
    width = 0.0
    height = 0.0

    def __init__(self, width, height):
        self.width = width
        self.height = height

    # TODO This is an example of the Fluent_Interface design pattern, which relies on method chaining to make the code
    # more readable and intuitive. In this pattern, methods return the instance of the object, allowing multiple method
    # calls to be linked together in a single, fluid expression.

    def scale(self, scale):
        self.width = self.width * scale
        self.height = self.height * scale
        return self
