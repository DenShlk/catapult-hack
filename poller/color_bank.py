import numpy as np
from numpy.random import choice

from model.color import Color

from typing import List, Dict


# Color(192, 39, 46): 13288, Color(35, 35, 35): 2390
class ColorBank:
    def __init__(self, wanted_colors: dict[Color, int], storage: dict[int, int]):
        self.wanted_colors = list(wanted_colors.keys())
        self.wanted_colors_weights = np.array([wanted_colors[c] for c in self.wanted_colors], dtype=float)
        self.wanted_colors_weights /= np.sum(self.wanted_colors_weights)
        self.colors = {Color(int(k)): v for k, v in storage.items()}
        self.current_amount = sum(storage.values())
        self.current_average = sum([w * Color(c).rgb_np() for c, w in storage.items()]) / self.current_amount

    def choose(self, options: Dict[str, Dict[str, int]]):
        target = choice(self.wanted_colors, p=self.wanted_colors_weights).rgb_np()
        colors = {Color(c['color']): c['amount'] for c in options.values()}
        diff = self.current_average - target
        best = sorted(list(colors.keys()), key=lambda c: np.dot(c.rgb_np() - target, diff) / np.linalg.norm(diff))[0]

        new_amount = colors[best]
        self.current_average = (self.current_average * self.current_amount + best.rgb_np() * new_amount) \
                               / (self.current_amount + new_amount)
        self.current_amount += new_amount
        for id, option in options.items():
            if option['color'] == best.to_integer():
                return id
