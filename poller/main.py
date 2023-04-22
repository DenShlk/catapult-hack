import random

from requests import Session

from client.api import PrefixAPI
from client.client import Factory, Client
from client.dats_api import DatsArtHttpAPI
import time

from model.color import Color
from poller.color_bank import ColorBank


class ColorPoller:
    def __init__(self, factory: Factory, color_bank: ColorBank):
        self.factory = factory
        self.color_bank = color_bank

    def run(self):
        while True:
            print('Generating...')
            data = self.factory.generate()
            if not data['success']:
                print('Failed to pick:', data)
                time.sleep(2)
                continue

            options = data['response']
            _id = self.color_bank.choose(options)
            result = self.factory.pick(_id, data['info']['tick'])

            if not result['success']:
                print('Failed to pick:', result)
                time.sleep(2)
                continue
            print('Picked:', Color(data['response'][_id]['color']).rgb())

            time_to_sleep = result['info']['ns'] * 10 ** -9
            time.sleep(time_to_sleep + 0.01)


if __name__ == '__main__':
    token = '643ef1557ac24643ef1557ac25'
    session = Session()
    session.headers.update({'Authorization': f'Bearer {token}'})

    api = PrefixAPI('/art', DatsArtHttpAPI('http://api.datsart.dats.team/', session))
    client = Client(api)
    # {Color(55, 59, 91): 56500, Color(255, 114, 0): 7500, Color(0, 4, 0): 100},
    poller = ColorPoller(client.factory, ColorBank({Color(255,0, 0):51000, Color(200, 200,200):20000,},
                                                   {int(c):v for c, v in client.colors.list()['response'].items()}))
    print(poller.run())
