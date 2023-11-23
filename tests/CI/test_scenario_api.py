from feo.client import api


def test_scenario_api():
    scenarios = api.scenarios.get()
    assert isinstance(scenarios, list)
    assert isinstance(scenarios[0], api.schemas.Scenario)
