from typing import Dict

from model.ballistics import point2params
from .api import API, PrefixAPI


class Base:
    def __init__(self, _api: API):
        self.api = _api


class Stage(Base):
    def __init__(self, api: API):
        super().__init__(api)

    def next(self):
        return self.api.exec('/next')

    def start_next(self, image_id):
        return self.api.exec('/next-start', data={'imageId': image_id})

    def info(self):
        return self.api.exec('/info')

    def finish(self):
        return self.api.exec('/finish')


class Factory(Base):
    def __init__(self, api: API):
        super().__init__(api)

    def generate(self):
        return self.api.exec('/generate')

    def pick(self, num, tick):
        return self.api.exec('/pick', data={'num': num, 'tick': tick})


class Colors(Base):
    def __init__(self, api: API):
        super().__init__(api)

    def info(self):
        return self.api.exec('/info')

    def amount(self, color):
        return self.api.exec('/amount', data={'color': color})

    def list(self):
        return self.api.exec('/list')


class Ballista(Base):
    def __init__(self, api: API):
        super().__init__(api)

    def shoot(self, angle_horizontal: float, angle_vertical: float, power: float, colors: Dict[int, int]):
        data = {
            'angleHorizontal': angle_horizontal,
            'angleVertical': angle_vertical,
            'power': round(power, 6),
        }

        for color in colors:
            data[f'colors[{color}]'] = colors[color]

        return self.api.exec('/shoot', data=data)

    def shoot_aim(self, canvas_w: int, x: int, y: int, colors: Dict[int, int]):
        params = point2params(canvas_w, x, y, sum(colors.values()))
        self.shoot(colors=colors, **params)


class State(Base):
    def __init__(self, api: API):
        super().__init__(api)

    def tick(self):
        return self.api.exec('/tick')

    def queue(self, _id: int):
        return self.api.exec('/queue', data={'id': _id})


class Client(Base):
    def __init__(self, _api: API):
        super().__init__(_api)

    @property
    def stage(self) -> Stage:
        return Stage(PrefixAPI('/stage', self.api))

    @property
    def factory(self) -> Factory:
        return Factory(PrefixAPI('/factory', self.api))

    @property
    def colors(self) -> Colors:
        return Colors(PrefixAPI('/colors', self.api))

    @property
    def ballista(self) -> Ballista:
        return Ballista(PrefixAPI('/ballista', self.api))

    @property
    def state(self) -> State:
        return State(PrefixAPI('/state', self.api))
