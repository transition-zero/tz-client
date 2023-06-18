import json
import os

import httpx

from transitionzero.client.auth import login


class Base:
    def __init__(self):
        token_path = os.environ.get(
            "FEO_TOKEN_PATH",
            os.path.join(os.path.expanduser("~"), ".tz-feo", "token.json"),
        )

        if os.path.exists(token_path):
            token = json.load(open(token_path))

        else:
            login()
            token = json.load(open(token_path))

        self.headers = {"Authorization": "Bearer {}".format(token["access_token"])}
        self.client = httpx.Client(
            base_url=os.environ.get(
                "FEO_API_URL", "https://api.feo.transitionzero.org"
            ),
            headers=self.headers,
        )

    def catch_errors(self, r):
        r.raise_for_status()
