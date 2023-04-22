import http.client
import json
import time

import numpy as np
from scipy.constants import precision

from client import Client
from client.mock_api import MockAPI
from client.api import PrefixAPI
from client.dats_api import DatsArtHttpAPI, DatsArtHttpJsonAPI
from model.color import Color
from mixer.mixer import find_mix
from requests import Session
from tqdm.auto import tqdm

token = '643ef1557ac24643ef1557ac25'
session = Session()
session.headers.update({'Authorization': f'Bearer {token}'})

api = PrefixAPI('/art', DatsArtHttpAPI('http://api.datsart.dats.team/', session))
client = Client(api)
colors = client.colors.list()['response']
colors = {Color(int(k)): v for k, v in colors.items()}

# comment 2 lines down to go production
api = PrefixAPI('/art', DatsArtHttpJsonAPI('http://127.0.0.1:8000/', session))
client = Client(api)

# client.ballista.shoot_aim(250, 110, 120, {int(k): v for k, v in colors.items()})

# target = Color(192, 39, 46)
# colors = find_mix(colors, target, 1500)
# print(f'target: {target}, result: {Color.mix_colors(colors)} {sum(colors.values())}')
# exit(0)

with open('solutions/level_6_ufo.json') as f:
    solutions = json.load(f)

solutions = sorted(solutions, key=lambda arr: arr[1], reverse=False)
# solutions = sorted(solutions, key=lambda arr: arr[2], reverse=True)


# exit(0)

def amount_in_radius(r):
    cnt = 0
    for x in range(-r, r + 1):
        for y in range(-r, r + 1):
            if x ** 2 + y ** 2 <= r ** 2:
                cnt += 1
    # d = r * 2 + 1
    # return (1 + d) * (r + 1) // 2 + (1 + d - 2) * r // 2
    return cnt


def is_white(color: Color):
    return np.linalg.norm(Color(255, 255, 255).rgb_np() - color.rgb_np()) < 30


solutions = solutions[:]
start_time = time.time()
idx = 0
precalculated_colors = []
for x, y, r, color in tqdm(solutions):
    color = Color(*color)
    if is_white(color):
        continue

    paint = find_mix(colors, color, amount_in_radius(r))
    if sum(paint.values()) != amount_in_radius(r):
        print(f'error with {x} {y} {r} {color} - {sum(paint.values())} != {amount_in_radius(r)}')
    print(f'target: {color}, result: {Color.mix_colors(paint)} {sum(paint.values())}/{amount_in_radius(r)}')
    for c, cnt in paint.items():
        colors[c] -= cnt
        if colors[c] <= 0:
            colors.pop(c)

    precalculated_colors.append({c.to_integer(): cnt for c, cnt in paint.items()})
    idx += 1

print(f'calculated mixing, took {time.time() - start_time}s')

with open('solutions/level_6_ufo_colors.json', 'w') as f:
    json.dump(precalculated_colors, f)

with open('solutions/level_6_ufo_colors.json') as f:
    precalculated_colors = json.load(f)
start_time = time.time()
print(f'total amount of paint: {sum([sum(x.values()) for x in precalculated_colors])}')
idx = 0
for x, y, r, color in reversed(solutions):
    color = Color(*color)
    if is_white(color):
        continue
    paint = precalculated_colors[-idx - 1]
    if idx <= -1:
        idx += 1
        continue
    result_color = Color.mix_colors({Color(int(k)): v for k, v in paint.items()})
    if np.linalg.norm(result_color.rgb_np() - color.rgb_np()) > 1e9:
        idx += 1
        print(f'skipping {idx} because color too bad: {result_color} insead of {color}')
        continue

    while True:
        time.sleep(0.5)
        try:
            result = client.ballista.shoot_aim(500, x, y, paint)
        except ConnectionAbortedError:
            print('connection aborted')
            time.sleep(2)
            continue
        except RecursionError:
            print(f'could not shoot idx={idx}')
            break

        if 'success' in result and result['success']:
            print(f'success {idx}')
            break
        if 'message' in result and 'Queue already has similar command' in result['message']:
            time.sleep(1)
        else:
            print(f'unknown result: {result}')

    idx += 1
# print(sorted(rs))
from collections import Counter

# print(Counter(rs))
# print(max(res['response'].items(), key=lambda x: x[1]))
print(f'finished shoting, took {time.time() - start_time}s')
print('Done, enjoy!')
