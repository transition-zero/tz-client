import pytest

from tz.client import Model, Run, utils


@pytest.fixture
def run_fixture():
    if utils.ENVIRONMENT == "staging":
        run_result = Run.from_id("feo-global-indonesia:feo-indonesia-current-policies:demo")
    elif utils.ENVIRONMENT == "production":
        run_result = Run.from_id("feo-global-indonesia:net-zero-2060:main")
    else:
        raise ValueError("Unknown environment")
    return run_result


@pytest.fixture
def run_fixture_with_chart_data():
    if utils.ENVIRONMENT == "staging":
        run_result = Run.from_id("feo-global-indonesia:feo-indonesia-current-policies:demo")
    elif utils.ENVIRONMENT == "production":
        run_result = Run.from_id("feo-global-indonesia:baseline:main")
    else:
        raise ValueError("Unknown environment")
    return run_result


@pytest.mark.xfail(reason="v2 migration wip")
def test_run_init(run_fixture):
    assert isinstance(run_fixture, Run)


@pytest.mark.xfail(reason="v2 migration wip")
def test_run_search():
    runs = Run.search()
    assert isinstance(runs, list)
    assert isinstance(runs[0], Run)


@pytest.mark.xfail(reason="v2 migration wip")
def test_search_pagination():
    PAGE_LIMIT = 2
    items1 = Run.search(limit=PAGE_LIMIT, page=0)
    assert len(items1) == PAGE_LIMIT
    items2 = Run.search(limit=PAGE_LIMIT, page=1)
    assert len(items2) == PAGE_LIMIT

    # assert that no items are returned when page number is too high
    items_bad = Run.search(limit=PAGE_LIMIT, page=10000)
    assert len(items_bad) == 0

    ids1 = {item.id for item in items1}
    ids2 = {item.id for item in items2}
    # assert that items on different pages are all different
    assert ids1.intersection(ids2) == set()


@pytest.mark.xfail(reason="v2 migration wip")
def test_run_model(run_fixture):
    model = run_fixture.model
    assert isinstance(model, Model)
    assert model.id == "feo-global-indonesia"


@pytest.mark.xfail(reason="v2 migration wip")
def test_run_str(run_fixture):
    if utils.ENVIRONMENT == "staging":
        output = "Run: demo (id=feo-global-indonesia:feo-indonesia-current-policies:demo)"
    elif utils.ENVIRONMENT == "production":
        output = "Run: main (id=feo-global-indonesia:net-zero-2060:main)"
    else:
        raise ValueError("Unknown environment")
    assert str(run_fixture) == output


@pytest.mark.xfail(reason="v2 migration wip")
def test_results_node_collection_capacities(run_fixture_with_chart_data):
    # structure should be:
    # node_id, technology_type, year, value
    #   IDN-AC     BAT           2047  1.87
    #   BIO        BIO           2047  1.86
    columns = ["node_id", "technology_type", "timestamp", "value"]
    assert [c for c in run_fixture_with_chart_data.results.node_capacity.columns] == columns
    assert len(run_fixture_with_chart_data.results.node_capacity) > 0


@pytest.mark.xfail(reason="v2 migration wip")
def test_results_edge_collection_capacities(run_fixture_with_chart_data):
    # structure should be:
    # node_id, technology_type,  year, value, commodity,
    #   IDN-AC     BAT           2047  1.87     ELEC
    #   BIO        BIO           2047  1.86     ELEC
    columns = ["node_id", "technology_type", "timestamp", "value", "commodity"]
    assert [c for c in run_fixture_with_chart_data.results.edge_capacity.columns] == columns
    assert len(run_fixture_with_chart_data.results.edge_capacity) > 0


@pytest.mark.xfail(reason="v2 migration wip")
def test_results_collection_production(run_fixture_with_chart_data):
    # structure should be:
    # node,   technology, commodity, year, value,
    # IDN-AC  BAT         ELEC       2046  36.499
    columns = ["node", "technology", "commodity", "year", "value"]
    assert [c for c in run_fixture_with_chart_data.results.production.columns] == columns
    assert len(run_fixture_with_chart_data.results.production) > 0


@pytest.mark.xfail(reason="v2 migration wip")
def test_results_collection_flow(run_fixture_with_chart_data):
    # structure should be:
    # node,   technology, commodity, year, value,
    # IDN-AC  BAT         ELEC       2046  36.499
    columns = ["source_node", "target_node", "commodity", "flow_type", "year", "value"]
    assert [c for c in run_fixture_with_chart_data.results.flow.columns] == columns
    assert len(run_fixture_with_chart_data.results.flow) > 0
