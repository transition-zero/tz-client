from tz.client import api

# Note: Removing this for now. See ENG-845.
# if utils.ENVIRONMENT == "staging":
#     EXAMPLE_SCENARIO = "feo-global-indonesia:feo-indonesia-current-policies"
# elif utils.ENVIRONMENT == "production":
#     EXAMPLE_SCENARIO = "feo-global-indonesia:net-zero-2060"


def test_scenario_search():
    scenarios = api.model_scenarios.search()
    assert isinstance(scenarios, list)
    assert isinstance(scenarios[0], api.generated_schema.ModelScenario)


def test_scenario_get():
    scenario = api.model_scenarios.get(
        owner="admin|sample", model_slug="feo-indonesia", model_scenario_slug="baseline"
    )
    assert isinstance(scenario, api.generated_schema.ModelScenario)
