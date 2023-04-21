import math

from model.catapult import PI, GRAVITATION, MASS_MULTIPLIER


def point2params(canvas_w: int, x: int, y: int, mass: int):
    print(f'aiming to ({x}, {y})')
    ver_angle = 45 / 180 * PI
    local_x, local_y = canvas2catapult(canvas_w, x, y)
    distance = (local_x ** 2 + local_y ** 2) ** .5
    hor_angle = math.atan2(local_x, local_y)

    t = (2 * distance * math.tan(ver_angle) / GRAVITATION) ** .5
    hor_velocity = distance / t
    velocity = hor_velocity / math.cos(ver_angle)

    power = (mass * MASS_MULTIPLIER) * velocity ** 2 / 2
    return {'power': power, 'angle_horizontal': hor_angle * 180 / PI, 'angle_vertical': ver_angle * 180 / PI}


def catapult2canvas(canvas_w: int, local_x: float, local_y: float):
    return local_x + canvas_w / 2, local_y - 300


def canvas2catapult(canvas_w: int, canvas_x: float, canvas_y: float):
    return canvas_x - canvas_w / 2, canvas_y + 300
