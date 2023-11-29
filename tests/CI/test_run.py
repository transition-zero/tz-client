from feo.client import Model, Run


def test_run_init():
    run = Run.from_id("feo-global-indonesia:feo-indonesia-current-policies:demo")
    assert isinstance(run, Run)
    assert run.id == "feo-global-indonesia:feo-indonesia-current-policies:demo"


def test_run_search():
    runs = Run.search()
    assert isinstance(runs, list)
    assert isinstance(runs[0], Run)


def test_search_pagination():
    PAGE_LIMIT = 2
    items1 = Run.search(limit=PAGE_LIMIT, page=0)
    assert len(items1) == PAGE_LIMIT
    items2 = Run.search(limit=PAGE_LIMIT, page=1)
    assert len(items2) == PAGE_LIMIT

    # assert that no items are returned when page number is too high
    items_bad = Run.search(limit=PAGE_LIMIT, page=10000)
    assert len(items_bad) == 0

    ids1 = {item.id for item in items1}
    ids2 = {item.id for item in items2}
    # assert that items on different pages are all different
    assert ids1.intersection(ids2) == set()


def test_run_model():
    run = Run.from_id("feo-global-indonesia:feo-indonesia-current-policies:demo")
    model = run.model
    assert isinstance(model, Model)
    assert model.id == "feo-global-indonesia"


def test_run_str():
    run = Run.from_id("feo-global-indonesia:feo-indonesia-current-policies:demo")
    assert str(run) == "Run: demo (id=feo-global-indonesia:feo-indonesia-current-policies:demo)"
