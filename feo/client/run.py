from typing import List

from pydantic import root_validator

from feo.client import api
from feo.client.api import schemas


class Run(schemas.Run):
    def __init__(self, fullslug: str, **kwargs):
        """
        Initialize the Run object.

        Args:
            fullslug (str): A combination of the model slug, scenario slug and run slug
                separated by a colon, e.g. `model-slug:scenario-slug:run-slug`.
            **kwargs: Additional keyword arguments to be passed to the parent class.
        """
        super(self.__class__, self).__init__(fullslug=fullslug, **kwargs)

    @classmethod
    def search(
        cls,
        slug: str | None = None,
        model_slug: str | None = None,
        scenario_slug: str | None = None,
        owner_id: str | None = None,
        featured: bool | None = None,
        includes: str | None = None,
        public: bool | None = None,
        limit: int = 5,
        page: int = 0,
    ) -> List["Run"]:
        """
        Search for runs using various filters.

        Args:
            slug (str, optional): The slug of the run.
            model_slug (str, optional): The slug of the model.
            scenario_slug (str, optional): The slug of the scenario.
            owner_id (str, optional): The ID of the owner.
            featured (bool, optional): Whether the run is featured.
            includes (str, optional): Additional fields to include in the search results.
            public (bool, optional): Whether the run is public.
            limit (int, optional): The maximum number of runs to return. Default is 5.
            page (int, optional): The page number of the results. Default is 0.

        Returns:
            List[Run]: A list of Run objects.
        """

        search_results = api.runs.search(
            slug=slug,
            model_slug=model_slug,
            scenario_slug=scenario_slug,
            owner_id=owner_id,
            featured=featured,
            includes=includes,
            public=public,
            limit=limit,
            page=page,
        )

        return [cls(**run.model_dump()) for run in search_results]

    @root_validator(pre=True)
    def maybe_initialise_from_api(cls, values):
        slug = values.get("slug")
        if slug is not None:
            # call from API
            run = api.runs.get(slug)

            for key, val in run.model_dump().items():
                values[key] = val

            return values

        return values
