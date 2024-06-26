from importlib import import_module
from typing import List, Union


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


def id(x):
    return x


def lazy_load_relationship(cls, mk_cls, field, loader, f=id, g=id):
    """Update the `cls` to have the `field` relationship (i.e. list of
    things) lazy-loaded by the provided loader so that when someone writes
    'cls.field' they get the pre-loaded objects.

    Note that this assumes there is a field named "_field" defined in "cls"
    where the results will be cached.

    Args:
        cls: The class name to which we will add `field` as a property.
        mk_cls: A way to construct the type of `field`;
          we let this be a string because, sometimes, it needs
          to be done lazily due to circular imports.
        field: The name of the field that we are overwriting.
        f: an (optional) function to be evaluated on the result of evaluating
          the 'loader' function and extracting 'field' from it. This can be
          used, say, to wrap the item in a list; because we assume list-based
          processing in the body of the function.
        g: an (optional) function to be evaluated _after_ converting all the
          items to a list of `mk_cls`-based classes. This can be used to, say,
          unwrap the item from a list if we previously had to do that.

    Returns:
        Nothing.
    """

    def camel_to_snake(s):
        return "".join(["_" + c.lower() if c.isupper() else c for c in s]).lstrip("_")

    def lazy_loader(self):
        # Note: Here we assume `self` is a pydantic model and we send the
        # value of `model_dump()` as context to the `loader` function above.
        # This is so initial values of fields can be used in lazy-loading.
        current_context = self.model_dump()

        if isinstance(mk_cls, str):
            # Bit of a hack to simplify the lazy-loading troubles: just let people
            # use a string and we'll just import it by convention; this is
            # because of circular dependencies.
            module_name = camel_to_snake(mk_cls)
            module = import_module(f"tz.client.{module_name}")
            mk_class = getattr(module, mk_cls)
        else:
            mk_class = mk_cls
        hidden = f"_{field}"

        if getattr(self, hidden) is None:
            loaded = loader(self, current_context)
            items = f(getattr(loaded, field))
            values = g([mk_class(**c.model_dump()) for c in items])
            setattr(self, hidden, values)
        v = getattr(self, hidden)
        return v

    setattr(cls, field, property(lazy_loader))


def lazy_load_single_relationship(cls, mk_cls, field, loader):
    # Re-use the above function for single-field relationships by just
    # pretending we have a list.
    to_list = lambda x: [x]  # noqa: E731
    from_list = lambda x: x[0]  # noqa: E731
    return lazy_load_relationship(cls, mk_cls, field, loader, f=to_list, g=from_list)
