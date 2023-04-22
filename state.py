import json
import os


class State:
    def __init__(self, path='state.json'):
        self.path = path
        if not os.path.exists(path):
            self.state = self.default_state
            self.dump()
        self.load()
    def dump(self):
        with open(self.path, 'w') as f:
            json.dump(self.state, f)

    def load(self):
        with open(self.path, 'r') as f:
            self.state = json.load(f)

    @staticmethod
    def default_state():
        return {'done': []}