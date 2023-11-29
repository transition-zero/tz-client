from feo.client import Model, Scenario


def test_model_init():
    model = Model.from_id("feo-global-indonesia")
    assert isinstance(model, Model)
    assert model.id == "feo-global-indonesia"


def test_model_search():
    models = Model.search()
    assert isinstance(models, list)
    assert isinstance(models[0], Model)


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
    model = Model.from_id("feo-global-indonesia")
    scenarios = model.scenarios
    print(scenarios[0])
    assert isinstance(scenarios, list)
    assert isinstance(scenarios[0], Scenario)

    assert isinstance(model.featured_scenario, Scenario | None)


def test_model_str():
    model = Model.from_id("feo-global-indonesia")
    assert str(model) == "Model: FEO-Global Indonesia (id=feo-global-indonesia)"
