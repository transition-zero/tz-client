from feo.client import model as _model
from feo.client import publisher as _publisher
from feo.client import run as _run
from feo.client import scenario as _scenario
from feo.client import source as _source


def model(**kwargs):
    return _model.Model(**kwargs)


def publisher(**kwargs):
    return _publisher.Publisher(**kwargs)


def run(**kwargs):
    return _run.Run(**kwargs)


def scenario(**kwargs):
    return _scenario.Scenario(**kwargs)


def source(**kwargs):
    return _source.Source(**kwargs)
