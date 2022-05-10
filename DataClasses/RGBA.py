from PyQt5.QtGui import QColor


class RGBA:
    def __init__(self, r: int, g: int, b: int, a: int):
        self.r = r
        self.g = g
        self.b = b
        self.a = a
        if r > 255 or g > 255 or b > 255 or a > 255 or r < 0 or g < 0 or b < 0 or a < 0:
            raise ValueError("cannot have rgb greater than 255 or less than 0")

    def color(self):
        c = QColor(self.r, self.g, self.b)
        c.setAlpha(self.a)
        return c