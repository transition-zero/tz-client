from feo.client import api


def test_api_records_get(record_get_cases):
    cases = []
    for params, expected_results in record_get_cases:
        response = api.records.get(**params)

        cases.append({record.node_id for record in response.records} == set(expected_results))

    assert all(cases)
