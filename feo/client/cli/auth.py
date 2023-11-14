import json
import os

import click
import requests

from feo.client.auth import login as auth_login
from feo.client.cli.cli import root


@root.group()
@click.pass_obj
def auth(config):
    """Authentication operations"""


@auth.command()
@click.pass_obj
def login(config):
    """
    Runs the device authorization flow, writes a long-expirey
    JWT to a new hidden folder in the $HOME directory
    """

    auth_login()


@auth.command()
@click.pass_obj
def test(config):
    URL = "https://power-legacy.feo.transitionzero.org"
    token = json.load(open(os.path.join(os.path.expanduser("~"), ".tz-feo", "token.json")))

    headers = {"Authorization": "Bearer {}".format(token["access_token"])}

    params = {"admin_0": "ID", "page": 3, "limit": 5}

    r = requests.get(URL + "/units/", params=params, headers=headers, timeout=30)

    print(r.status_code)
    units = json.loads(r.text)["units"]
    print(units)
