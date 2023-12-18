from unittest import mock

import pytest
from requests.exceptions import HTTPError

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


@pytest.mark.parametrize(
    "name, short_name, organisation_type, url, public, slug",
    [
        ("Publisher 1", "pub1", "Type 1", "http://example.com", True, "slug1"),
        ("Publisher 2", "pub2", "Type 2", None, False, None),
    ],
)
def test_publisher_post(name, short_name, organisation_type, url, public, slug):
    with mock.patch.object(api.publishers.client, "post") as mock_post:
        mock_response = mock.Mock()
        mock_response.json.return_value = {"status": "success"}
        mock_post.return_value = mock_response

        result = api.publishers._post(
            name=name,
            short_name=short_name,
            organisation_type=organisation_type,
            url=url,
            public=public,
            slug=slug,
        )

        assert result == {"status": "success"}
        mock_post.assert_called_once_with(
            "/publishers",
            json={
                "name": name,
                "short_name": short_name,
                "url": url,
                "public": public,
                "organisation_type": organisation_type,
                "slug": slug,
            },
        )


@pytest.mark.parametrize(
    "name, short_name, organisation_type, url, public, slug",
    [
        ("Publisher 3", "pub3", "Type 3", None, None, None),
    ],
)
def test_publisher_post_http_error(name, short_name, organisation_type, url, public, slug):
    with mock.patch.object(api.publishers.client, "post") as mock_post:
        mock_response = mock.Mock()
        mock_response.raise_for_status.side_effect = HTTPError("HTTP Error")
        mock_post.return_value = mock_response

        with pytest.raises(HTTPError):
            api.publishers._post(
                name=name,
                short_name=short_name,
                organisation_type=organisation_type,
                url=url,
                public=public,
                slug=slug,
            )

        mock_post.assert_called_once_with(
            "/publishers",
            json={
                "name": name,
                "short_name": short_name,
                "url": url,
                "public": public,
                "organisation_type": organisation_type,
                "slug": slug,
            },
        )


@pytest.mark.parametrize(
    "name, short_name, organisation_type, url, public, slug",
    [
        (123, "pub", "Type", "http://example.com", True, "slug"),
        ("Publisher", None, "Type", "http://example.com", True, "slug"),
        ("Publisher", "pub", True, "http://example.com", True, "slug"),
        ("Publisher", "pub", "Type", 123, True, "slug"),
        ("Publisher", "pub", "Type", "http://example.com", 123, "slug"),
        ("Publisher", "pub", "Type", None, None, 123),
    ],
)
def test_publisher_post_type_errors(name, short_name, organisation_type, url, public, slug):
    with pytest.raises(TypeError):
        api.publishers._post(
            name=name,
            short_name=short_name,
            organisation_type=organisation_type,
            url=url,
            public=public,
            slug=slug,
        )
