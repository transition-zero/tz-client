import pytest

from tz.client import Model, ModelScenario, Run


@pytest.fixture
def scenario(username):
    scenario = ModelScenario.from_fullslug(f"{username}:feo-indonesia:net-zero-2060")
    return scenario


def test_model_scenario_init(scenario):
    assert isinstance(scenario, ModelScenario)


def test_model_scenario_search():
    scenarios = ModelScenario.search()
    assert isinstance(scenarios, list)
    assert isinstance(scenarios[0], ModelScenario)


def test_model_scenario_search_pagination():
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
    assert isinstance(scenario.model, Model)
    assert scenario.model.slug == "feo-indonesia"


def test_model_scenario_featured_run(scenario):
    assert isinstance(scenario.featured_run, Run)
    assert scenario.featured_run.slug == "run1"


def test_model_scenario_str(scenario):
    assert str(scenario) == "ModelScenario: Net Zero 2060 (id=feo-indonesia:net-zero-2060)"
