class API:
    def exec(self, path: str, data: any = None):
        raise Exception('API is an interface!')


class MapAPI(API):
    def __init__(self, mapper, api: API):
        self.api = api
        self.mapper = mapper

    def exec(self, path: str, data: any = None):
        path, data = self.mapper(path, data)
        return self.api.exec(path, data)


class PrefixAPI(MapAPI):
    @staticmethod
    def _join_paths(p1: str, p2: str):
        parts1 = p1.split('/')
        parts2 = p2.split('/')
        all_parts = parts1 + parts2
        normalized_parts = list(filter(lambda part: len(part) > 0, map(lambda x: x.strip(), all_parts)))
        return '/' + '/'.join(normalized_parts)

    def __init__(self, prefix: str, api: API):
        super().__init__(
            lambda path, data: (PrefixAPI._join_paths(prefix, path), data),
            api,
        )
