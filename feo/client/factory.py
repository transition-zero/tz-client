import feo.client.model as _model
import feo.client.run as _run
import feo.client.scenario as _scenario


def scenario(**kwargs):
    return _scenario.Scenario(**kwargs)


def model(**kwargs):
    return _model.Model(**kwargs)


def run(**kwargs):
    return _run.Run(**kwargs)
