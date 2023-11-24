from typing import List, Optional

from feo.client import Source, api
from feo.client.api import schemas


class Publisher(schemas.Publisher):

    """
    The Publisher class catalogues third parties who publish data relevant to the energy transition.
    Publishers have a name, a short-name, and an organisation-type.

    """

    _sources: Optional[List[Source]] = None

    @classmethod
    def from_id(cls, id: str) -> "Publisher":
        """Initialise Source from `id` as a positional argument:

        ```python
        source = Source.from_id("<publisher_id>:<source_id>")
        ```
        """
        publisher = api.publishers.get(ids=id)[0]
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

        search_results = api.publishers.get(
            name=name,
        )

        return [cls(**publisher.model_dump()) for publisher in search_results.publishers]

    @classmethod
    def _get_sources(cls, publisher_id: str):
        return [
            Source(**source.model_dump())
            for source in api.sources.get(publisher_id=publisher_id).sources
        ]

    @property
    def sources(self) -> list["Source"]:
        """A list of sources made available by this publisher."""
        if self._sources is None:
            self._sources = self._get_sources(self.id)
            return self._sources
        return self._sources
