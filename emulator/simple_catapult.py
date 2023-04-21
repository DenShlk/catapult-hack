import math
import random

from model.catapult import Catapult, MASS_MULTIPLIER, GRAVITATION, PI
from model.color import Color


class SimpleCatapult(Catapult):

    def shoot(self, power: float, angle_horizontal: float, angle_vertical: float, colors: dict[Color, int]):
        color = Color.mix_colors(colors)
        color_amount = sum(colors.values())
        local_x, local_y = self._simulate_trajectory(power, angle_horizontal, angle_vertical, color_amount)
        canvas_x, canvas_y = self._local2canvas(local_x, local_y)
        print(f'shot at ({canvas_x}, {canvas_y})')
        self.paint(int(canvas_x), int(canvas_y), color_amount, color)

    def stupid_paint(self, x: int, y: int, amount: int, color: Color):
        radius = int(math.sqrt(amount))
        for ix in range(x - radius // 2, x + radius // 2 + 1):
            for iy in range(y - radius // 2, y + radius // 2 + 1):
                self.canvas.set(ix, iy, color)
                
    def paint(self, x: int, y: int, amount: int, color: Color):
        def amount_in_radius(r):
            d = r * 2 + 1
            return (1 + d) * (r + 1) // 2 + (1 + d - 2) * r // 2

        radius = 0
        while amount_in_radius(radius) <= amount:
            radius += 1

        left_over_points = []
        for xx in range(x - radius, x + radius + 1):
            for yy in range(y - radius, y + radius + 1):
                dist = abs(x - xx) + abs(y - yy)
                if dist < radius:
                    self.canvas.set(xx, yy, color)
                elif dist == radius:
                    left_over_points.append((xx, yy))

        left_over_cnt = amount - amount_in_radius(radius - 1)
        for xx, yy in random.sample(left_over_points, left_over_cnt):
            self.canvas.set(xx, yy, color)

    def _local2canvas(self, local_x: float, local_y: float):
        return local_x + self.canvas.w / 2, local_y - 300

    def _canvas2local(self, canvas_x: float, canvas_y: float):
        return canvas_x - self.canvas.w / 2, canvas_y + 300

    @staticmethod
    def _simulate_trajectory(power: float, hor_angle: float, ver_angle: float, mass: float):
        velocity = (2 * power / (mass * MASS_MULTIPLIER)) ** .5
        ver_velocity = math.sin(ver_angle / 180 * PI) * velocity
        hor_velocity = math.cos(ver_angle / 180 * PI) * velocity
        t = 2 * ver_velocity / GRAVITATION
        distance = hor_velocity * t
        return distance * math.sin(hor_angle / 180 * PI), distance * math.cos(hor_angle / 180 * PI)
