from model.color import Color


class Canvas:
    def __init__(self, w: int, h: int, init_color: Color = Color(255, 255, 255)):
        self.w = w
        self.h = h
        self.init_color = init_color
        self._canvas = None
        self.reset()

    def at(self, x: int, y: int):
        return self._canvas[y][x]

    def set(self, x: int, y: int, color: Color):
        self._canvas[y][x] = color

    def reset(self):
        self._canvas = [[self.init_color] * self.w for _ in range(self.h)]
