from feo.client import Run


def test_run_init():
    runs = Run("feo-global-indonesia:feo-indonesia-current-policies:demo")
    assert isinstance(runs, Run)


def test_run_search():
    runs = Run.search()
    assert isinstance(runs, list)
    assert isinstance(runs[0], Run)
