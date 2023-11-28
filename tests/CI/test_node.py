import pytest

from feo.client import AssetCollection, Geometry, Node


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


def test_node_geometry(node):
    geom = node.geometry
    assert isinstance(geom, Geometry)
