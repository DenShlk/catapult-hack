import numpy as np

from model.color import Color


# class Mix:
#     def __init__(self, colors: list[Color], amounts: list[int]):
#         self.colors = colors
#         self.amounts = amounts
#
#     def mix_with(self, another: 'Mix') -> 'Mix':
#         return Mix(self.colors + another.colors, self.amounts + another.amounts)


def find_mix(storage: dict[Color, int], target: Color, target_amount: int) -> dict[Color, int]:
    storage = dict(storage)
    target = target.rgb_np()
    current = Color.mix_colors(storage).rgb_np()
    current_amount = sum(storage.values())
    while current_amount > target_amount * 2:
        diff = current - target
        worst = None
        worst_proj = -1
        for c in storage:
            proj = np.dot(c.rgb_np() - target, diff) / np.linalg.norm(diff)
            if proj > worst_proj:
                worst, worst_proj = c, proj
        worst_amount = storage[worst]
        current = Color(*list((current * current_amount - worst.rgb_np() * worst_amount)
                              // (current_amount - worst_amount)))
        current_amount -= worst_amount
        storage[worst] -= worst_amount
        if storage[worst] == 0:
            storage.pop(worst)

    while current_amount > target_amount:
        diff = current - target
        worst = None
        worst_proj = -1
        for c in storage:
            proj = np.dot(c.rgb_np() - target, diff) / np.linalg.norm(diff)
            if proj > worst_proj:
                worst, worst_proj = c, proj
        worst_amount = 1
        current = Color(*list((current * current_amount - worst.rgb_np() * worst_amount)
                              // (current_amount - worst_amount)))
        current_amount -= worst_amount
        storage[worst] -= worst_amount
        if storage[worst] == 0:
            storage.pop(worst)

    return storage
