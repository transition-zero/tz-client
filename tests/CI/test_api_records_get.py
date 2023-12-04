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
