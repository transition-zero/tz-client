import json
import os
import threading
from typing import Generator

import httpx
from httpx._models import Request, Response

from tz.client.api.schemas import AuthToken
from tz.client.auth import AUTH0_CLIENT_ID, AUTH0_DOMAIN, TOKEN_PATH

CLIENT_TIMEOUT = 10
LOGIN_EXAMPLE = """from tz.client.auth import login
login()"""


class RefreshTokenError(Exception):
    pass


class ClientAuth(httpx.Auth):
    """Auth class to attach token headers to requests."""

    requires_response_body = True

    def __init__(self):
        self.token_path = TOKEN_PATH
        self._sync_lock = threading.RLock()
        try:
            # Parse from local token file if it exists.
            self.token = AuthToken.from_file(self.token_path)
        except FileNotFoundError:
            # Silently set token to None.
            self.token = None

    def get_token(self):
        """Get an AuthToken if instance does not already have one.

        Raises:
            FileNotFoundError: If token file does not exist.
        """
        with self._sync_lock:
            if self.token is None:
                try:
                    # Parse from local token file.
                    self.token = AuthToken.from_file(self.token_path)
                except FileNotFoundError:
                    raise FileNotFoundError(
                        f"No token file found at path '{self.token_path}'."
                        f" Please login e.g. \n{LOGIN_EXAMPLE}"
                    )

    def _refresh_token_parse(self, token_response: httpx.Response):
        """Parse a httpx Response into a new AuthToken object

        Args:
            token_response httpx.Response: Response from the oauth/token endpoint.

        Raises:
            RefreshTokenError: If there is an error with the response.
        """

        # need to call read before parsing
        token_response.read()
        token_json = token_response.json()
        if token_response.status_code == 403:
            err_description = token_json.get("error_description", "No additional information")
            raise RefreshTokenError(f"{err_description}. Please login e.g. \n{LOGIN_EXAMPLE}")
        self.token = AuthToken(**token_json)

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
            self._refresh_token_parse(refresh_response)

            # attach new token header
            request.headers.update({"Authorization": f"Bearer {self.token.access_token}"})
            yield request


class Client:
    base_url = (
        os.environ.get("TZ_API_URL", "https://api.feo.transitionzero.org")
        + "/"
        + os.environ.get("TZ_API_VERSION", "v1")
    )

    headers = {}
    maybe_headers = os.environ.get("TZ_HEADERS")
    if maybe_headers:
        headers = json.loads(maybe_headers)

    httpx_client = httpx.Client(
        base_url=base_url, auth=ClientAuth(), timeout=CLIENT_TIMEOUT, headers=headers
    )

    def __init__(self):
        pass

    def get(self, *args, **kwargs):
        return self.httpx_client.get(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self.httpx_client.post(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.httpx_client.delete(*args, **kwargs)

    @classmethod
    def catch_errors(cls, r):
        r.raise_for_status()


client = Client()
