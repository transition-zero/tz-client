import os
from unittest import mock
from unittest.mock import ANY

import pytest

from tz.client import api

FULLSLUG = "feo-global-indonesia:feo-indonesia-current-policies:demo"
RECORD_GET_CASES = [
    (
        dict(
            node_id="BRN",
            datum_type="technology_parameter",
            datum_detail="power.BIO.capex",
            valid_timestamp_start="2039-01-01 00:00:00",
            valid_timestamp_end="2039-01-01 23:59:59",
        ),
        dict(value=1570.5),
    ),
]
RECORD_POST_CSV_CASES = [
    (
        dict(
            csv_path="tmp.csv",
            publisher_slug="feo-global-indonesia",
            source_slug="feo-indonesia-current-policies",
        ),
        dict(status="success"),
    ),
]


@pytest.mark.xfail(reason="v2 migration wip")
@pytest.mark.parametrize("record_get_cases", RECORD_GET_CASES)
def test_api_records_get(record_get_cases):
    params, expected_result = record_get_cases
    records = api.records.get(**params)

    for k, v in expected_result.items():
        for record in records:
            print(record)
            print(k, v)
            print("GET", getattr(record, k))
            assert getattr(record, k) == v


@pytest.mark.xfail(reason="v2 migration wip")
@pytest.mark.parametrize("record_post_csv_cases", RECORD_POST_CSV_CASES)
def test_post_csv(record_post_csv_cases):
    params, expected_result = record_post_csv_cases
    csv_path = params["csv_path"]
    publisher_slug = params["publisher_slug"]
    source_slug = params["source_slug"]

    with mock.patch.object(api.records.client, "post") as mock_post:
        mock_response = mock.Mock()
        mock_response.json.return_value = expected_result
        mock_post.return_value = mock_response

        # POST dummy CSV file
        with open(csv_path, "w") as f:
            f.write("a,b,c")
        result = api.records.post_csv(csv_path, publisher_slug, source_slug)

        assert result == expected_result
        with open(csv_path, "rb") as f:
            mock_post.assert_called_once_with(
                f"/records/{publisher_slug}:{source_slug}/data",
                files={"file": ("tmp.csv", ANY)},
            )
        os.remove(csv_path)
