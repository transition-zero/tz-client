from feo.client import Scenario


def test_scenario_init():
    scenario = Scenario.from_id("feo-global-indonesia:feo-indonesia-current-policies")
    assert isinstance(scenario, Scenario)
    assert scenario.id == "feo-global-indonesia:feo-indonesia-current-policies"


def test_scenario_search():
    scenarios = Scenario.search()
    assert isinstance(scenarios, list)
    assert isinstance(scenarios[0], Scenario)
