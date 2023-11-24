from feo.client import Model


def test_model_init():
    model = Model.from_id("feo-global-indonesia")
    assert isinstance(model, Model)
    assert model.id == "feo-global-indonesia"


def test_model_search():
    models = Model.search()
    assert isinstance(models, list)
    assert isinstance(models[0], Model)
