from tz.client import model as _model
from tz.client import publisher as _publisher
from tz.client import run as _run
from tz.client import source as _source


def model(**kwargs):
    return _model.Model(**kwargs)


def publisher(**kwargs):
    return _publisher.Publisher(**kwargs)


def run(**kwargs):
    return _run.Run(**kwargs)


def source(**kwargs):
    return _source.Source(**kwargs)
