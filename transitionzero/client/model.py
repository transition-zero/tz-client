"""Example NumPy style docstrings.

This module demonstrates documentation as specified by the `NumPy
Documentation HOWTO`_. Docstrings may extend over multiple lines. Sections
are created with a section header followed by an underline of equal length.

Example
-------
Examples can be given using either the ``Example`` or ``Examples``
sections. Sections support any reStructuredText formatting, including
literal blocks::

    $ python example_numpy.py


Section breaks are created with two blank lines. Section breaks are also
implicitly created anytime a new section starts. Section bodies *may* be
indented:

Notes
-----
    This is an example of an indented section. It's like any other section,
    but the body is indented to help it stand out from surrounding text.

If a section is indented, then a section break is created by
resuming unindented text.

Attributes
----------
module_level_variable1 : int
    Module level variables may be documented in either the ``Attributes``
    section of the module docstring, or in an inline docstring immediately
    following the variable.

    Either form is acceptable, but the two should not be mixed. Choose
    one convention to document module level variables and be consistent
    with it.


.. _NumPy docstring standard:
   https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard

"""


import os
from typing import Optional

import httpx

from transitionzero.client.base import Base


class Model(Base):
    """A desc that fits on one line

    Attributes
    ----------
    headers : dict
        Authorisation headers inherited from transitionzero.client.base
    client : httpx.Client
        An httpx client instance with the base_url set to the model-results FEO endpoint

    Methods
    -------
    search_model_runs(model_id=None, scenario_id=None, owner=None, public=None, limit=None, page=None)
        Searches for available model runs using the FEO API

    """

    def __init__(self):
        super().__init__()
        self.client = httpx.Client(
            base_url=os.environ.get(
                "FEO_MODEL_URL", "https://model-results.feo.transitionzero.org/"
            ),
            headers=self.headers,
        )

    def search_model_runs(
        self,
        model_id: Optional[str],
        scenario_id: Optional[str],
        owner: Optional[str],
        public: Optional[bool],
        limit: Optional[int],
        page: Optional[int],
    ):
        """Searches for available model runs using the FEO API.

        Parameters
        ----------
            model_id : Optional[str]
                Any model_id to filter search results by.
            scenario_id : Optional[str]
                Any scenario_id to filter search results by.
            owner : Optional[str]
                Any model_run owner to filter search results by.
            public : Optional[bool]
                Whether to filter results to return only those that are public.
            limit : Optional[int]
                The number of search results to obtain; default: 5, max: 10.
            page : Optional[int]
                The page number of the search results to obtain.

        Returns
        -------
        List[transitionzero.schemas.RunId]

        """

        r = self.client.get(
            "v1/model_run/",
            params={
                "model_id": model_id,
                "scenario_id": scenario_id,
                "owner": owner,
                "public": public,
                "limit": limit,
                "page": page,
            },
        )

        self.catch_errors(r)

        return r.json()

    def get_model_run(self, uuid: str, includes: str):
        """
        Acquires model_run data from the FEO API.

        Parameters
        ----------
            uuid : str
                The uuid of the model_run.
            includes : str
                Comma-separated optional data to include in the returned object, some combination of ["generation","capacity","flows","metrics"].

        Returns
        -------
        transitionzero.schemas.Run

        """

        r = self.client.get(f"v1/model_run/{uuid}")

        self.catch_errors(r)

        return r.json()
