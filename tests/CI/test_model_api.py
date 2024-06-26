from tz.client import api

EXAMPLE_MODEL = "feo-indonesia"


def test_model_search():
    models = api.models.search()
    assert isinstance(models, list)
    assert isinstance(models[0], api.generated_schema.Model)


def test_model_get(username):
    models = api.models.get(owner=username, model_slug=EXAMPLE_MODEL)
    assert isinstance(models, api.generated_schema.Model)
