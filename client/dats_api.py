import json

from .api import API
import requests
from urllib.parse import urljoin


class DatsArtHttpAPI(API):
    def __init__(self, base_url, session: requests.Session):
        self._session = session
        self._base_url = base_url

    def exec(self, path: str, data: any = None):
        url = urljoin(self._base_url, path)

        data = data or {}
        new_data = {}
        for k, v in data.items():
            if isinstance(v, dict):
                for kk in v:
                    new_data[f'{k}[{kk}]'] = data[k][kk]
            else:
                new_data[k] = data[k]

        files = {key: (None, str(new_data[key])) for key in new_data}
        response = self._session.post(url, files=files)

        return response.json()


class DatsArtHttpJsonAPI(API):
    def __init__(self, base_url, session: requests.Session):
        self._session = session
        self._base_url = base_url

    def exec(self, path: str, data: any = None):
        url = urljoin(self._base_url, path)

        data = data or {}
        response = self._session.post(url, json.dumps(data))

        return response.json()

