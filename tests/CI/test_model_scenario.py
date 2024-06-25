import pytest

from tz.client import Model, ModelScenario, Run


@pytest.fixture
def scenario(username):
    scenario = ModelScenario.from_fullslug(f"{username}:feo-indonesia:net-zero-2060")
    return scenario


def test_model_scenario_create_and_delete(new_model_scenario):
    assert new_model_scenario  # We really care about the fixture running


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

    ids1 = {item.fullslug for item in items1}
    ids2 = {item.fullslug for item in items2}

    # assert that items on different pages are all different
    assert ids1.intersection(ids2) == set()

    # assert that no items are returned when page number is too high
    items_bad = ModelScenario.search(limit=PAGE_LIMIT, page=10000)
    assert len(items_bad) == 0


def test_model_scenario_model(scenario):
    assert isinstance(scenario.model, Model)
    assert scenario.model.slug == "feo-indonesia"


def test_model_scenario_runs(scenario):
    assert isinstance(scenario.runs, list)
    assert isinstance(scenario.runs[0], Run)


def test_model_scenario_featured_run(scenario):
    assert isinstance(scenario.featured_run, Run)
    assert scenario.featured_run.slug == "run1"


def test_model_scenario_str(username, scenario):
    assert (
        str(scenario)
        == f"ModelScenario: Net Zero 2060 (fullslug={username}:feo-indonesia:net-zero-2060)"
    )
