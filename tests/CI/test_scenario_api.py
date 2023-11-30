from feo.client import api, utils

if utils.ENVIRONMENT == "staging":
    EXAMPLE_SCENARIO = "feo-global-indonesia:feo-indonesia-current-policies"
elif utils.ENVIRONMENT == "production":
    EXAMPLE_SCENARIO = "feo-global-indonesia:net-zero-2060"


def test_scenario_search():
    scenarios = api.scenarios.search()
    assert isinstance(scenarios, list)
    assert isinstance(scenarios[0], api.schemas.Scenario)


def test_scenario_get():
    scenario = api.scenarios.get(EXAMPLE_SCENARIO)
    assert isinstance(scenario, api.schemas.Scenario)
