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
        files = {key: (None, data[key]) for key in data}
        response = self._session.post(url, files=files)

        return response.json()
