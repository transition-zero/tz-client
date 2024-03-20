from tz.client.api.client import Client, ClientAuth


def test_client_no_token(mock_no_token):
    client_auth = ClientAuth()
    assert client_auth.no_token is True
    assert client_auth.token is None


def test_client_some_header(mock_some_header):
    client = Client(headers={"x-another-header": "another-value"})
    for k, v in [("x-some-header", "some-value"), ("x-another-header", "another-value")]:
        assert client.httpx_client.headers.get(k) == v


def test_client_overwrite_header(mock_some_header):
    client = Client(headers={"x-some-header": "overwrite-value"})
    for k, v in [("x-some-header", "overwrite-value")]:
        assert client.httpx_client.headers.get(k) == v
