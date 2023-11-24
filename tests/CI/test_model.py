from feo.client import Model


def test_model_init():
    models = Model.from_id("feo-global-indonesia")
    assert isinstance(models, Model)


def test_model_search():
    models = Model.search()
    assert isinstance(models, list)
    assert isinstance(models[0], Model)
