import math

from model.catapult import Catapult, MASS_MULTIPLIER, GRAVITATION, PI
from model.color import Color


class SimpleCatapult(Catapult):
    def shoot(self, power: float, hor_angle: float, ver_angle: float, colors: dict[Color, int]):
        color = Color.mix_colors(colors)
        color_amount = sum(colors.values())
        local_x, local_y = self._simulate_trajectory(power, hor_angle, ver_angle, color_amount)
        canvas_x, canvas_y = self._local2canvas(local_x, local_y)
        self._paint(int(canvas_x), int(canvas_y), color_amount, color)

    def _paint(self, x: int, y: int, amount: int, color: Color):
        radius = int(math.sqrt(amount))
        for ix in range(x - radius // 2, x + radius // 2):
            for iy in range(y - radius // 2, y + radius // 2):
                self.canvas.set(ix, iy, color)

    def _local2canvas(self, local_x: float, local_y: float):
        return local_x + self.canvas.w / 2, local_y - 300

    @staticmethod
    def _simulate_trajectory(power: float, hor_angle: float, ver_angle: float, mass: float):
        velocity = power / (mass * MASS_MULTIPLIER)
        ver_velocity = math.sin(ver_angle / 180 * PI) * velocity
        hor_velocity = math.cos(ver_angle / 180 * PI) * velocity
        t = ver_velocity / GRAVITATION
        distance = hor_velocity * t
        return distance * math.cos(hor_angle / 180 * PI), distance * math.sin(ver_angle / 180 * PI)
