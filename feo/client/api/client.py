import json
import os

import httpx

from feo.client.api.schemas import AuthToken
from feo.client.auth import login


class MissingAuthError(BaseException):
    pass


class Auth:
    DEFAULT_TOKEN_PATH = os.path.join(os.path.expanduser("~"), ".tz-feo", "token.json")
    DEFAULT_TOKEN_ENV = "FEO_TOKEN_PATH"  # nosec

    def __init__(self):
        self.token_path = os.environ.get(self.DEFAULT_TOKEN_ENV, self.DEFAULT_TOKEN_PATH)

        self.token = None

    def authorize(self):
        login()
        self.token = AuthToken.from_file(self.token_path)

    def to_header(self):
        if self.token is None:
            self.authorize()

        return {"Authorization": f"Bearer {self.token.access_token}"}


class Client:
    token_path = os.environ.get(
        "FEO_TOKEN_PATH",
        os.path.join(os.path.expanduser("~"), ".tz-feo", "token.json"),
    )

    if os.path.exists(token_path):
        token = json.load(open(token_path))

    else:
        login()
        token = json.load(open(token_path))

    headers = {
        "Authorization": "Bearer {}".format(token["access_token"]),
        "user-agent": "feo-client",
    }

    base_url = (
        os.environ.get("FEO_API_URL", "https://api.feo.transitionzero.org")
        + "/"
        + os.environ.get("FEO_API_VERSION", "v1")
    )
    httpx_client = httpx.Client(
        base_url=base_url,
        headers=headers,
        timeout=10,
    )

    def _add_auth(self, func):
        pass

    def _parse_token(self):
        pass

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
