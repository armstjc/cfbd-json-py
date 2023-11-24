# Creation Date: 08/30/2023 01:13 EDT
# Last Updated Date: 11/24/2023 2:55 PM EDT
# Author: Joseph Armstrong (armstrongjoseph08@gmail.com)
# File Name: teams.py
# Purpose: Houses functions pertaining to CFB team data within the CFBD API.
####################################################################################################

from datetime import datetime
import logging
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
        row_df = pd.DataFrame({"team_id": t_team_id}, index=[0])
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

        teams_df = pd.concat([teams_df, row_df], ignore_index=True)

        del row_df
        del t_team_id

    return teams_df


def get_cfbd_fbs_team_list(
        api_key: str = None,
        api_key_dir: str = None,
        season: int = None,
        return_as_dict: bool = False):
    """
    Allows you to get CFB team information for FBS teams from the CFBD API.

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

    `season` (int, optional):
        Optional argument.
        If you only want CFB team information for FBS teams in a specific season,
        set `season` to that season.

    `return_as_dict` (bool, semi-optional):
        Semi-optional argument.
        If you want this function to return the data as a dictionary (read: JSON object), 
        instead of a pandas `DataFrame` object,
        set `return_as_dict` to `True`.

    Usage
    ----------
    ```
    import time

    from cfbd_json_py.teams import get_cfbd_fbs_team_list


    cfbd_key = "tigersAreAwsome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwsome":
        print("Using the user's API key declared in this script for this example.")

        # Get the current list of FBS teams.
        print("Get the current list of FBS teams.")
        json_data = get_cfbd_fbs_team_list(
            api_key=cfbd_key
        )
        print(json_data)
        time.sleep(5)


        # Get a list of FBS teams for the 2020 CFB season.
        print("Get a list of FBS teams for the 2020 CFB season.")
        json_data = get_cfbd_fbs_team_list(
            api_key=cfbd_key,
            season=2020
        )
        print(json_data)
        time.sleep(5)


        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_fbs_team_list(
            api_key=cfbd_key,
            season=1990,
            return_as_dict=True
        )    
        print(json_data)

    else:
        # Alternatively, if the CFBD API key exists in this python environment,
        # or it's been set by cfbd_json_py.utls.set_cfbd_api_token(),
        # you could just call these functions directly, without setting the API key
        # in the script.
        print("Using the user's API key suposedly loaded into this python environment for this example.")

        # Get the current list of FBS teams.
        print("Get the current list of FBS teams.")
        json_data = get_cfbd_fbs_team_list()
        print(json_data)
        time.sleep(5)


        # Get a list of FBS teams for the 2020 CFB season.
        print("Get a list of FBS teams for the 2020 CFB season.")
        json_data = get_cfbd_fbs_team_list(
            season=2020
        )
        print(json_data)
        time.sleep(5)


        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_fbs_team_list(
            season=1990,
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
    url = "https://api.collegefootballdata.com/teams/fbs"

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
    if season != None:
        url += f"?year={season}"

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
        row_df = pd.DataFrame({"team_id": t_team_id}, index=[0])
        row_df['school'] = team['school']
        row_df['school_mascot'] = team['mascot']
        row_df['school_abbreviation'] = team['abbreviation']
        row_df['school_alt_name_1'] = team['alt_name1']
        row_df['school_alt_name_2'] = team['alt_name2']
        row_df['school_alt_name_3'] = team['alt_name3']
        row_df['conference'] = team['conference']
        # row_df['ncaa_classification'] = team['classification']
        row_df['ncaa_classification'] = "fbs"
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

        teams_df = pd.concat([teams_df, row_df], ignore_index=True)

        del row_df
        del t_team_id

    return teams_df


def get_cfbd_team_rosters(
        api_key: str = None,
        api_key_dir: str = None,
        team: str = None,
        season: int = None,
        return_as_dict: bool = False):
    """
    Allows you to get CFB team roster data for FBS teams from the CFBD API.

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

    `season` (int, optional):
        Optional argument.
        If you only want CFB team roster data for FBS teams in a specific season,
        set `season` to that season.

    `team` (str, optional):
        Optional argument.
        If you only want CFB team roster data for a specific CFB team,
        set `team` to that CFB team's name.

    `return_as_dict` (bool, semi-optional):
        Semi-optional argument.
        If you want this function to return the data as a dictionary (read: JSON object), 
        instead of a pandas `DataFrame` object,
        set `return_as_dict` to `True`.

    Usage
    ----------
    ```
    import time

    from cfbd_json_py.teams import get_cfbd_team_rosters


    cfbd_key = "tigersAreAwsome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwsome":
        print("Using the user's API key declared in this script for this example.")

        # Get the team roster for the 2019 LSU Tigers Football Team.
        print("Get the team rosters for the 2020 CFB season.")
        json_data = get_cfbd_team_rosters(
            api_key=cfbd_key,
            season=2020,
            team="LSU"
        )
        print(json_data)
        time.sleep(5)

        # Get the team rosters for the 2020 CFB season.
        print("Get the team rosters for the 2020 CFB season.")
        json_data = get_cfbd_team_rosters(
            api_key=cfbd_key,
            season=2020
        )
        print(json_data)
        time.sleep(5)



        # Get a list of known players with the Ohio State Buckeyes Football Team.
        print("Get a list of known players with the Ohio State Buckeyes Football Team.")
        json_data = get_cfbd_team_rosters(
            api_key=cfbd_key,
            team="Ohio State"
        )
        print(json_data)
        time.sleep(5)


        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_team_rosters(
            api_key=cfbd_key,
            season=2015,
            team="LSU",
            return_as_dict=True
        )    
        print(json_data)

    else:
        # Alternatively, if the CFBD API key exists in this python environment,
        # or it's been set by cfbd_json_py.utls.set_cfbd_api_token(),
        # you could just call these functions directly, without setting the API key
        # in the script.
        print("Using the user's API key suposedly loaded into this python environment for this example.")


        # Get the team roster for the 2019 LSU Tigers Football Team.
        print("Get the team roster for the 2019 LSU Tigers Football Team.")
        json_data = get_cfbd_team_rosters(
            season=2020,
            team="LSU"
        )
        print(json_data)
        time.sleep(5)

        # Get the team rosters for the 2020 CFB season.
        print("Get the team rosters for the 2020 CFB season.")
        json_data = get_cfbd_team_rosters(
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get a list of known players with the Ohio State Buckeyes Football Team.
        print("Get a list of known players with the Ohio State Buckeyes Football Team.")
        json_data = get_cfbd_team_rosters(
            team="Ohio State"
        )
        print(json_data)
        time.sleep(5)


        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_team_rosters(
            season=2015,
            team="LSU",
            return_as_dict=True
        )    
        print(json_data)

    ```
    Returns
    ----------
    A pandas `DataFrame` object with CFB team roster data, 
    or (if `return_as_dict` is set to `True`) 
    a dictionary object with CFB team roster data.

    """
    now = datetime.now()
    roster_df = pd.DataFrame()
    row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/roster"

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

    if season != None and season > (now.year + 1):
        raise ValueError(f"`season` cannot be greater than {season}.")
    elif season != None and season < 1869:
        raise ValueError(f"`season` cannot be less than 1869.")

    # URL builder
    ########################################################################################################################################################################################################
    url_elements = 0

    if season != None and url_elements == 0:
        url += f"?year={season}"
        url_elements += 1
    elif season != None:
        url += f"&year={season}"
        url_elements += 1

    if team != None and url_elements == 0:
        url += f"?team={team}"
        url_elements += 1
    elif team != None:
        url += f"&team={team}"
        url_elements += 1

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

    # for player in tqdm(json_data):
        p_id = player["id"]
        row_df = pd.DataFrame({"player_id": p_id}, index=[0])
        row_df['season'] = season
        row_df['team'] = player['team']
        row_df['player_jersey'] = player['jersey']
        row_df['position'] = player['position']
        row_df['player_first_name'] = player['first_name']
        row_df['player_last_name'] = player['last_name']
        row_df['weight_lbs'] = player['weight']
        row_df['height_in'] = player['height']
        row_df['years_experience'] = player['year']
        row_df['team'] = player['team']
        row_df['player_home_city'] = player['home_city']
        row_df['player_home_state'] = player['home_state']
        row_df['player_home_country'] = player['home_country']
        row_df['player_home_latitude'] = player['home_latitude']
        row_df['player_home_longitude'] = player['home_longitude']
        row_df['player_home_county_fips'] = player['home_county_fips']
        try:
            row_df['player_recruit_ids'] = player['recruit_ids']
        except:
            row_df['player_recruit_ids'] = None

        roster_df = pd.concat([roster_df, row_df], ignore_index=True)
        del row_df
        del p_id
    roster_df = pd.DataFrame(json_data)
    return roster_df


def get_cfbd_team_talent_rankings(
        api_key: str = None,
        api_key_dir: str = None,
        season: int = None,
        return_as_dict: bool = False):
    """
    Get a list of teams, and their overall talent rankings, from the CFBD API.

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

    `season` (int, optional):
        Optional argument.
        If you only want CFB team talent ranking data for FBS teams in a specific season,
        set `season` to that season.

    `return_as_dict` (bool, semi-optional):
        Semi-optional argument.
        If you want this function to return the data as a dictionary (read: JSON object), 
        instead of a pandas `DataFrame` object,
        set `return_as_dict` to `True`.

    Usage
    ----------
    ```
    import time

    from cfbd_json_py.teams import get_cfbd_team_talent_rankings


    cfbd_key = "tigersAreAwsome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwsome":
        print("Using the user's API key declared in this script for this example.")

        # Get team talent rankings data for the 2020 CFB season.
        print("Get team talent rankings data for the 2020 CFB season.")
        json_data = get_cfbd_team_talent_rankings(
            api_key=cfbd_key,
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get team talent rankings data for as many seasons as possible.
        print("Get team talent rankings data for as many seasons as possible.")
        json_data = get_cfbd_team_talent_rankings(
            api_key=cfbd_key
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_team_talent_rankings(
            api_key=cfbd_key,
            season=2015,
            return_as_dict=True
        )    
        print(json_data)

    else:
        # Alternatively, if the CFBD API key exists in this python environment,
        # or it's been set by cfbd_json_py.utls.set_cfbd_api_token(),
        # you could just call these functions directly, without setting the API key
        # in the script.
        print("Using the user's API key suposedly loaded into this python environment for this example.")


        # Get team talent rankings data for the 2020 CFB season.
        print("Get team talent rankings data for the 2020 CFB season.")
        json_data = get_cfbd_team_talent_rankings(
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get team talent rankings data for as many seasons as possible.
        print("Get team talent rankings data for as many seasons as possible.")
        json_data = get_cfbd_team_talent_rankings()
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_team_talent_rankings(
            season=2015,
            return_as_dict=True
        )    
        print(json_data)

    ```
    Returns
    ----------
    A pandas `DataFrame` object with CFB team talent ratings data, 
    or (if `return_as_dict` is set to `True`) 
    a dictionary object with CFB team talent ratings data.
    """
    now = datetime.now()
    teams_df = pd.DataFrame()
    row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/talent"

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

    if season != None and season > (now.year + 1):
        raise ValueError(f"`season` cannot be greater than {season}.")
    elif season != None and season < 1869:
        raise ValueError(f"`season` cannot be less than 1869.")

    # URL builder
    ########################################################################################################################################################################################################

    if season != None:
        url += f"?year={season}"

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

    teams_df = pd.DataFrame(json_data)

    return teams_df


def get_cfbd_team_matchup_history(
        team_1: str,
        team_2: str,
        api_key: str = None,
        api_key_dir: str = None,
        min_season: int = None,
        max_season: int = None,
        return_as_dict: bool = False):
    """
    Get a list of matchups between two teams, from the CFBD API.

    Parameters
    ----------
    `team_1` (str, mandatory):
        Mandatory argument.
        This is the name of the **first** team in this matchup.

    `team_1` (str, mandatory):
        Mandatory argument.
        This is the name of the **second** team in this matchup.

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

    `min_season` (int, optional):
        Optional argument.
        If you only want matchups starting in a specific season, 
        set `min_season` to that season.

    `max_season` (int, optional):
        Optional argument.
        If you only want matchups up to a specific season, 
        set `max_season` to that season.

    `return_as_dict` (bool, semi-optional):
        Semi-optional argument.
        If you want this function to return the data as a dictionary (read: JSON object), 
        instead of a pandas `DataFrame` object,
        set `return_as_dict` to `True`.

    Usage
    ----------
    ```
    import time

    from cfbd_json_py.teams import get_cfbd_team_matchup_history


    cfbd_key = "tigersAreAwsome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwsome":
        print("Using the user's API key declared in this script for this example.")

        # Get the matchup history betwen the University of Cincinnati 
        # and the Miami (OH) Redhawks football teams.
        print("Get the matchup history betwen the University of Cincinnati and the Miami (OH) Redhawks football teams.")
        json_data = get_cfbd_team_matchup_history(
            api_key=cfbd_key,
            team_1="Cincinnati",
            team_2="Miami (OH)"
        )
        print(json_data)
        time.sleep(5)

        # Get the matchup history betwen the Ohio State Buckeyes 
        # and the Michigan Wolverines football teams, 
        # starting in 2002.
        print("Get the matchup history betwen the Ohio State Buckeyes and the University of Michigan Wolverines football teams, starting in 2002.")
        json_data = get_cfbd_team_matchup_history(
            api_key=cfbd_key,
            team_1="Ohio State",
            team_2="Michigan",
            min_season=2002
        )
        print(json_data)
        time.sleep(5)

        # Get the matchup history betwen the Ohio Bobcats 
        # and the Miami (OH) Redhawks football teams,
        # starting in 1990 and ending in 2005.
        print("Get the matchup history betwen the University of Cincinnati and the Miami (OH) Redhawks football teams.")
        json_data = get_cfbd_team_matchup_history(
            api_key=cfbd_key,
            team_1="Ohio",
            team_2="Miami (OH)",
            min_season=1990,
            max_season=2005
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_team_matchup_history(
            api_key=cfbd_key,
            team_1="Cincinnati",
            team_2="Miami (OH)",
            min_season=2020,
            return_as_dict=True
        )    
        print(json_data)

    else:
        # Alternatively, if the CFBD API key exists in this python environment,
        # or it's been set by cfbd_json_py.utls.set_cfbd_api_token(),
        # you could just call these functions directly, without setting the API key
        # in the script.
        print("Using the user's API key suposedly loaded into this python environment for this example.")


        # Get the matchup history betwen the University of Cincinnati 
        # and the Miami (OH) Redhawks football teams.
        print("Get the matchup history betwen the University of Cincinnati and the Miami (OH) Redhawks football teams.")
        json_data = get_cfbd_team_matchup_history(
            team_1="Cincinnati",
            team_2="Miami (OH)"
        )
        print(json_data)
        time.sleep(5)

        # Get the matchup history betwen the Ohio State Buckeyes 
        # and the Michigan Wolverines football teams, 
        # starting in 2002.
        print("Get the matchup history betwen the Ohio State Buckeyes and the University of Michigan Wolverines football teams, starting in 2002.")
        json_data = get_cfbd_team_matchup_history(
            team_1="Ohio State",
            team_2="Michigan",
            min_season=2002
        )
        print(json_data)
        time.sleep(5)

        # Get the matchup history betwen the Ohio Bobcats 
        # and the Miami (OH) Redhawks football teams,
        # starting in 1990 and ending in 2005.
        print("Get the matchup history betwen the University of Cincinnati and the Miami (OH) Redhawks football teams.")
        json_data = get_cfbd_team_matchup_history(
            team_1="Ohio",
            team_2="Miami (OH)",
            min_season=1990,
            max_season=2005
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_team_matchup_history(
            team_1="Cincinnati",
            team_2="Miami (OH)",
            min_season=2020,
            return_as_dict=True
        )    
        print(json_data)
    ```
    Returns
    ----------
    A pandas `DataFrame` object with CFB team matchup data, 
    or (if `return_as_dict` is set to `True`)
    a dictionary object with CFB team matchup data.
    """
    now = datetime.now()
    matchups_df = pd.DataFrame()
    row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/teams/matchup"

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

    if min_season != None and min_season > (now.year + 1):
        raise ValueError(f"`min_season` cannot be greater than {min_season}.")
    elif min_season != None and min_season < 1869:
        raise ValueError(f"`min_season` cannot be less than 1869.")

    if max_season != None and max_season > (now.year + 1):
        raise ValueError(f"`max_season` cannot be greater than {max_season}.")
    elif max_season != None and max_season < 1869:
        raise ValueError(f"`max_season` cannot be less than 1869.")

    # URL builder
    ########################################################################################################################################################################################################

    # Required by the API:
    url += f"?team1={team_1}&team2={team_2}"

    if min_season != None:
        url += f"&minYear={min_season}"

    if max_season != None:
        url += f"&maxYear={max_season}"

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

    team_1_wins = json_data['team1Wins']
    team_2_wins = json_data['team2Wins']
    total_ties = json_data['ties']

    for game in tqdm(json_data['games']):
        row_df = pd.DataFrame(
            {
                "team_1": team_1,
                "team_2": team_2,
                "start_year": min_season,
                "end_year": max_season,
                "team_1_wins": team_1_wins,
                "team_2_wins": team_2_wins,
                "ties": total_ties
            }, index=[0]
        )
        row_df['season'] = game['season']
        row_df['week'] = game['week']
        row_df['season_type'] = game['seasonType']
        row_df['date'] = game['date']
        row_df['is_neutral_site_game'] = game['neutralSite']
        row_df['venue'] = game['venue']
        row_df['home_team'] = game['homeTeam']
        row_df['home_score'] = game['homeScore']
        row_df['away_team'] = game['awayTeam']
        row_df['away_score'] = game['awayScore']
        row_df['winner'] = game['winner']

        matchups_df = pd.concat([matchups_df, row_df], ignore_index=True)
        del row_df

    return matchups_df
