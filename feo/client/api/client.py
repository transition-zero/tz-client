import json
import os

import httpx

from feo.client.auth import login


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

    headers = {"Authorization": "Bearer {}".format(token["access_token"])}

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
