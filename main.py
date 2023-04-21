import time

from client import Client
from client.mock_api import MockAPI
from client.api import PrefixAPI
from client.dats_api import DatsArtHttpAPI
from requests import Session

token = '643ef1557ac24643ef1557ac25'
session = Session()
session.headers.update({'Authorization': f'Bearer {token}'})

api = PrefixAPI('/art', DatsArtHttpAPI('http://api.datsart.dats.team/', session))
client = Client(api)


def check(ah, av, power, color, amount):
    res = client.ballista.shoot(ah, av, power, {color: amount})
    time.sleep(0.5)
    return client.stage.info()['response']['stats']['shootsMisses']

# print(max(res['response'].items(), key=lambda x: x[1]))
print(res)
print('Done, enjoy!')



