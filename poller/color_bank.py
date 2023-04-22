from model.color import Color

from typing import List, Dict


# Color(192, 39, 46): 13288, Color(35, 35, 35): 2390
class ColorBank:
    def __init__(self, wanted_colors: dict[Color, int], storage: dict[int, int]):
        self.wanted_colors = wanted_colors
        self.colors = {Color(k): v for k, v in storage.items()}

    def choose(self, colors: List[Dict[str, int]]):
        colors = {Color(c['color']): c['amount'] for c in colors}
