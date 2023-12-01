import json
import os

import httpx

from feo.client.auth import login


class Client:
    def __init__(self):
        self.token_path = os.environ.get(
            "FEO_TOKEN_PATH",
            os.path.join(os.path.expanduser("~"), ".tz-feo", "token.json"),
        )

        if os.path.exists(self.token_path):
            self.token = json.load(open(self.token_path))

        else:
            login()
            self.token = json.load(open(self.token_path))

        self.headers = {"Authorization": "Bearer {}".format(self.token["access_token"])}

        self.base_url = (
            os.environ.get("FEO_API_URL", "https://api.feo.transitionzero.org")
            + "/"
            + os.environ.get("FEO_API_VERSION", "v1")
        )
        self.httpx_client = httpx.Client(
            base_url=self.base_url,
            headers=self.headers,
            timeout=10,
        )

    def get(self, *args, **kwargs):
        return self.httpx_client.get(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self.httpx_client.post(*args, **kwargs)

    @classmethod
    def catch_errors(cls, r):
        r.raise_for_status()
