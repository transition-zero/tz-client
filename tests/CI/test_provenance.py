from feo.client import Publisher, Source, api
from feo.client.api import schemas

TEST_SOURCE = "contributions"
TEST_PUBLISHER = "tz"


def test_api_sources_get():
    source = api.sources.get(f"{TEST_PUBLISHER}:{TEST_SOURCE}")

    assert isinstance(source, schemas.Source)


def test_api_publishers_get():
    publisher = api.publishers.get(f"{TEST_PUBLISHER}")

    assert isinstance(publisher, schemas.Publisher)


def test_publisher_get_sources():
    publisher = Publisher(**api.publishers.get(f"{TEST_PUBLISHER}").model_dump())

    for source in publisher.sources:
        assert isinstance(source, Source)


def test_source_get_publisher():
    source = Source(**api.sources.get(f"{TEST_PUBLISHER}:{TEST_SOURCE}").model_dump())

    assert isinstance(source.publisher, Publisher)
