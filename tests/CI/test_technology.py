import pytest

from feo.client import Technology


@pytest.mark.in_dev
def test_technology_init():
    technology = Technology.from_id("coal")
    assert isinstance(technology, Technology)
    assert technology.id == "coal"


@pytest.mark.in_dev
def test_technology_search():
    technologies = Technology.search()
    assert isinstance(technologies, list)
    assert isinstance(technologies[0], Technology)
