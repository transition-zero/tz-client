from feo.client import Record, RecordCollection, Technology


def test_technology_init():
    technology = Technology.from_id("coal")
    assert isinstance(technology, Technology)
    assert technology.id == "coal"


def test_technology_search():
    technologies = Technology.search()
    assert isinstance(technologies, list)
    assert isinstance(technologies[0], Technology)


def test_technology_str():
    technology = Technology.from_id("coal")
    assert str(technology) == "Technology: Coal (id=coal)"


def test_technology_projections():
    gas_combined_cycle = Technology.from_id("combined-cycle-gas-turbine")
    assert isinstance(gas_combined_cycle.projections, RecordCollection)
    assert len(gas_combined_cycle.projections) > 0
    print(gas_combined_cycle.projections.valid_timestamp_start)
    after_2040 = gas_combined_cycle.projections.loc[
        gas_combined_cycle.projections.valid_timestamp_start > "2030-01-01"
    ]
    assert len(after_2040) > 0

    record = gas_combined_cycle.projections.iloc[0].to_records()
    assert isinstance(record, Record)
