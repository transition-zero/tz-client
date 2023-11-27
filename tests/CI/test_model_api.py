from feo.client import api

EXAMPLE_MODEL = "feo-global-indonesia"


def test_model_search():
    models = api.models.search()
    assert isinstance(models, list)
    assert isinstance(models[0], api.schemas.Model)


def test_model_get():
    models = api.models.get(EXAMPLE_MODEL)
    assert isinstance(models, api.schemas.Model)
