from typing import TYPE_CHECKING, ForwardRef, List, Optional

from feo.client import api, factory
from feo.client.api import schemas

# from feo.client.source import factory as source_factory

if TYPE_CHECKING:
    from feo.client.source import Source


class Publisher(schemas.Publisher):

    """
    The Publisher class catalogues third parties who publish data relevant to the energy transition.
    Publishers have a name, a short-name, and an organisation-type.

    """

    _sources: Optional[List[ForwardRef("Source")]] = None  # type: ignore[valid-type]

    @classmethod
    def from_id(cls, id: str) -> "Publisher":
        """Initialise Source from `id` as a positional argument:

        ```python
        source = Source.from_id("<publisher_id>:<source_id>")
        ```
        """
        publisher = api.publishers.get(slug=id)
        return cls(**publisher.model_dump())

    @classmethod
    def search(cls, name: str | None) -> list["Publisher"]:
        """
        Search for publishers using their identifiers: name

        Args:
            name (str): The name to search

        Returns:
            List[Publisher]: A list of Publisher objects.
        """

        search_results = api.publishers.search(
            name=name,
        )

        return [cls(**publisher.model_dump()) for publisher in search_results]

    @classmethod
    def _get_sources(cls, publisher_slug: str):
        return [
            factory.source(**source.model_dump())
            for source in api.sources.search(publisher_slug=publisher_slug)
        ]

    @property
    def sources(self) -> list["Source"]:
        """A list of sources made available by this publisher."""
        if self._sources is None:
            self._sources = self._get_sources(self.slug)
            return self._sources
        return self._sources

    @property
    def id(self) -> str:
        return self.slug

    def __str__(self) -> str:
        return f"Publisher: {self.name} (id={self.id})"
