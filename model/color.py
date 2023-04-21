class Color:
    def __init__(self, integer, g=None, b=None):
        if g is None:
            self._r = (integer >> 16) & 255
            self._g = (integer >> 8) & 255
            self._b = integer & 255
        else:
            self._r = integer
            self._g = g
            self._b = b

    def r(self) -> int:
        return self._r

    def g(self) -> int:
        return self._g

    def b(self) -> int:
        return self._g

    def rgb(self) -> (int, int, int):
        return self._r, self._g, self._b

    def to_integer(self) -> int:
        return (self._r << 16) | (self._g << 8) | self._b
