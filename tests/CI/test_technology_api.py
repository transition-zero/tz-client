import pytest

from feo.client import api

EXAMPLE_TECHNOLOGY = "coal"


@pytest.mark.in_dev
def test_technology_search():
    technologies = api.technologies.search()
    assert isinstance(technologies, list)
    assert isinstance(technologies[0], api.schemas.Technology)


@pytest.mark.in_dev
def test_model_get():
    models = api.models.get(EXAMPLE_TECHNOLOGY)
    assert isinstance(models, api.schemas.Technology)
