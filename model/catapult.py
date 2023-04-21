from typing import List, Dict

from model.canvas import Canvas
from model.color import Color

GRAVITATION = 9.80665
PI = 3.1415926535898
MASS_MULTIPLIER = 0.001 # * 100 / 4.464285714285714


class Catapult:
    def __init__(self, canvas: Canvas):
        self.canvas = canvas

    def shoot(self, power: float, angle_horizontal: float, angle_vertical: float, colors: dict[Color, int]):
        raise NotImplemented

    def paint(self, x: int, y: int, amount: int, color: Color):
        raise NotImplemented

    def point2params(self, x: int, y: int, mass: int):
        raise NotImplemented
