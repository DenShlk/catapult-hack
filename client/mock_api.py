from .api import API


class MockAPI(API):
    def exec(self, path: str, data: any = None):
        print(f'Getting: path=\'{path}\' data=\'{data}\'')
        return None
