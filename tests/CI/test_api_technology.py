from unittest import mock

import pytest
from requests.exceptions import HTTPError

from feo.client import api

EXAMPLE_TECHNOLOGY = "coal"
TECHNOLOGY_POST_CASES = [
    dict(
        name="example_name",
        slug="example_slug",
        public=True,
        properties={"key": "value"},
        parents=["parent1", "parent2"],
        children=["child1", "child2"],
    ),
    dict(status="success"),
]


def test_technology_search():
    technologies = api.technologies.search()
    assert isinstance(technologies, list)
    assert isinstance(technologies[0], api.schemas.Technology)


def test_model_get():
    models = api.technologies.get(EXAMPLE_TECHNOLOGY)
    assert isinstance(models, api.schemas.Technology)


@pytest.mark.parametrize("technology_post_cases", TECHNOLOGY_POST_CASES)
def test_technology_post(technology_post_cases):
    params, expected_result = technology_post_cases
    with mock.patch.object(api.sources.client, "post") as mock_post:
        mock_response = mock.Mock()
        mock_response.json.return_value = expected_result
        mock_post.return_value = mock_response

        result = api.technologies._post(
            **params,
        )

        assert result == expected_result
        mock_post.assert_called_once_with(
            "/technologies",
            json=params,
        )


@pytest.mark.parametrize("technology_post_cases", TECHNOLOGY_POST_CASES)
def test_technology_post_http_error(technology_post_cases):
    params, _ = technology_post_cases
    with mock.patch.object(api.sources.client, "post") as mock_post:
        mock_response = mock.Mock()
        mock_response.raise_for_status.side_effect = HTTPError("HTTP Error")
        mock_post.return_value = mock_response

        with pytest.raises(HTTPError):
            api.sources._post(
                **params,
            )

        mock_post.assert_called_once_with(
            "/technologies",
            json=params,
        )
