import json

import pytest


@pytest.fixture
def mock_no_token(monkeypatch):
    monkeypatch.setenv("TZ_NO_TOKEN", "TRUE")


@pytest.fixture
def mock_some_header(monkeypatch):
    monkeypatch.setenv("TZ_HEADERS", json.dumps({"x-some-header": "some-value"}))
