import pytest

from tz.client import Model, ModelScenario
from tz.client.api.generated_schema import ModelCreate


@pytest.fixture()
def model(username):
    return Model.from_fullslug(f"{username}:feo-indonesia")


def test_model_create_and_delete():
    slug = "test_model_create_and_delete-some-model-slug"
    some_model = ModelCreate(
        slug=slug,
        public=True,
        name="name",
        description="A test model",
        version="test",
        start_year=2021,
        end_year=2050,
        nodes=["GBR"],
        commodities=["electricity"],
        technologies=["battery", "coal", "combined-cycle", "photovoltaic"],
    )
    model = Model.create(model=some_model)
    assert model.slug == slug

    response = Model.delete(model.owner, model.slug)
    assert response.objects_deleted == 1, response.message


def test_model_init(model):
    assert isinstance(model, Model)
    assert model.slug == "feo-indonesia"


def test_model_search():
    models = Model.search()
    assert isinstance(models, list)
    assert isinstance(models[0], Model)


def test_model_search_pagination():
    PAGE_LIMIT = 1
    items1 = Model.search(limit=PAGE_LIMIT, page=0)
    assert len(items1) <= PAGE_LIMIT
    items2 = Model.search(limit=PAGE_LIMIT, page=1)
    assert len(items2) <= PAGE_LIMIT

    # assert that no items are returned when page number is too high
    items_bad = Model.search(limit=PAGE_LIMIT, page=10000)
    assert len(items_bad) == 0

    ids1 = {item.slug for item in items1}
    ids2 = {item.slug for item in items2}
    # assert that items on different pages are all different
    assert ids1.intersection(ids2) == set()


def test_model_scenarios(model):
    scenarios = model.model_scenarios

    assert isinstance(scenarios, list)
    assert isinstance(scenarios[0], ModelScenario)
    assert isinstance(model.featured_scenario, ModelScenario | None)


def test_model_str(username, model):
    assert str(model) == f"Model: Indonesia Power Grid (fullslug={username}:feo-indonesia)"
