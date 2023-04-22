import random

from requests import Session

from client.api import PrefixAPI
from client.client import Factory, Client
from client.dats_api import DatsArtHttpAPI
import time

from model.color import Color


class ColorPoller:
    def __init__(self, factory: Factory):
        self.factory = factory

    def run(self):
        while True:
            print('Generating...')
            data = self.factory.generate()
            if not data['success']:
                print('Failed to pick:', data)
                time.sleep(2)
                continue

            _id = random.choice(list(data['response'].keys()))
            result = self.factory.pick(_id, data['info']['tick'])

            if not result['success']:
                print('Failed to pick:', result)
                time.sleep(2)
                continue
            print('Picked:', Color(data['response'][_id]['color']).rgb())

            time_to_sleep = result['info']['ns'] * 10 ** -9
            time.sleep(time_to_sleep + 0.04)


if __name__ == '__main__':
    token = '643ef1557ac24643ef1557ac25'
    session = Session()
    session.headers.update({'Authorization': f'Bearer {token}'})

    api = PrefixAPI('/art', DatsArtHttpAPI('http://api.datsart.dats.team/', session))
    client = Client(api)

    poller = ColorPoller(client.factory)
    print(poller.run())
