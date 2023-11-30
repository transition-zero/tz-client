import pytest

from feo.client import Model, Run, utils


@pytest.fixture
def run_fixture():
    if utils.ENVIRONMENT == "staging":
        run = Run.from_id("feo-global-indonesia:feo-indonesia-current-policies:demo")
    elif utils.ENVIRONMENT == "production":
        run = Run.from_id("feo-global-indonesia:net-zero-2060:main")
    else:
        raise ValueError("Unknown environment")
    return run


def test_run_init(run_fixture):
    run = run_fixture
    assert isinstance(run, Run)


def test_run_search():
    runs = Run.search()
    assert isinstance(runs, list)
    assert isinstance(runs[0], Run)


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


def test_run_model(run_fixture):
    run = run_fixture
    model = run.model
    assert isinstance(model, Model)
    assert model.id == "feo-global-indonesia"


def test_run_str(run_fixture):
    run = run_fixture
    if utils.ENVIRONMENT == "staging":
        output = "Run: demo (id=feo-global-indonesia:feo-indonesia-current-policies:demo)"
    elif utils.ENVIRONMENT == "production":
        output = "Run: main (id=feo-global-indonesia:net-zero-2060:main)"
    else:
        raise ValueError("Unknown environment")
    assert str(run) == output


def test_results_collection():
    net_zero_demo_run = Run.from_id("feo-global-indonesia:coal-retirement:main")
    assert net_zero_demo_run.results == RunResults(id="feo-global-indonesia:coal-retirement:main")
    assert type(net_zero_demo_run.results.node_capacity) == ResultsCollection
    assert type(net_zero_demo_run.results.edge_capacity) == ResultsCollection
    net_zero_demo_run.results.edge_capacity.filter(node_id="IDN", technology="coal")
    net_zero_demo_run.results.edge_capacity.next_page()
