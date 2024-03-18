import os
from typing import List, Union

ENVIRONMENT = (
    "staging"
    if os.environ.get("TZ_API_URL") == "https://staging.api.feo.transitionzero.org"
    else "production"
)


def parse_slug(fullslug, nparts):
    slug_parts = fullslug.split(":")

    if len(slug_parts) != nparts:
        raise ValueError(
            f"Wrong number of slug parts provided; required {nparts}, got {len(slug_parts)}."
        )

    return slug_parts


def enforce_list(val: Union[List, str]):
    if isinstance(val, list):
        return val
    elif isinstance(val, str):
        return val.split(",")
