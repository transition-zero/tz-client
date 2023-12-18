import os
from unittest import mock
from unittest.mock import ANY

import pytest

from feo.client import api

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


@pytest.mark.parametrize(
    "csv_path, publisher_slug, source_slug",
    [
        ("tmp.csv", "pub1", "source1"),
    ],
)
def test_post_csv(api, csv_path, publisher_slug, source_slug):
    with mock.patch.object(api.records.client, "post") as mock_post:
        mock_response = mock.Mock()
        mock_response.json.return_value = {"status": "success"}
        mock_post.return_value = mock_response

        # POST dummy CSV file
        with open(csv_path, "w") as f:
            f.write("a,b,c")
        result = api.post_csv(csv_path, publisher_slug, source_slug)

        assert result == {"status": "success"}
        with open(csv_path, "rb") as f:
            mock_post.assert_called_once_with(
                f"/records/{publisher_slug}:{source_slug}/data",
                files={"file": ("tmp.csv", ANY)},
            )
        os.remove(csv_path)


@pytest.mark.parametrize(
    "csv_path, publisher_slug, source_slug",
    [
        ("path/to/csv", "pub1", 1),
        ("path/to/csv", 2, 2),
        (1, "pub1", "source1"),
    ],
)
def test_post_type_errors(api, csv_path, publisher_slug, source_slug):
    with pytest.raises(TypeError):
        api.post_csv(csv_path, publisher_slug, source_slug)
