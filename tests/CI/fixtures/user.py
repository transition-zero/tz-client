import os

import pytest


@pytest.fixture
def username():
    return os.environ.get("TZ_TEST_DATA_OWNER", "feo-core-admin")
