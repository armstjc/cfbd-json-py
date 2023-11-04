# Creation Date: 08/30/2023 01:13 EDT
# Last Updated Date: 10/15/2023 06:57 PM EDT
# Author: Joseph Armstrong (armstrongjoseph08@gmail.com)
# File Name: venues.py
# Purpose: Houses functions pertaining to CFB team venues/stadium data within the CFBD API.
####################################################################################################

import pandas as pd
import requests

from cfbd_json_py.utls import get_cfbd_api_token


def get_cfbd_venues(
        api_key: str = None,
        api_key_dir: str = None,
        return_as_dict: bool = False):
    """
    Allows a user to get CFB venue/stadium information from the CFBD API.

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

    from cfbd_json_py.venues import get_cfbd_venues


    cfbd_key = "tigersAreAwsome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwsome":
        print("Using the user's API key declared in this script for this example.")

        # Get CFB venue/stadium data from the CFBD API.
        print("Get CFB venue/stadium data from the CFBD API.")
        json_data = get_cfbd_venues(
            api_key=cfbd_key
        )
        print(json_data)
        time.sleep(5)


        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_venues(
            api_key=cfbd_key,
            return_as_dict=True
        )
        print(json_data)

    else:
        # Alternatively, if the CFBD API key exists in this python environment,
        # or it's been set by cfbd_json_py.utls.set_cfbd_api_token(),
        # you could just call these functions directly, without setting the API key
        # in the script.
        print("Using the user's API key suposedly loaded into this python environment for this example.")

        # Get CFB venue/stadium data from the CFBD API.
        print("Get CFB venue/stadium data from the CFBD API.")
        json_data = get_cfbd_venues()
        print(json_data)
        time.sleep(5)


        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_venues(
            return_as_dict=True
        )
        print(json_data)


    ```
    Returns
    ----------
    A pandas `DataFrame` object with CFB venue/stadium information, 
    or (if `return_as_dict` is set to `True`) 
    a dictionary object with with CFB venue/stadium information.

    """
    venue_df = pd.DataFrame()
    row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/venues"

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

    ########################################################################################################################################################################################################
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

    for v in json_data:
        v_id = v['id']
        row_df = pd.DataFrame({"venue_id":v_id},index=[0])
        row_df['venue_name'] = v['name']
        row_df['venue_capacity'] = v['capacity']
        row_df['is_grass'] = v['grass']
        row_df['venue_city'] = v['city']
        row_df['venue_state'] = v['state']
        row_df['venue_zip_code'] = v['zip']
        row_df['venue_country_code'] = v['country_code']
        
        try:
            row_df['venue_location_x'] = v['location']['x']
        except:
            row_df['venue_location_x'] = None

        try:
            row_df['venue_location_y'] = v['location']['y']
        except:
            row_df['venue_location_y'] = None

        row_df['venue_elevation'] = v['elevation']
        row_df['year_constructed'] = v['year_constructed']
        row_df['is_dome'] = v['dome']
        row_df['timezone'] = v['timezone']
        

        venue_df = pd.concat([venue_df,row_df],ignore_index=True)
        del row_df
        del v_id

    return venue_df