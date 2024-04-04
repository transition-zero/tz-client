import pytest

from tz.client import Model, ModelScenario, Run


@pytest.fixture
def scenario():
    scenario = ModelScenario.from_slug(
        owner="me", model_slug="feo-indonesia", model_scenario_slug="baseline"
    )
    # Note: Removing this for now. See ENG-845.
    #
    # if utils.ENVIRONMENT == "staging":
    #     scenario = ModelScenario.from_id("feo-global-indonesia:feo-indonesia-current-policies")
    # elif utils.ENVIRONMENT == "production":
    #     scenario = ModelScenario.from_id("feo-global-indonesia:net-zero-2060")
    # else:
    #     raise ValueError("Unknown environment")
    return scenario


def test_model_scenario_init(scenario):
    assert isinstance(scenario, ModelScenario)


def test_model_scenario_search():
    scenarios = ModelScenario.search()
    assert isinstance(scenarios, list)
    assert isinstance(scenarios[0], ModelScenario)


def test_model_search_pagination():
    PAGE_LIMIT = 2
    items1 = ModelScenario.search(limit=PAGE_LIMIT, page=0)
    assert len(items1) <= PAGE_LIMIT
    items2 = ModelScenario.search(limit=PAGE_LIMIT, page=1)
    assert len(items2) <= PAGE_LIMIT

    # assert that no items are returned when page number is too high
    items_bad = ModelScenario.search(limit=PAGE_LIMIT, page=10000)
    assert len(items_bad) == 0

    ids1 = {item.id for item in items1}
    ids2 = {item.id for item in items2}
    # assert that items on different pages are all different
    assert ids1.intersection(ids2) == set()


def test_model_scenario_model(scenario):
    model = scenario.model
    assert isinstance(model, Model)
    assert model.slug == "feo-indonesia"


def test_model_scenario_featured_run(scenario):
    assert isinstance(scenario.featured_run, Run)
    assert scenario.featured_run.slug == "run1"


def test_model_scenario_str(scenario):
    assert str(scenario) == "ModelScenario: Current Policies (id=feo-indonesia:baseline)"
    # Note: Removing this for now. See ENG-845.
    # if utils.ENVIRONMENT == "staging":
    #     output = (
    #         "ModelScenario: FEO Indonesia - Current Policies "
    #         "(id=feo-global-indonesia:feo-indonesia-current-policies)"
    #     )
    # elif utils.ENVIRONMENT == "production":
    #     output = "ModelScenario: Net Zero 2060 (id=feo-global-indonesia:net-zero-2060)"
    # else:
    #     raise ValueError("Unknown environment")
    # assert str(scenario) == output
