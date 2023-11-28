from feo.client import publisher as _publisher
from feo.client import source as _source


def source(**kwargs):
    return _source.Source(**kwargs)


def publisher(**kwargs):
    return _publisher.Publisher(**kwargs)
