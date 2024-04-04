import pytest

from tz.client import Model, ModelScenario


def test_model_init():
    model = Model.from_fullslug("me:feo-indonesia")
    assert isinstance(model, Model)
    assert model.slug == "feo-indonesia"


def test_model_search():
    models = Model.search()
    assert isinstance(models, list)
    assert isinstance(models[0], Model)


@pytest.mark.xfail(reason="v2 migration wip")
def test_search_pagination():
    PAGE_LIMIT = 1
    items1 = Model.search(limit=PAGE_LIMIT, page=0)
    assert len(items1) == PAGE_LIMIT
    items2 = Model.search(limit=PAGE_LIMIT, page=1)
    assert len(items2) == PAGE_LIMIT

    # assert that no items are returned when page number is too high
    items_bad = Model.search(limit=PAGE_LIMIT, page=10000)
    assert len(items_bad) == 0

    ids1 = {item.id for item in items1}
    ids2 = {item.id for item in items2}
    # assert that items on different pages are all different
    assert ids1.intersection(ids2) == set()


def test_model_scenarios():
    model = Model.from_slug(owner="me", model_slug="feo-indonesia")
    scenarios = model.model_scenarios

    assert isinstance(scenarios, list)
    assert isinstance(scenarios[0], ModelScenario)
    assert isinstance(model.featured_scenario, ModelScenario | None)


def test_model_str():
    model = Model.from_slug(owner="me", model_slug="feo-indonesia")
    assert str(model) == "Model: Indonesia Power Grid (id=feo-indonesia)"

    # Note: Removing this for now. See ENG-845.
    #
    # if utils.ENVIRONMENT == "staging":
    #     output = "Model: FEO-Global Indonesia (id=feo-global-indonesia)"
    # elif utils.ENVIRONMENT == "production":
    #     output = "Model: Indonesia JETP (id=feo-global-indonesia)"
    # assert str(model) == output
