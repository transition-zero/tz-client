from tests.CI.test_run import run_fixture  # flake8: noqa # noqa: F401
from tz.client import Job
from tz.client.api.generated_schema import JobCreate


def test_job_create_and_delete(run_fixture):  # noqa: F811
    slug = "test_job_create_and_delete-some-job-slug"

    some_job = JobCreate(
        slug=slug,
        run=run_fixture.fullslug,
        submit_job=False,
    )

    job = Job.create(some_job)
    assert job.slug == slug

    response = Job.delete(uuid=job.uuid)
    assert response.objects_deleted == 1, response.message
