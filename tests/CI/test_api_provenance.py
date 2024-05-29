from unittest import mock

import pytest
from requests.exceptions import HTTPError

from tz.client import Publisher, Source, api
from tz.client.api import schemas

TEST_SOURCE = "contributions"
TEST_PUBLISHER = "tz"

PUBLISHER_POST_CASES = [
    (
        dict(
            name="Publisher 1",
            short_name="pub1",
            organisation_type="Type 1",
            url="http://example.com",
            public=True,
            slug="slug1",
        ),
        dict(status="success"),
    ),
]
SOURCE_POST_CASES = [
    (
        dict(
            name="dummy_name",
            short_name="dummy_short_name",
            public=True,
            description="dummy_description",
            year=2022,
            month=1,
            day=1,
            quarter=1,
            license_abbrv="dummy_license_abbrv",
            publisher_slug="dummy_publisher_slug",
            slug="dummy_slug",
            links=[],
            nodes=[],
            license="dummy_license",
        ),
        dict(status="success"),
    ),
]


@pytest.mark.xfail(reason="v2 migration wip")
def test_api_sources_get():
    source = api.sources.get(f"{TEST_PUBLISHER}:{TEST_SOURCE}")

    assert isinstance(source, schemas.Source)


@pytest.mark.xfail(reason="v2 migration wip")
def test_api_publishers_get():
    publisher = api.publishers.get(f"{TEST_PUBLISHER}")

    assert isinstance(publisher, schemas.Publisher)


@pytest.mark.xfail(reason="v2 migration wip")
def test_publisher_get_sources():
    publisher = Publisher(**api.publishers.get(f"{TEST_PUBLISHER}").model_dump())

    for source in publisher.sources:
        assert isinstance(source, Source)


@pytest.mark.xfail(reason="v2 migration wip")
def test_source_get_publisher():
    source = Source(**api.sources.get(f"{TEST_PUBLISHER}:{TEST_SOURCE}").model_dump())

    assert isinstance(source.publisher, Publisher)


@pytest.mark.xfail(reason="v2 migration wip")
@pytest.mark.parametrize("publisher_post_cases", PUBLISHER_POST_CASES)
def test_publisher_post(publisher_post_cases):
    params, expected_result = publisher_post_cases
    with mock.patch.object(api.publishers.client, "post") as mock_post:
        mock_response = mock.Mock()
        mock_response.json.return_value = expected_result
        mock_post.return_value = mock_response

        result = api.publishers.post(**params)

        assert result == expected_result
        mock_post.assert_called_once_with(
            "/publishers",
            json=params,
        )


@pytest.mark.xfail(reason="v2 migration wip")
@pytest.mark.parametrize("publisher_post_cases", PUBLISHER_POST_CASES)
def test_publisher_post_http_error(publisher_post_cases):
    params, _ = publisher_post_cases
    with mock.patch.object(api.publishers.client, "post") as mock_post:
        mock_response = mock.Mock()
        mock_response.raise_for_status.side_effect = HTTPError("HTTP Error")
        mock_post.return_value = mock_response

        with pytest.raises(HTTPError):
            api.publishers.post(
                **params,
            )

        mock_post.assert_called_once_with(
            "/publishers",
            json=params,
        )


@pytest.mark.xfail(reason="v2 migration wip")
@pytest.mark.parametrize("source_post_cases", SOURCE_POST_CASES)
def test_source_post(source_post_cases):
    params, expected_result = source_post_cases
    with mock.patch.object(api.sources.client, "post") as mock_post:
        mock_response = mock.Mock()
        mock_response.json.return_value = expected_result
        mock_post.return_value = mock_response

        result = api.sources.post(
            **params,
        )

        assert result == expected_result
        mock_post.assert_called_once_with(
            "/sources",
            json=params,
        )


@pytest.mark.xfail(reason="v2 migration wip")
@pytest.mark.parametrize("source_post_cases", SOURCE_POST_CASES)
def test_source_post_http_error(source_post_cases):
    params, _ = source_post_cases
    with mock.patch.object(api.sources.client, "post") as mock_post:
        mock_response = mock.Mock()
        mock_response.raise_for_status.side_effect = HTTPError("HTTP Error")
        mock_post.return_value = mock_response

        with pytest.raises(HTTPError):
            api.sources.post(
                **params,
            )

        mock_post.assert_called_once_with(
            "/sources",
            json=params,
        )
