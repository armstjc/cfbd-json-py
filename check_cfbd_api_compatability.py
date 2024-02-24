"""
# Creation Date: 10/06/2023 05:23 EDT
# Last Updated Date: 02/17/2024 10:55 PM EDT
# Author: Joseph Armstrong (armstrongjoseph08@gmail.com)
# File Name: check_cfbd_api_compatability.py
# Purpose: Checks if the API Version that this package is designed for
    is the same as the current version of the CFBD API
"""

import json

import requests


def check_cfbd_api_compatability():
    """
    Checks if the CFBD API version that `cfbd-json-py` is compatable with
    is the current version of the CFBD API.

    Parameters
    ----------

    None.

    Usage
    ----------

    Use the `check_cfbd_api_script.py` python script.
    Do not call this script outside of the `cfbd-json-py` GitHub repo.

    Returns
    ----------
    Nothing, unless there is a change in version for the CFBD API,
    in which this function will raise an exception.
    """
    with open("cfbd_api_version.json", "r") as f:
        json_str = f.read()

    json_data = json.loads(json_str)

    cfbd_json_py_version = json_data["current_verson"]
    del json_str, json_data

    cfbd_swagger_json_url = (
        "https://raw.githubusercontent.com" + "/CFBD/cfb-api/main/swagger.json"
    )
    response = requests.get(cfbd_swagger_json_url)

    if response.status_code == 200:
        pass
    elif response.status_code == 401:
        raise ConnectionRefusedError(
            "Could not connect. The connection was refused.\n" +
            "HTTP Status Code 401."
        )
    else:
        raise ConnectionError(
            f"Could not connect.\nHTTP Status code {response.status_code}"
        )
    json_data = response.json()

    cfbd_api_version = json_data["info"]["version"]
    del response, json_data

    print(
        f"Package Compatability Version:\t{cfbd_json_py_version}\n"
        + f"Current CFBD API Version:\t{cfbd_api_version}"
    )

    if cfbd_api_version == cfbd_json_py_version:
        print("Version match confirmed. No need to raise an exception.")
    else:
        print(
            "Version match unconfirmed. "
            + "Raising a `ValueError` exception to make it clear "
            + "that there is a version mismatch."
        )
        raise ValueError(
            "There is a difference "
            + "between the current version of the CFBD API, "
            + "and the version of the CFBD API "
            + "this package is compatable with."
            + "\nIf you see this message, and an issue has not been raised, "
            + "create an issue with the following paramaters:"
            + f"\nTitle: Package needs to be upgraded to {cfbd_api_version}"
            + "\nContent: The `cfbd-json-py` package is compatable "
            + f"with the {cfbd_json_py_version} version of the CFBD API, "
            + f"but the current version of the CFBD API is {cfbd_api_version}."
            f"\nLabel: `enhancement`"
        )


def main():
    check_cfbd_api_compatability()


if __name__ == "__main__":
    main()
