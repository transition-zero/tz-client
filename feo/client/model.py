from typing import List, Optional, TypeVar

from feo.client.base import Base
from feo.client.node import Node

Cls = TypeVar("Cls", bound="Model")


class Model(Base):
    """A FEO systems model specifying nodes, links, sectors, and time resolution.


    Attributes
    ----------
    geography : str | None
        A named geography 'alias' corresponding to a representative node.
    node_level : str | None
        The node_level to define the model fidelity if initialising from a named geography.
    nodes : list[str] | list[Node] | None
        The nodes to comprise the model. Either 'geography'&'node_level' OR 'nodes'&'links' is required.
    links : list[str] | list[Link] | None
        The links which join the nodes into a network.
    sectors : list[str] | None
        A list of sectors to define the coverage of the model.
    time_resolution : str | None
        The time resolution of the model.

    Methods
    -------
    copy()
        Copy the model to a new one under the user's ownership.
    save()
        Save any changes to the current model.
    json()
        Access a JSON representation of the current model.
    _load_model()
        Populate model properties.

    ClassMethods
    -------
    from_json(blob: dict)
        Instantiate a model from a json blob.
    search()

    get(id: str)
        Return a new instance of a model, calling the api and the id.

    _get(id: str)
        Call the api and return a model's properties.



    """

    def __init__(
        self,
        uuid: Optional[str] = None,
        name: Optional[str] = None,
        sectors: Optional[List[str]] = None,
        time_scope: Optional[dict] = None,
        slug: Optional[str] = None,
        version: Optional[str] = None,
        geography: Optional[str] = None,
        node_level: Optional[str] = None,
        node_ids: Optional[List[str]] = None,
        link_ids: Optional[List[str]] = None,
        **kwargs,
    ):
        super().__init__()

        # LOAD A MODEL
        if uuid is not None:
            # check all other params are available
            self.uuid = uuid
            if all(
                [
                    (val is not None)
                    for val in [
                        name,
                        sectors,
                        time_scope,
                        slug,
                        version,
                        node_ids,
                        link_ids,
                    ]
                ]
            ):
                self._load_model(
                    name, sectors, time_scope, slug, version, node_ids, link_ids
                )
            elif all(
                [
                    (val is None)
                    for val in [
                        name,
                        sectors,
                        time_scope,
                        slug,
                        version,
                        node_ids,
                        link_ids,
                    ]
                ]
            ):
                # initialise via api call and uuid.
                params = self._get(uuid)
                self._load_model(**params)
            else:
                for var_name, val in zip(
                    [
                        "name",
                        "sectors",
                        "time_scope",
                        "slug",
                        "version",
                        "node_ids",
                        "link_ids",
                    ],
                    [name, sectors, time_scope, slug, version, node_ids, link_ids],
                ):
                    if val is None:
                        raise ValueError(
                            f"Initialising model: missing {var_name}. If initialising with uuid, all variables must be available."
                        )

        # CREATE A NEW MODEL
        # geography and node_level must be specified together
        if geography is not None:
            assert (
                node_level is not None
            ), "Specify either a 'geography' and a 'node_level', or a set or 'node_ids'."

            geography_node = Node.from_alias(geography)

            nodes = geography_node.children(node_level=node_level)
            node_ids = [n.code for n in nodes]
            link_ids = []  # TODO

        for var_name, val in zip(
            ["name", "sectors", "time_scope", "slug", "version", "nodes", "link_ids"],
            [name, sectors, time_scope, slug, version, node_ids, link_ids],
        ):
            assert val is not None, f"Creating model: {var_name} must not be None."
        self._load_model(name, sectors, time_scope, slug, version, node_ids, link_ids)

    def save(self):
        raise NotImplementedError

    def copy(self):
        raise NotImplementedError

    def json(self):
        raise NotImplementedError

    def _load_model(
        self,
        name: str,
        sectors: List[str],
        time_scope: dict,
        slug: str,
        version: str,
        node_ids: str,
        link_ids: str,
    ):
        self.name = name
        self.sectors = sectors
        self.time_scope = time_scope
        self.slug = slug
        self.version = version
        self.node_ids = node_ids
        self.link_ids = link_ids

    @classmethod
    def from_json(cls, **kwargs):
        return cls(**kwargs)

    @classmethod
    def search(
        cls,
        owner: Optional[str] = None,
        public: Optional[bool] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
    ) -> List[Cls]:
        params = {
            "owner": owner,
            "public": public,
            "limit": limit,
            "page": page,
        }

        r = cls.api.get(
            "/models",
            params={k: v for k, v in params.items() if v},
        )

        cls.catch_errors(r)

        return [cls.from_json(**data) for uuid, data in r.json()["models"].items()]

    @classmethod
    def get(cls, uuid: str) -> Cls:
        return cls.from_json(cls._get(uuid))

    @classmethod
    def _get(cls, uuid: str) -> dict:
        r = cls.api.get(f"/models/{uuid}")

        cls.catch_errors(r)

        return r.json()
