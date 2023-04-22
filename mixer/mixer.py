import random

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
    if len(storage) > 1000:
        storage = {k: storage[k] for k in random.sample(list(storage.keys()), 1000)}
    else:
        storage = dict(storage)
    target = target.rgb_np()
    current_amount = sum(storage.values())
    current = sum([w * c.rgb_np() for c, w in storage.items()]) / current_amount
    while current_amount > target_amount * 2 and len(storage) > 100:
        diff = current - target

        bads = sorted(list(storage.keys()), key=lambda c: np.dot(c.rgb_np() - target, diff) / np.linalg.norm(diff))[-50:]
        for bad in bads:
            bad_amount = storage[bad]
            current = (current * current_amount - bad.rgb_np() * bad_amount) / (current_amount - bad_amount)
            current_amount -= bad_amount
            storage[bad] -= bad_amount
            if storage[bad] == 0:
                storage.pop(bad)
        # print(f'rough stage: still has {current_amount}/{target_amount}, current avg {current}')

    while current_amount > target_amount:
        diff = current - target

        bads = sorted(list(storage.keys()), key=lambda c: np.dot(c.rgb_np() - target, diff) / np.linalg.norm(diff))[-1:]#[-(current_amount - target_amount) // 50 - 1:]
        for bad in bads:
            bad_amount = min(storage[bad], (current_amount - target_amount) // 10 + 1)
            current = (current * current_amount - bad.rgb_np() * bad_amount) / (current_amount - bad_amount)
            current_amount -= bad_amount
            storage[bad] -= bad_amount
            if storage[bad] == 0:
                storage.pop(bad)
        # print(f'fine stage: still has {current_amount}/{target_amount}, current avg {current}')

    return storage
