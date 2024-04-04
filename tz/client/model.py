from typing import List, Optional

from tz.client import api
from tz.client.api import generated_schema
from tz.client.model_scenario import ModelScenario
# fmt: off
from tz.client.utils import (lazy_load_relationship,
                             lazy_load_single_relationship)


class Model(generated_schema.Model):
    _model_scenarios: list[ModelScenario] | None = None
    _featured_scenario: Optional[ModelScenario] | None = None

    @classmethod
    def from_slug(cls, model_slug: str, owner: str) -> "Model":
        """
        Initialize the Model object from a slug.

        Args:
            model_slug (str): A model slug, e.g. `feo-global-indonesia`.
            owner (str): A username, e.g. `me`.

        Returns:
            Model: A Model object.
        """
        model = api.models.get(owner=owner, model_slug=model_slug)
        return cls(**model.model_dump())

    @classmethod
    def search(
        cls,
        slug: str | None = None,
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
            slug (str | None): The target model slug to search.
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
            slug=slug,
            includes=includes,
            owner=owner,
            sort=sort,
            featured=featured,
            public=public,
            limit=limit,
            page=page,
        )

        return [cls(**model.model_dump()) for model in search_results]

    def __str__(self) -> str:
        return f"Model: {self.name} (id={self.slug})"


lazy_load_relationship(
    Model,
    ModelScenario,
    "model_scenarios",
    lambda self: api.models.get(owner=self.owner, model_slug=self.slug, includes="model_scenarios"),
)


lazy_load_single_relationship(
    Model,
    "ModelScenario",
    "featured_scenario",
    lambda self: api.models.get(
        owner=self.owner,
        model_slug=self.slug,
        includes="featured_scenario",
    ),
)
