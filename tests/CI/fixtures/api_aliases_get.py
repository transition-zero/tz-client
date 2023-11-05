import pytest


@pytest.fixture
def alias_get_cases():
    return [
        (dict(alias="indonesia", node_type="admin_0"), ["IDN"]),
    ]
