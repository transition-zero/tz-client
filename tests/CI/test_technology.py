import pytest

from feo.client import Record, RecordCollection, Technology


@pytest.fixture
def technology():
    return Technology.from_id("coal")


def test_technology_init(technology):
    assert isinstance(technology, Technology)
    assert technology.id == "coal"


def test_technology_search():
    technologies = Technology.search()
    assert isinstance(technologies, list)
    assert isinstance(technologies[0], Technology)


def test_technology_str(technology):
    assert str(technology) == "Technology: Coal (id=coal)"


def test_technology_children(technology):
    assert isinstance(technology.children, list)


def test_technology_parents(technology):
    assert isinstance(technology.parents, list)


def test_technology_projections():
    gas_combined_cycle = Technology.from_id("combined-cycle-gas-turbine")
    assert isinstance(gas_combined_cycle.projections, RecordCollection)
    assert len(gas_combined_cycle.projections) > 0
    record = gas_combined_cycle.projections.iloc[0].to_records()
    assert isinstance(record, Record)


def test_technology_delete(technology):
    technology.delete()
    assert Technology.from_id("coal") is None
