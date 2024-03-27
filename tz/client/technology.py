from typing import ForwardRef, Optional

from tz.client import RecordCollection, api
from tz.client.api import generated_schema
from tz.client.utils import lazy_load_relationship


class Technology(generated_schema.Technology):

    """
    <!--
    The Technology class enables access to technology data.
    Technologies are related hierarchically to one another via their parents / children properties.
    -->

    Technologies can be loaded directly with their id:

    ```python
    coal = Technology.from_id("wind")
    ```

    """

    _projections: Optional[ForwardRef("RecordCollection")] = None  # type: ignore[valid-type]
    _children: Optional[list["Technology"]] = None
    _parents: Optional[list["Technology"]] = None

    @classmethod
    def from_slug(cls, slug: str) -> "Technology":
        """
        Initialize the Technology object from an ID.

        Args:
            id (str): A technology ID, e.g. `coal`.

        Returns:
            Technology: A Technology object.
        """
        technology = api.technologies.get(slug=slug)
        return cls(**technology.model_dump())

    @classmethod
    def search(
        cls,
        uuid: str | None = None,
        slug: str | None = None,
        name: str | None = None,
        owner_id: str | None = None,
        limit: int = 10,
        page: int = 0,
    ) -> list["Technology"]:
        """
        Search for technologies.

        Args:
            uuid (str | None): The target technology UUID to search.
            slug (str | None): The target technology slug to search.
            names (str | None): The target technology name to search.
            owner_id (str | None): The owner of the technologiess to filter.
            limit (int): The maximum number of search results to return.
            page (int): The page number of search results to return.

        Returns:
            List[Technology]: A list of Technology objects.
        """

        search_results = api.technologies.search(
            uuid=uuid,
            slug=slug,
            name=name,
            owner_id=owner_id,
            limit=limit,
            page=page,
        )

        return [cls(**technology.model_dump()) for technology in search_results]

    @property
    def projections(self):
        """The RecordCollection associated with the technoogy"""
        if self._projections is None:
            collection = RecordCollection()
            self._projections = collection.search(technology=self.slug)
        return self._projections

    def __str__(self) -> str:
        return f"Technology: {self.name} (slug={self.slug})"


lazy_load_relationship(
    Technology,
    "children",
    lambda self: api.technologies.get(slug=self.slug, includes="children"),
)

lazy_load_relationship(
    Technology,
    "parents",
    lambda self: api.technologies.get(slug=self.slug, includes="parents"),
)
