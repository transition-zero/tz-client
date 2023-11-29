import pytest

from feo.client import RecordCollection, Technology


@pytest.mark.skip(reason="missing tech data")
def test_technology_init():
    technology = Technology.from_id("coal")
    assert isinstance(technology, Technology)
    assert technology.id == "coal"


@pytest.mark.skip(reason="missing tech data")
def test_technology_search():
    technologies = Technology.search()
    assert isinstance(technologies, list)
    assert isinstance(technologies[0], Technology)


@pytest.mark.skip(reason="missing tech data")
def test_technology_projections():
    technology = Technology.from_id("coal")
    projections = technology.projections
    assert isinstance(projections, RecordCollection)


def test_technology_str():
    technology = Technology.from_id("coal")
    assert str(technology) == "Technology: Coal (id=coal)"
