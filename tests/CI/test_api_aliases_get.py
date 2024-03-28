import pytest

from tz.client import api


@pytest.mark.xfail(reason="v2 migration wip")
def test_api_aliases_get(alias_get_cases):
    cases = []
    for params, expected_results in alias_get_cases:
        response = api.aliases.get(**params)

        cases.append({alias.node_id for alias in response.aliases} == set(expected_results))

    assert all(cases)
