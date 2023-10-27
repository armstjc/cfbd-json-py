# Creation Date: 08/30/2023 01:13 EDT
# Last Updated Date: 10/23/2023 04:09 PM EDT
# Author: Joseph Armstrong (armstrongjoseph08@gmail.com)
# File Name: conferences.py
# Purpose: Houses functions pertaining to CFB conference data within the CFBD API.
####################################################################################################

import pandas as pd
import requests

from cfbd_json_py.utls import get_cfbd_api_token


def get_cfbd_conference_info(
        api_key: str = None,
        api_key_dir: str = None,
        return_as_dict: bool = False):
    """
    Retrives a list of CFB conferences from the CFBD API.

    Parameters
    ----------
    `api_key` (str, optional):
        Semi-optional argument. 
        If `api_key` is null, this function will attempt to load a CFBD API key
        from the python environment, or from a file on this computer.
        If `api_key` is not null, this function will automatically assume that the
        inputted `api_key` is a valid CFBD API key.

    `api_key_dir` (str, optional):
        Optional argument.
        If `api_key` is set to am empty string, this variable is ignored.
        If `api_key_dir` is null, and `api_key` is null, 
        this function will try to find a CFBD API key file in this user's home directory.
        If `api_key_dir` is set to a string, and `api_key` is null,
        this function will assume that `api_key_dir` is a directory, 
        and will try to find a CFBD API key file in that directory.

    `return_as_dict` (bool, semi-optional):
        Semi-optional argument.
        If you want this function to return the data as a dictionary (read: JSON object), 
        instead of a pandas `DataFrame` object,
        set `return_as_dict` to `True`.

    Usage
    ---------- 
    ```
    import time

    from cfbd_json_py.conferences import get_cfbd_conference_info

    cfbd_key = "tigersAreAwsome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwsome":
        print("Using the user's API key declared in this script for this example.")

        # Gets CFB confrence info from the CFBD API.
        print("Gets CFB confrence info from the CFBD API.")
        json_data = get_cfbd_conference_info(api_key=cfbd_key)
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_conference_info(
            api_key=cfbd_key,
            return_as_dict=True)
        print(json_data)

    else:
        # Alternatively, if the CFBD API key exists in this python environment,
        # or it's been set by cfbd_json_py.utls.set_cfbd_api_token(),
        # you could just call these functions directly, without setting the API key
        # in the script.
        print("Using the user's API key suposedly loaded into this python environment for this example.")

        # Gets CFB confrence info from the CFBD API.
        print("Gets CFB confrence info from the CFBD API.")
        json_data = get_cfbd_conference_info()
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_conference_info(return_as_dict=True)
        print(json_data)

    ```

    Returns
    ----------
    A pandas `DataFrame` object with CFB conference data, 
    or (if `return_as_dict` is set to `True`) 
    a dictionary object with CFB conference data.
    """

    conference_df = pd.DataFrame()
    row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/conferences"

    # Input validation
    ########################################################################################################################################################################################################

    if api_key != None:
        real_api_key = api_key
        del api_key
    else:
        real_api_key = get_cfbd_api_token(api_key_dir=api_key_dir)

    if real_api_key == "tigersAreAwsome":
        raise ValueError(
            "You actually need to change `cfbd_key` to your CFBD API key.")
    elif "Bearer " in real_api_key:
        pass
    elif "Bearer" in real_api_key:
        real_api_key = real_api_key.replace('Bearer', 'Bearer ')
    else:
        real_api_key = "Bearer " + real_api_key

    headers = {
        'Authorization': f'{real_api_key}',
        'accept': 'application/json'
    }

    response = requests.get(url, headers=headers)
    

    if response.status_code == 200:
        pass
    elif response.status_code == 401:
        raise ConnectionRefusedError(
            f'Could not connect. The connection was refused.\nHTTP Status Code 401.'
        )
    else:
        raise ConnectionError(
            f'Could not connect.\nHTTP Status code {response.status_code}'
        )

    json_data = response.json()

    if return_as_dict == True:
        return json_data

    for conference in json_data:
        conference_id = conference['id']
        conference_name = conference['name']
        conference_short_name = conference['short_name']
        conference_abbreviation = conference['abbreviation']
        ncaa_classification = conference['classification']

        row_df = pd.DataFrame(
            {
                "conference_id": conference_id,
                "conference_name": conference_name,
                "conference_short_name": conference_short_name,
                "conference_abbreviation": conference_abbreviation,
                "ncaa_classification": ncaa_classification
            }, index=[0]
        )

        conference_df = pd.concat([conference_df, row_df], ignore_index=True)
        del conference_id, conference_name, \
            conference_short_name, conference_abbreviation, \
            ncaa_classification

        del row_df

    return conference_df
