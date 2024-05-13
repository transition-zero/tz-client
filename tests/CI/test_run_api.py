from datetime import datetime

import pytest

from tz.client import api

FULLSLUG = "feo-indonesia:nz-2050:run1"

EXAMPLE_PARAMS = [
    dict(
        fullslug=FULLSLUG,
        includes=None,
        start_datetime=None,
        end_datetime=None,
    ),
    dict(
        fullslug=FULLSLUG,
        includes=None,
        start_datetime=datetime(2010, 1, 1),
        end_datetime=None,
    ),
    dict(
        fullslug=FULLSLUG,
        includes=None,
        start_datetime=None,
        end_datetime=datetime(2020, 1, 1),
    ),
    dict(
        fullslug=FULLSLUG,
        includes=None,
        start_datetime=datetime(2010, 1, 1),
        end_datetime=datetime(2020, 1, 1),
    ),
]


@pytest.mark.parametrize("run_params", EXAMPLE_PARAMS)
@pytest.mark.xfail(reason="v2 migration wip")
def test_run_get(run_params):
    run = api.runs.get(**run_params)
    assert isinstance(run, api.schemas.Run)


@pytest.mark.xfail(reason="v2 migration wip")
def test_run_search():
    runs = api.runs.search()
    assert isinstance(runs, list)
    assert isinstance(runs[0], api.schemas.Run)
