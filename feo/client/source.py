from typing import TYPE_CHECKING, ForwardRef, Optional

from feo.client import api, factory
from feo.client.api import schemas
from feo.client.utils import parse_slug

if TYPE_CHECKING:
    from feo.client.publisher import Publisher


class Source(schemas.Source):

    """
    The Source class references data to open-access documents by third parties.
    Sources have a license, and can have multiple links to track the origin of data.
    Sources are affiliated with a Publisher, and have a publication date.

    """

    _publisher: Optional[ForwardRef("Publisher")] = None  # type: ignore[valid-type]

    @classmethod
    def from_id(cls, id: str) -> "Source":
        """Initialise Source from `id` as a positional argument:

        ```python
        source = Source.from_id("<publisher_id>:<source_id>")
        ```
        """
        publisher_slug, source_slug = parse_slug(id, 2)
        source = api.sources.get(slug=id)
        return cls(**source.model_dump())

    @classmethod
    def search(cls, name: str | None, year: int | None, publisher_id: str) -> list["Source"]:
        """
        Search for sources using their identifiers: name, year, publisher_id

        Args:
            name (str): The name to search
            year (int): The publication year to filter by
            published_id (str): The publisher identifier

        Returns:
            List[Source]: A list of Source objects.
        """

        search_results = api.sources.search(
            name=name,
            year=year,
            publisher_slug=publisher_id,
            includes="publisher,links,license",
        )

        return [cls(**source.model_dump()) for source in search_results]

    def _get_links(self):
        links = api.sources.get(
            slug=f"{self.publisher_slug}:{self.slug}", includes="links"
        ).base_links
        return links

    def _get_license(self):
        return api.sources.get(
            slug=f"{self.publisher_slug}:{self.slug}", includes="license"
        ).base_license

    @property
    def links(self):
        """A list of sources made available by this publisher."""
        if self.base_links is None:
            self.base_links = self._get_links()
            return self.base_links
        return self.base_links

    @property
    def license(self):
        if self.base_license is None:
            self.base_license = self._get_license()
            return self.base_license
        return self.base_license

    @property
    def publisher(self):
        if self._publisher is None:
            self._publisher = factory.publisher(
                **api.publishers.get(slug=self.publisher_slug).model_dump()
            )
            return self._publisher
        return self._publisher

    @property
    def id(self) -> str:
        return f"{self.publisher_slug}:{self.slug}"

    def __str__(self) -> str:
        return f"Source: {self.name} (i{self.id})"
