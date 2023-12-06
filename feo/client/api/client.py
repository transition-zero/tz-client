import os

import httpx

from feo.client.api.schemas import AuthToken
from feo.client.auth import AUTH0_CLIENT_ID, AUTH0_DOMAIN, TOKEN_PATH, login

CLIENT_TIMEOUT = 10


class ClientAuth(httpx.Auth):
    requires_response_body = True

    def __init__(self):
        self.token_path = TOKEN_PATH

    def _parse_token_file(self, token_file):
        try:
            self.token = AuthToken.from_file(self.token_path)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"No token file found at path '{self.token_path}'. Please login."
            )

    def _parse_token_response(self, token_response):
        self.token = AuthToken(**token_response.json())

    def _refresh_token_resquest(self):
        token_payload = {
            "grant_type": "refresh_token",
            "client_id": AUTH0_CLIENT_ID,
            "refresh_token": self.token.refresh_token,
        }

        return httpx.Request("POST", f"https://{AUTH0_DOMAIN}/oauth/token", data=token_payload)

    def auth_flow(self, request):
        if self.token is None:
            try:
                self._parse_token_file(self.token_path)
            except FileNotFoundError:
                login()

        else:
            request.headers.update({"Authorization": f"Bearer {self.token.access_token}"})
            response = yield request

            if response.status_code == 401:
                # possible expired token
                refresh_response = yield self.refresh_token_resquest()
                self._parse_token_response(refresh_response)

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
