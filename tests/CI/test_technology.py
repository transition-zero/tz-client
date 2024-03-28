import pytest

from tz.client import Record, RecordCollection, Technology


@pytest.fixture
def technology():
    return Technology.from_slug("wind")


def test_technology_init(technology):
    assert isinstance(technology, Technology)
    assert technology.slug == "wind"


def test_technology_search():
    technologies = Technology.search()
    assert isinstance(technologies, list)
    assert isinstance(technologies[0], Technology)


def test_technology_str(technology):
    assert str(technology) == "Technology: WIND (slug=wind)"


def test_technology_children(technology):
    assert isinstance(technology.children, list)
    assert all([isinstance(child, Technology) for child in technology.children])


def test_technology_parents(technology):
    assert isinstance(technology.parents, list)
    assert all([isinstance(parent, Technology) for parent in technology.parents])


@pytest.mark.xfail(reason="v2 migration wip (perhaps also not needed)")
def test_technology_projections():
    gas_combined_cycle = Technology.from_id("combined-cycle-gas-turbine")
    assert isinstance(gas_combined_cycle.projections, RecordCollection)
    assert len(gas_combined_cycle.projections) > 0
    record = gas_combined_cycle.projections.iloc[0].to_records()
    assert isinstance(record, Record)
