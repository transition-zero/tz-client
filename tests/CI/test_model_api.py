from feo.client import api


def test_model_api():
    models = api.models.get()
    assert isinstance(models, list)
    assert isinstance(models[0], api.schemas.Model)
