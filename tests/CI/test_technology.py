from feo.client import RecordCollection, Technology


def test_technology_init():
    technology = Technology.from_id("coal")
    assert isinstance(technology, Technology)
    assert technology.id == "coal"


def test_technology_search():
    technologies = Technology.search()
    assert isinstance(technologies, list)
    assert isinstance(technologies[0], Technology)


def test_technology_projections():
    technology = Technology.from_id("coal")
    projections = technology.projections
    assert isinstance(projections, RecordCollection)
