from abc import ABC

from .client import client


class BaseAPI(ABC):
    client = client
