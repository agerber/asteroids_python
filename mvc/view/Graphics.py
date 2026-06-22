from collections import OrderedDict
from PIL import Image, ImageDraw



# Java's java.awt.Graphics is a stateful drawing context: callers set the
# current color/font on it, then issue draw/fill calls that consume that
# state. Python's PIL exposes the same primitives through ImageDraw, but
# without the stateful color/font and without a single object that also
# knows how to blit raster images. Graphics binds an Image + an ImageDraw
# together and presents the same Java-style API so the Movable.draw(g)
# contract is a direct, faithful port.
class Graphics:

    # LRU cache of pre-rasterized text glyphs, keyed by (text, font_id,
    # color). FreeType glyph rasterization through PIL.ImageDraw.text is
    # the dominant per-frame cost after the Tk bitmap transfer; caching
    # makes stable HUD strings (level, status) effectively free and keeps
    # ever-changing ones (frame counter) bounded.
    _TEXT_CACHE_CAP = 256
    _textCache: "OrderedDict[tuple, Image.Image]" = OrderedDict()

    def __init__(self, image: Image.Image):
        self._image = image
        self._draw = ImageDraw.Draw(image)
        self._color = (255, 255, 255)
        self._font = None

    @property
    def image(self) -> Image.Image:
        return self._image

    def setColor(self, color):
        self._color = color

    def getColor(self):
        return self._color

    def setFont(self, font):
        self._font = font

    def getFont(self):
        return self._font

    def drawLine(self, x1, y1, x2, y2):
        self._draw.line((x1, y1, x2, y2), fill=self._color)

    def drawRect(self, x, y, width, height):
        self._draw.rectangle((x, y, x + width, y + height), outline=self._color)

    def fillRect(self, x, y, width, height):
        self._draw.rectangle((x, y, x + width, y + height), fill=self._color)

    def drawOval(self, x, y, width, height):
        self._draw.ellipse((x, y, x + width, y + height), outline=self._color)

    def fillOval(self, x, y, width, height):
        self._draw.ellipse((x, y, x + width, y + height), fill=self._color)

    def drawPolygon(self, points):
        self._draw.polygon(list(points), outline=self._color)

    def fillPolygon(self, points):
        self._draw.polygon(list(points), fill=self._color)

    def drawString(self, text, x, y):
        key = (text, id(self._font), self._color)
        cache = Graphics._textCache
        glyph = cache.get(key)
        if glyph is None:
            bbox = self._draw.textbbox((0, 0), text, font=self._font)
            w = max(1, bbox[2] - bbox[0] + 2)
            h = max(1, bbox[3] - bbox[1] + 2)
            glyph = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            ImageDraw.Draw(glyph).text(
                (-bbox[0], -bbox[1]), text, font=self._font, fill=self._color
            )
            cache[key] = glyph
            if len(cache) > Graphics._TEXT_CACHE_CAP:
                cache.popitem(last=False)
        else:
            cache.move_to_end(key)
        self._image.paste(glyph, (int(x), int(y)), glyph)

    # Mirrors Graphics.drawImage(img, x, y, observer). Caller supplies the
    # top-left corner; alpha is honored when present.
    def drawImage(self, image: Image.Image, x: int, y: int):
        if image.mode == "RGBA":
            self._image.paste(image, (int(x), int(y)), image)
        else:
            self._image.paste(image, (int(x), int(y)))
