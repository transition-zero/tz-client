from datetime import datetime

import pytest

from tz.client import api, utils

if utils.ENVIRONMENT == "staging":
    FULLSLUG = "feo-global-indonesia:feo-indonesia-current-policies:demo"
elif utils.ENVIRONMENT == "production":
    FULLSLUG = "feo-global-indonesia:net-zero-2060:main"
else:
    raise ValueError("Unknown environment")

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
