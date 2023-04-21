from typing import Type

from model.canvas import Canvas
from model.catapult import Catapult
from model.color import Color


class Emulator:
    def __init__(self, catapult_class: Type[Catapult], canvas: Canvas):
        self.catapult_class = catapult_class
        self.canvas = canvas
        self.catapult = self.catapult_class(self.canvas)

    def canvas(self):
        return self.canvas

    def shoot(self, power: float, hor_angle: float, ver_angle: float, colors: dict[int, int]):
        self.catapult.shoot(power, hor_angle, ver_angle, {Color(i): x for i, x in colors.items()})

    def reset(self):
        self.canvas.reset()
