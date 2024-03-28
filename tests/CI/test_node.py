import pytest

from tz.client import AssetCollection, Node


@pytest.fixture
def node():
    return Node.from_slug("DEU")


def test_node_initialization(node):
    assert node.slug == "DEU"


def test_node_search():
    nodes = Node.search("Germany")
    node_slugs = [node.slug for node in nodes]
    assert "DEU" in node_slugs


@pytest.mark.xfail(reason="v2 migration; assets needs a bit of work")
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


@pytest.mark.xfail(reason="search currently not working")
def test_node_search_pagination():
    PAGE_LIMIT = 2
    items1 = Node.search("power plant", limit=PAGE_LIMIT, page=0)
    assert len(items1) == PAGE_LIMIT
    items2 = Node.search("power plant", limit=PAGE_LIMIT, page=1)
    assert len(items2) == PAGE_LIMIT

    ids1 = {item.id for item in items1}
    ids2 = {item.id for item in items2}
    # assert that items on different pages are all different
    assert ids1.intersection(ids2) == set()


def test_node_str(node):
    assert str(node) == "Node: Germany (id=DEU)"
