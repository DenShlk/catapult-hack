from typing import Callable, Type

from model.canvas import Canvas
from model.catapult import Catapult


class Emulator:
    def __init__(self, catapult_class: Type[Catapult], canvas: Canvas):
        self.catapult_class = catapult_class
        self.canvas = canvas
        self.catapult = self.catapult_class(self.canvas)

