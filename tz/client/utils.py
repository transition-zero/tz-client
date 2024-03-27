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


def lazy_load_relationship(cls, field, loader):
    """Update the `cls` to have the `field` relationship (i.e. list of
    things) lazy-loaded by the provided loader so that when someone writes
    'cls.field' they get the pre-loaded objects.

    Note that this assumes there is a field named "_field" defined in "cls"
    where the results will be cached.
    """

    def lazy_loader(self):
        hidden = f"_{field}"
        if getattr(self, hidden) is None:
            loaded = loader(self)
            items = getattr(loaded, field)
            values = [cls(**c.model_dump()) for c in items]
            setattr(self, hidden, values)
        v = getattr(self, hidden)
        return v

    setattr(cls, field, property(lazy_loader))
