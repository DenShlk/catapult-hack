import random

from requests import Session

from client.api import PrefixAPI
from client.client import Factory, Client
from client.dats_api import DatsArtHttpAPI


class ColorPoller:
    def __init__(self, factory: Factory):
        self.factory = factory

    def run(self):
        while True:
            data = self.factory.generate()
            _id = random.choice(list(data['response'].keys()))
            print(self.factory.pick(_id, data['info']['tick']))
            print('1')


if __name__ == '__main__':
    token = '643ef1557ac24643ef1557ac25'
    session = Session()
    session.headers.update({'Authorization': f'Bearer {token}'})

    api = PrefixAPI('/art', DatsArtHttpAPI('http://api.datsart.dats.team/', session))
    client = Client(api)

    poller = ColorPoller(client.factory)
    print(poller.run())
