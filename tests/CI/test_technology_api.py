from feo.client import api

EXAMPLE_TECHNOLOGY = "coal"


def test_technology_search():
    technologies = api.technologies.search()
    assert isinstance(technologies, list)
    assert isinstance(technologies[0], api.schemas.Technology)


def test_model_get():
    models = api.technologies.get(EXAMPLE_TECHNOLOGY)
    assert isinstance(models, api.schemas.Technology)
