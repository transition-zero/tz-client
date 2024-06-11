import pytest

from tz.client import ModelScenario, Run
from tz.client.api.generated_schema import RunCreate


@pytest.fixture
def run_fixture(username):
    run_result = Run.from_fullslug(f"{username}:feo-indonesia:net-zero-2060:run1")
    return run_result


def test_run_create_and_delete(run_fixture):
    slug = "test_run_create_and_delete-some-run-slug"

    model_slug = run_fixture.model
    model_scenario_slug = run_fixture.model_scenario.fullslug

    some_run = RunCreate(
        slug=slug,
        public=True,
        name="name",
        description="A test model scenario",
        # A minor hack: Just use the model that we at least succesfully found
        # above as the one that our scenario depends on. Then we don't have to
        # make a new one for ourselves.
        model=model_slug,
        model_scenario=model_scenario_slug,
        # Skip the runspec, as that requires a bit more service coordination.
        skip_build_runspec=True,
    )

    run = Run.create(some_run)
    assert run.slug == slug

    response = Run.delete(
        owner=run.owner,
        model_slug=run.model,
        model_scenario_slug=run.model_scenario.slug,
        slug=run.slug,
    )
    assert response.objects_deleted == 1, response.message


@pytest.fixture
def run_fixture_with_chart_data():
    # TODO: Implement!
    run_result = Run.from_fullslug(...)
    return run_result


def test_run_init(run_fixture):
    assert isinstance(run_fixture, Run)


def test_run_search():
    runs = Run.search()
    assert isinstance(runs, list)
    assert isinstance(runs[0], Run)


def test_search_pagination():
    PAGE_LIMIT = 2
    items1 = Run.search(limit=PAGE_LIMIT, page=0)
    assert len(items1) <= PAGE_LIMIT
    items2 = Run.search(limit=PAGE_LIMIT, page=1)
    assert len(items2) <= PAGE_LIMIT

    # assert that no items are returned when page number is too high
    items_bad = Run.search(limit=PAGE_LIMIT, page=10000)
    assert len(items_bad) == 0

    ids1 = {item.fullslug for item in items1}
    ids2 = {item.fullslug for item in items2}

    # assert that items on different pages are all different
    assert ids1.intersection(ids2) == set()


def test_run_model_scenario(run_fixture):
    model_scenario = run_fixture.model_scenario
    assert isinstance(model_scenario, ModelScenario)
    assert model_scenario.slug == "net-zero-2060"


def test_run_str(run_fixture, username):
    output = f"Run: Run 1 (fullslug={username}:feo-indonesia:net-zero-2060:run1)"
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
