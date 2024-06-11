from uuid import UUID

from tz.client import api
from tz.client.api import generated_schema


class Job(generated_schema.Job):
    @classmethod
    def create(cls, job: generated_schema.JobCreate) -> "Job":
        result = api.jobs.create(job)
        return cls(**result.model_dump())

    @classmethod
    def delete(cls, uuid: UUID) -> generated_schema.DeleteResponse:
        result = api.jobs.delete(uuid=uuid)
        return generated_schema.DeleteResponse(**result.model_dump())
