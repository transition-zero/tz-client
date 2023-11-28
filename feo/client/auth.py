import json
import os
import time

import requests

from feo.client.core import logger

AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "HhT6aGS8u3Pg4PkVQ8sKUtnrtg0x7nUk")
AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "prod-feo-tz.eu.auth0.com")
AUTH0_AUDIENCE = os.environ.get("AUTH0_AUDIENCE", "https://api.feo.transitionzero.org")
ALGORITHMS = ["RS256"]


def login(config=None):
    """
    Runs the device authorization flow, writes a long-expiry JWT
    to a new hidden folder in the $HOME directory
    """

    token_dir = os.path.join(os.path.expanduser("~"), ".tz-feo")

    if not os.path.exists(token_dir):
        logger.info(f"Writing token directory {token_dir}")
        os.makedirs(token_dir)

    device_code_payload = {
        "client_id": AUTH0_CLIENT_ID,
        "scope": "openid profile offline_access",
        "audience": AUTH0_AUDIENCE,
    }

    device_code_response = requests.post(
        f"https://{AUTH0_DOMAIN}/oauth/device/code", json=device_code_payload, timeout=30  # noqa
    )
    device_code_response.raise_for_status()

    if device_code_response.status_code != 200:
        logger.error("Error generating the device code")
        raise ValueError("Error generating device code")

    logger.info("Device code successful")
    device_code_data = device_code_response.json()
    print("1. In a browser navigate to: ", device_code_data["verification_uri_complete"])
    print("2. Enter the following code: ", device_code_data["user_code"])

    token_payload = {
        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
        "device_code": device_code_data["device_code"],
        "client_id": AUTH0_CLIENT_ID,
        "audience": AUTH0_AUDIENCE,
    }

    authenticated = False
    print("Checking for authentication", end="")
    while not authenticated:
        token_response = requests.post(
            f"https://{AUTH0_DOMAIN}/oauth/token", data=token_payload, timeout=30  # noqa
        )

        token_data = token_response.json()
        if token_response.status_code == 200:
            print("Authenticated!")
            print("- Id Token: {}...".format(token_data["id_token"][:10]))
            authenticated = True
        elif token_data["error"] not in ("authorization_pending", "slow_down"):
            print(token_data["error_description"])
            raise ValueError("Error generating device code")
        else:
            print(".", end="")
            time.sleep(device_code_data["interval"])

    # success!
    # TODO: use our new token to fetch our current_user
    # display a friendly welcome... print ('Hello {name}!')

    # write token data to file
    json.dump(
        token_data,
        open(os.path.join(os.path.expanduser("~"), ".tz-feo", "token.json"), "w"),
    )
