from typing import List

from pydantic import root_validator

from feo.client import api
from feo.client.api import schemas


class Model(schemas.Model):
    def __init__(self, slug: str, **kwargs):
        """
        Initialize the Model object.

        Args:
            slug (str): A model ID slug, e.g. `feo-global-indonesia`.
            **kwargs: Additional keyword arguments to be passed to the parent class.
        """
        super(self.__class__, self).__init__(slug=slug, **kwargs)

    @classmethod
    def search(
        cls,
        model_slug: str | None = None,
        includes: str | None = None,
        owner: str | None = None,
        sort: str | None = None,
        featured: bool | None = None,
        public: bool | None = None,
        limit: int = 10,
        page: int = 0,
    ) -> List["schemas.Model"]:
        """
        Search for models.

        Args:
            model_slug (str | None): The target model slug to search.
            includes (str | None): The included fields in the search result.
            owner (str | None): The owner of the models to filter.
            sort (str | None): The sorting criteria for the search result.
            featured (bool | None): Filter models by featured status.
            public (bool | None): Filter models by public status.
            limit (int): The maximum number of search results to return.
            page (int): The page number of search results to return.

        Returns:
            List[Model]: A list of Model objects.
        """

        search_results = api.models.search(
            model_slug=model_slug,
            includes=includes,
            owner=owner,
            sort=sort,
            featured=featured,
            public=public,
            limit=limit,
            page=page,
        )

        return [cls(**model.model_dump()) for model in search_results]

    @root_validator(pre=True)
    def maybe_initialise_from_api(cls, values):
        slug = values.get("slug")

        if slug is not None:
            # call from API
            model = api.models.get(slug=slug)

            for key, val in model.model_dump().items():
                values[key] = val

            return values

        return values
