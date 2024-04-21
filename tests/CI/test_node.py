import pytest

from tz.client import AssetCollection, Geometry, Node


@pytest.fixture
def node():
    return Node.from_id("DEU")


def test_node_initialization(node):
    assert node.id == "DEU"


def test_node_search():
    nodes = Node.search("germany")
    node_ids = [node.id for node in nodes]
    assert "DEU" in node_ids


def test_node_assets(node):
    assets = node.assets
    assert isinstance(assets, AssetCollection)


def test_node_children(node):
    children = node.children
    assert isinstance(children, list)
    assert all([isinstance(child, Node) for child in children])


def test_node_parents(node):
    parents = node.parents
    assert isinstance(parents, list)
    assert all(isinstance(parent, Node) for parent in parents)


def test_search_pagination():
    PAGE_LIMIT = 2
    items1 = Node.search("power plant", limit=PAGE_LIMIT, page=0)
    assert len(items1) == PAGE_LIMIT
    items2 = Node.search("power plant", limit=PAGE_LIMIT, page=1)
    assert len(items2) == PAGE_LIMIT

    ids1 = {item.id for item in items1}
    ids2 = {item.id for item in items2}
    # assert that items on different pages are all different
    assert ids1.intersection(ids2) == set()


def test_node_geometry(node):
    geom = node.geometry
    assert isinstance(geom, Geometry)


def test_node_str(node):
    assert str(node) == "Node: Germany (id=DEU)"


def test_node_children_with_type():
    children = Node.search("Europe")[0].get_children(child_type="admin_1")
    assert all([child.node_type == "admin_1" for child in children])