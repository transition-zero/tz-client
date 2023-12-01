from .client import Client


class BaseAPI:
    def __init__(self):
        self.client = Client()
