# Creation Date: 08/30/2023 01:13 EDT
# Last Updated Date: 11/24/2023 12:55 PM EDT
# Author: Joseph Armstrong (armstrongjoseph08@gmail.com)
# File Name: teams.py
# Purpose: Houses functions pertaining to CFB team data within the CFBD API.
####################################################################################################

from datetime import datetime
import numpy as np
import warnings

import pandas as pd
import requests
from tqdm import tqdm
from cfbd_json_py.utls import get_cfbd_api_token


def get_cfbd_team_information(
        api_key: str = None,
        api_key_dir: str = None,
        conference_abv: str = None,
        return_as_dict: bool = False):
    """
    Allows you to get CFB team information from the CFBD API.
    
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

    `conference_abv` (str, optional):
        Optional argument.
        If you only want CFB team information from a specific confrence, 
        set `conference_abv` to the abbreviation 
        of the conference you want CFB team information from.
        For a list of confrences, 
        use the `cfbd_json_py.conferences.get_cfbd_conference_info()`
        function.

    `return_as_dict` (bool, semi-optional):
        Semi-optional argument.
        If you want this function to return the data as a dictionary (read: JSON object), 
        instead of a pandas `DataFrame` object,
        set `return_as_dict` to `True`.

    Usage
    ----------
    ```
    import time

    from cfbd_json_py.teams import get_cfbd_team_information


    cfbd_key = "tigersAreAwsome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwsome":
        print("Using the user's API key declared in this script for this example.")

        # Get CFB team information for all known CFB teams.
        print("Get CFB team information for all known CFB teams.")
        json_data = get_cfbd_team_information(
            api_key=cfbd_key
        )
        print(json_data)
        time.sleep(5)


        # Get CFB team information for all known Southeastern Confrence (SEC) CFB teams.
        print("Get CFB team information for all known Southeastern Confrence (SEC) CFB teams.")
        json_data = get_cfbd_team_information(
            api_key=cfbd_key,
            conference_abv="SEC"
        )
        print(json_data)
        time.sleep(5)


        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_team_information(
            api_key=cfbd_key,
            conference_abv="B1G",
            return_as_dict=True
        )    
        print(json_data)

    else:
        # Alternatively, if the CFBD API key exists in this python environment,
        # or it's been set by cfbd_json_py.utls.set_cfbd_api_token(),
        # you could just call these functions directly, without setting the API key
        # in the script.
        print("Using the user's API key suposedly loaded into this python environment for this example.")

        # Get CFB team information for all known CFB teams.
        print("Get CFB team information for all known CFB teams.")
        json_data = get_cfbd_team_information()
        print(json_data)
        time.sleep(5)


        # Get CFB team information for all known Southeastern Confrence (SEC) CFB teams.
        print("Get CFB team information for all known Southeastern Confrence (SEC) CFB teams.")
        json_data = get_cfbd_team_information(
            conference_abv="SEC"
        )
        print(json_data)
        time.sleep(5)


        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_team_information(
            conference_abv="B1G",
            return_as_dict=True
        )    
        print(json_data)

    ```
    Returns
    ----------
    A pandas `DataFrame` object with CFB team information, 
    or (if `return_as_dict` is set to `True`) 
    a dictionary object with CFB team information.

    """
    warnings.simplefilter(action='ignore', category=FutureWarning)
    
    teams_df = pd.DataFrame()
    row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/teams"

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
    # URL builder
    ########################################################################################################################################################################################################
    if conference_abv != None:
        url += f"?conference={conference_abv}"

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

    for team in tqdm(json_data):
        t_team_id = team['id']
        row_df = pd.DataFrame({"team_id":t_team_id},index=[0])
        row_df['school'] = team['school']
        row_df['school_mascot'] = team['mascot']
        row_df['school_abbreviation'] = team['abbreviation']
        row_df['school_alt_name_1'] = team['alt_name1']
        row_df['school_alt_name_2'] = team['alt_name2']
        row_df['school_alt_name_3'] = team['alt_name3']
        row_df['conference'] = team['conference']
        row_df['ncaa_classification'] = team['classification']
        row_df['school_primary_color'] = team['color']
        row_df['school_alt_color'] = team['alt_color']
        try:
            row_df['school_primary_logo'] = team['logos'][0]
        except:
            row_df['school_primary_logo'] = np.NaN

        try:
            row_df['school_primary_logo'] = team['logos'][1]
        except:
            row_df['school_primary_logo'] = np.NaN

        row_df['school_twitter'] = team['twitter']
        row_df['home_venue_id'] = team['location']['venue_id']
        row_df['home_venue_name'] = team['location']['name']
        row_df['home_venue_capacity'] = team['location']['capacity']
        row_df['home_venue_year_constructed'] = team['location']['capacity']
        row_df['is_home_venue_grass'] = team['location']['grass']
        row_df['is_home_venue_dome'] = team['location']['dome']
        row_df['city'] = team['location']['city']
        row_df['state'] = team['location']['state']
        row_df['zip'] = team['location']['zip']
        row_df['country_code'] = team['location']['country_code']
        row_df['timezone'] = team['location']['timezone']
        row_df['latitude'] = team['location']['latitude']
        row_df['longitude'] = team['location']['longitude']
        row_df['elevation'] = team['location']['elevation']

        teams_df = pd.concat([teams_df,row_df],ignore_index=True)
        
        del row_df
        del t_team_id

    return teams_df 

def get_cfbd_fbs_team_list(
        api_key: str = None,
        api_key_dir: str = None,
        season: int = None,

        return_as_dict: bool = False):
    """

    """
    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )


def get_cfbd_team_rosters(
        api_key: str = None,
        api_key_dir: str = None,
        team: str = None,
        season: int = None,

        return_as_dict: bool = False):
    """

    """
    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )


def get_cfbd_team_talent_rankings(
        api_key: str = None,
        api_key_dir: str = None,
        season: int = None,

        return_as_dict: bool = False):
    """

    """
    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )


def get_cfbd_team_matchup_history(
        team_1: str,
        team_2: str,
        api_key: str = None,
        api_key_dir: str = None,
        min_season: int = None,
        max_season: int = None,

        return_as_dict: bool = False):
    """

    """
    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )
