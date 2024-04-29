from tz.client import api


def test_model_scenario_search():
    scenarios = api.model_scenarios.search()
    assert isinstance(scenarios, list)
    assert isinstance(scenarios[0], api.generated_schema.ModelScenario)


def test_model_scenario_get():
    scenario = api.model_scenarios.get(
        owner="feo-core-admin", model_slug="feo-indonesia", model_scenario_slug="net-zero-2060"
    )
    assert isinstance(scenario, api.generated_schema.ModelScenario)
