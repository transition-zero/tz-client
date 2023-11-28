from feo.client import Model, Scenario


def test_model_init():
    model = Model.from_id("feo-global-indonesia")
    assert isinstance(model, Model)
    assert model.id == "feo-global-indonesia"


def test_model_search():
    models = Model.search()
    assert isinstance(models, list)
    assert isinstance(models[0], Model)


def test_model_scenarios():
    model = Model.from_id("feo-global-indonesia")
    scenarios = model.scenarios
    print(scenarios[0])
    assert isinstance(scenarios, list)
    assert isinstance(scenarios[0], Scenario)

    assert isinstance(model.featured_scenario, Scenario | None)
