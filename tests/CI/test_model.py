import pytest

from tz.client import Model, ModelScenario


@pytest.fixture()
def model(username):
    return Model.from_fullslug(f"{username}:feo-indonesia")


def test_model_init(model):
    assert isinstance(model, Model)
    assert model.slug == "feo-indonesia"


def test_model_search():
    models = Model.search()
    assert isinstance(models, list)
    assert isinstance(models[0], Model)


def test_model_search_pagination():
    PAGE_LIMIT = 1
    items1 = Model.search(limit=PAGE_LIMIT, page=0)
    assert len(items1) <= PAGE_LIMIT
    items2 = Model.search(limit=PAGE_LIMIT, page=1)
    assert len(items2) <= PAGE_LIMIT

    # assert that no items are returned when page number is too high
    items_bad = Model.search(limit=PAGE_LIMIT, page=10000)
    assert len(items_bad) == 0

    ids1 = {item.slug for item in items1}
    ids2 = {item.slug for item in items2}
    # assert that items on different pages are all different
    assert ids1.intersection(ids2) == set()


def test_model_scenarios(model):
    scenarios = model.model_scenarios

    assert isinstance(scenarios, list)
    assert isinstance(scenarios[0], ModelScenario)
    assert isinstance(model.featured_scenario, ModelScenario | None)


def test_model_str(model):
    assert str(model) == "Model: Indonesia Power Grid (slug=feo-indonesia)"
