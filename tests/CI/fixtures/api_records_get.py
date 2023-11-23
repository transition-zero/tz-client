import pytest


@pytest.fixture
def records_get_cases():
    return [
        (
            dict(alias="indonesia", node_type="admin_0"),
            ["IDN"],
        ),  # TODO: Get example records
    ]
