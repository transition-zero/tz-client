from feo.client import Scenario


def test_scenario_init():
    scenarios = Scenario("feo-global-indonesia:feo-indonesia-current-policies")
    assert isinstance(scenarios, Scenario)


def test_scenario_search():
    scenarios = Scenario.search()
    assert isinstance(scenarios, list)
    assert isinstance(scenarios[0], Scenario)
