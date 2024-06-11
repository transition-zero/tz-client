from uuid import UUID

from tz.client.api.base import BaseAPI
# fmt: off
from tz.client.api.generated_schema import DeleteResponse, Job, JobCreate


class JobAPI(BaseAPI):
    def create(self, job: JobCreate) -> Job:
        resp = self.client.post("/jobs", json=job.model_dump())
        resp.raise_for_status()
        return Job(**resp.json())

    def delete(self, uuid: UUID) -> DeleteResponse:
        resp = self.client.delete(f"/jobs/{uuid}")
        resp.raise_for_status()
        return DeleteResponse(**resp.json())
