import os
import threading
from typing import Generator

import httpx
from httpx._models import Request, Response

from feo.client.api.schemas import AuthToken
from feo.client.auth import AUTH0_CLIENT_ID, AUTH0_DOMAIN, TOKEN_PATH

CLIENT_TIMEOUT = 10


class RefreshTokenError(Exception):
    pass


class ClientAuth(httpx.Auth):
    """Auth class to attach token headers to requests"""

    requires_response_body = True

    def __init__(self):
        self.token_path = TOKEN_PATH
        self.token = None
        self._sync_lock = threading.RLock()

    def get_token(self):
        with self._sync_lock:
            if self.token is None:
                try:
                    # parse from local token file
                    self.token = AuthToken.from_file(self.token_path)
                except FileNotFoundError:
                    raise FileNotFoundError(
                        f"No token file found at path '{self.token_path}'. Please login."
                    ) from None

    def _parse_token_response(self, token_response):
        if token_response.status_code == 403:
            raise RefreshTokenError("Token refresh failed. Please login again.")
        self.token = AuthToken(**token_response.json())

    def _refresh_token_request(self) -> httpx.Request:
        """Build a refresh token HTTPX request"""
        token_payload = {
            "grant_type": "refresh_token",
            "client_id": AUTH0_CLIENT_ID,
            "refresh_token": self.token.refresh_token,
        }

        return httpx.Request("POST", f"https://{AUTH0_DOMAIN}/oauth/token", data=token_payload)

    def sync_auth_flow(self, request: Request) -> Generator[Request, Response, None]:
        self.get_token()
        request.headers.update({"Authorization": f"Bearer {self.token.access_token}"})
        response = yield request

        if response.status_code == 401:
            # Auth failed - possible expired token
            # Send refresh token request and parse response
            refresh_response = yield self._refresh_token_request()
            self._parse_token_response(refresh_response)

            # attach new token header
            request.headers.update({"Authorization": f"Bearer {self.token.access_token}"})
            yield request


class Client:
    base_url = (
        os.environ.get("FEO_API_URL", "https://api.feo.transitionzero.org")
        + "/"
        + os.environ.get("FEO_API_VERSION", "v1")
    )

    httpx_client = httpx.Client(
        base_url=base_url,
        auth=ClientAuth(),
        timeout=CLIENT_TIMEOUT,
    )

    def __init__(self):
        pass

    def get(self, *args, **kwargs):
        return self.httpx_client.get(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self.httpx_client.post(*args, **kwargs)

    @classmethod
    def catch_errors(cls, r):
        r.raise_for_status()


client = Client()
