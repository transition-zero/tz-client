from typing import Optional

from feo.client import Publisher, api
from feo.client.api import schemas


class Source(schemas.Source):

    """
    The Source class references data to open-access documents by third parties.
    Sources have a license, and can have multiple links to track the origin of data.
    Sources are affiliated with a Publisher, and have a publication date.

    """

    _publisher: Optional[Publisher] = None

    @classmethod
    def from_id(cls, id: str) -> "Source":
        """Initialise Source from `id` as a positional argument:

        ```python
        source = Source.from_id("<publisher_id>:<source_id>")
        ```
        """
        source = api.sources.get(ids=id)[0]
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

        search_results = api.sources.get(
            name=name, year=year, publisher_id=publisher_id, includes="publisher,links,license"
        )

        return [cls(**source.model_dump()) for source in search_results.sources]
