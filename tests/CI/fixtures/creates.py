import pytest

from tz.client import Job, Model, ModelScenario, Run
# fmt: off
from tz.client.api.generated_schema import (JobCreate, ModelCreate,
                                            ModelScenarioCreate, RunCreate)


@pytest.fixture
def new_model():
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

    yield model

    response = Model.delete(model.owner, model.slug)
    assert response.objects_deleted == 1, response.message


@pytest.fixture
def new_model_scenario(new_model):
    slug = "test_model_create_and_delete-some-model-scenario-slug"
    some_model_scenario = ModelScenarioCreate(
        slug=slug,
        public=True,
        name="name",
        description="A test model scenario",
        model=f"{new_model.owner}:{new_model.slug}",
    )

    model_scenario = ModelScenario.create(model_scenario=some_model_scenario)
    assert model_scenario.slug == slug
    yield model_scenario

    response = ModelScenario.delete(
        owner=model_scenario.owner, model_slug=new_model.slug, slug=model_scenario.slug
    )
    assert response.objects_deleted == 1, response.message


@pytest.fixture
def new_run(new_model_scenario):
    slug = "test_run_create_and_delete-some-run-slug"

    model_slug = new_model_scenario.model.fullslug
    model_scenario_slug = new_model_scenario.fullslug

    some_run = RunCreate(
        slug=slug,
        public=True,
        name="name",
        description="A test run",
        model=model_slug,
        model_scenario=model_scenario_slug,
        runtime_estimate_hours=0.05,
        # Skip the runspec, as that requires a bit more service coordination.
        skip_build_runspec=True,
    )

    run = Run.create(some_run)
    assert run.slug == slug

    yield run

    response = Run.delete(
        owner=run.owner,
        model_slug=run.model,
        model_scenario_slug=new_model_scenario.slug,
        slug=run.slug,
    )
    assert response.objects_deleted == 1, response.message


@pytest.fixture
def new_job(new_run):
    slug = "test_job_create_and_delete-some-job-slug"

    some_job = JobCreate(
        slug=slug,
        run=new_run.fullslug,
        submit_job=False,
    )

    job = Job.create(some_job)
    assert job.slug == slug

    yield job

    response = Job.delete(uuid=job.uuid)
    assert response.objects_deleted == 1, response.message
