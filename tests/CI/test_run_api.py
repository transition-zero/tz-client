from feo.client import api


def test_run_api():
    runs = api.runs.get()
    assert isinstance(runs, list)
    assert isinstance(runs[0], api.schemas.Run)
