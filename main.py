import time

from client import Client
from client.mock_api import MockAPI
from client.api import PrefixAPI
from client.dats_api import DatsArtHttpAPI, DatsArtHttpJsonAPI
from model.color import Color
from requests import Session

token = '643ef1557ac24643ef1557ac25'
session = Session()
session.headers.update({'Authorization': f'Bearer {token}'})
if True:
    api = PrefixAPI('/art', DatsArtHttpAPI('http://api.datsart.dats.team/', session))
else:
    api = PrefixAPI('/art', DatsArtHttpJsonAPI('http://127.0.0.1:8000/', session))
client = Client(api)


colors = client.colors.list()['response']
colors = {k: colors[k] for k in list(colors.keys())}
# client.ballista.shoot_aim(250, 110, 120, {int(k): v for k, v in colors.items()})

print(find_mix(colors, ))

exit(0)
from json import load

with open('solutions/level_1.json') as f:
    solution = load(f)


def amount_in_radius(r):
    d = r * 2 + 1
    return (1 + d) * (r + 1) // 2 + (1 + d - 2) * r // 2


rs = []
for x, y, r, color in solution:
    # client.ballista.shoot_aim(250, x, y, {Color(*color).to_integer(): amount_in_radius(r)})
    # time.sleep(0.1)
    rs.append(amount_in_radius(r))
print(sorted(rs))
from collections import Counter

# print(Counter(rs))
# print(max(res['response'].items(), key=lambda x: x[1]))

print('Done, enjoy!')
