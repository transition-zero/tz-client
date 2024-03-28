import pytest

from tz.client import api

EXAMPLE_MODEL = "feo-global-indonesia"


@pytest.mark.xfail(reason="v2 migration wip")
def test_model_search():
    models = api.models.search()
    assert isinstance(models, list)
    assert isinstance(models[0], api.schemas.Model)


@pytest.mark.xfail(reason="v2 migration wip")
def test_model_get():
    models = api.models.get(EXAMPLE_MODEL)
    assert isinstance(models, api.schemas.Model)
