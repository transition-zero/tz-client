from typing import TYPE_CHECKING, List, Optional

from feo.client import api, factory
from feo.client.api import schemas

if TYPE_CHECKING:
    from feo.client.scenario import Scenario


class Model(schemas.ModelBase):
    @classmethod
    def from_id(cls, id: str) -> "Model":
        """
        Initialize the Model object from an ID.

        Args:
            id (str): A model ID, e.g. `feo-global-indonesia`.

        Returns:
            Model: A Model object.
        """
        model = api.models.get(slug=id)
        return cls(**model.model_dump())

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
    ) -> List["Model"]:
        """
        Search for models.

        Args:
            model_slug (str | None): The target model slug to search.
            includes (str | None): Related resources to be included in the search result.
            owner (str | None): The owner of the models to filter.
            sort (str | None): The sorting criteria for the search result.
            featured (bool | None): Filter models by featured status.
            public (bool | None): Filter models by public status.
            limit (int): The maximum number of search results to return per page.
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

    @property
    def id(self) -> str:
        """The ID of the model."""
        return self.slug

    @property
    def scenarios(self) -> list["Scenario"]:
        """A collection of scenarios associated with this model."""
        model_data = api.models.get(slug=self.id, includes="scenarios")
        if model_data.scenarios is None:
            return []
        return [factory.scenario(**s.model_dump()) for s in model_data.scenarios]

    @property
    def featured_scenario(self) -> Optional["Scenario"]:
        """The featured scenario associated with this model."""
        model_data = api.models.get(slug=self.id, includes="featured_scenario")
        if model_data.featured_scenario is None:
            return None
        return factory.scenario(**model_data.featured_scenario.model_dump())

    def __str__(self) -> str:
        return f"Model: {self.name} (id={self.id})"
