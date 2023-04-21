from typing import List, Dict

from model.canvas import Canvas
from model.color import Color

GRAVITATION = 9.80665
PI = 3.1415926535898
MASS_MULTIPLIER = 0.001


class Catapult:
    def __init__(self, canvas: Canvas):
        self.canvas = canvas

    def shoot(self, power: float, hor_angle: float, ver_angle: float, colors: dict[Color, int]):
        raise NotImplemented
