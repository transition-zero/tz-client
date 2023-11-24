from feo.client import Run


def test_run_init():
    run = Run.from_id("feo-global-indonesia:feo-indonesia-current-policies:demo")
    assert isinstance(run, Run)
    assert run.id == "feo-global-indonesia:feo-indonesia-current-policies:demo"


def test_run_search():
    runs = Run.search()
    assert isinstance(runs, list)
    assert isinstance(runs[0], Run)
