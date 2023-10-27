# Creation Date: 08/30/2023 01:13 EDT
# Last Updated Date: 10/23/2023 04:09 PM EDT
# Author: Joseph Armstrong (armstrongjoseph08@gmail.com)
# File Name: draft.py
# Purpose: Houses functions pertaining to NFL Draft data within the CFBD API.
####################################################################################################

from datetime import datetime
import logging
import pandas as pd
import requests
from tqdm import tqdm

from cfbd_json_py.utls import get_cfbd_api_token


def get_cfbd_nfl_teams(
        api_key: str = None,
        api_key_dir: str = None,
        return_as_dict: bool = False):
    """
    Retrives a list of NFL teams from the CFBD API.

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

    from cfbd_json_py.draft import get_cfbd_nfl_teams

    cfbd_key = "tigersAreAwsome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwsome":
        print("Using the user's API key declared in this script for this example.")

        # Gets NFL team info from the CFBD API.
        print("Gets NFL team info from the CFBD API.")
        json_data = get_cfbd_nfl_teams(api_key=cfbd_key)
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_nfl_teams(
            api_key=cfbd_key,
            return_as_dict=True)
        print(json_data)

    else:
        # Alternatively, if the CFBD API key exists in this python environment,
        # or it's been set by cfbd_json_py.utls.set_cfbd_api_token(),
        # you could just call these functions directly, without setting the API key
        # in the script.
        print("Using the user's API key suposedly loaded into this python environment for this example.")

        # Gets NFL team info from the CFBD API.
        print("Gets NFL team info from the CFBD API.")
        json_data = get_cfbd_nfl_teams()
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_nfl_teams(return_as_dict=True)
        print(json_data)

    ```    

    Returns
    ----------
    A pandas `DataFrame` object with NFL team data, 
    or (if `return_as_dict` is set to `True`) 
    a dictionary object with NFL team data.

    """

    nfl_teams_df = pd.DataFrame()
    row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/draft/teams"

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

    for nfl_team in json_data:
        nfl_team_location = nfl_team['location']
        nfl_team_nickname = nfl_team['nickname']
        nfl_team_display_name = nfl_team['displayName']
        nfl_team_logo = nfl_team['logo']

        row_df = pd.DataFrame(
            {
                "nfl_team_location": nfl_team_location,
                "nfl_team_nickname": nfl_team_nickname,
                "nfl_team_display_name": nfl_team_display_name,
                "nfl_team_logo": nfl_team_logo
            }, index=[0]
        )

        nfl_teams_df = pd.concat([nfl_teams_df, row_df], ignore_index=True)

        del nfl_team_location, nfl_team_nickname, \
            nfl_team_display_name, nfl_team_logo

        del row_df

    return nfl_teams_df


def get_cfbd_nfl_positions(
        api_key: str = None,
        api_key_dir: str = None,
        return_as_dict: bool = False):
    """
    Retrives a list of player positions for the NFL Draft from the CFBD API.

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

    from cfbd_json_py.draft import get_cfbd_nfl_positions

    cfbd_key = "tigersAreAwsome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwsome":
        print("Using the user's API key declared in this script for this example.")

        # Gets a list of player positions for the NFL Draft from the CFBD API.
        print("Gets a list of player positions for the NFL Draft from the CFBD API.")
        json_data = get_cfbd_nfl_positions(api_key=cfbd_key)
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_nfl_positions(
            api_key=cfbd_key,
            return_as_dict=True)
        print(json_data)

    else:
        # Alternatively, if the CFBD API key exists in this python environment,
        # or it's been set by cfbd_json_py.utls.set_cfbd_api_token(),
        # you could just call these functions directly, without setting the API key
        # in the script.
        print("Using the user's API key suposedly loaded into this python environment for this example.")

        # Gets a list of player positions for the NFL Draft from the CFBD API.
        print("Gets a list of player positions for the NFL Draft from the CFBD API.")
        json_data = get_cfbd_nfl_positions()
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_nfl_positions(return_as_dict=True)
        print(json_data)

    ```
    Returns
    ----------
    A pandas `DataFrame` object with player position data, 
    or (if `return_as_dict` is set to `True`) 
    a dictionary object with player position data.

    """

    positions_df = pd.DataFrame()
    row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/draft/positions"

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

    for p in json_data:
        position_name = p['name']
        position_abbreviation = p['abbreviation']

        row_df = pd.DataFrame(
            {
                "position_name": position_name,
                "position_abbreviation": position_abbreviation
            }, index=[0]
        )
        positions_df = pd.concat([positions_df, row_df], ignore_index=True)

        del position_name, position_abbreviation
        del row_df

    return positions_df


def get_cfbd_nfl_draft_info(
        api_key: str = None,
        api_key_dir: str = None,
        season: int = None,
        nfl_team: str = None,
        college: str = None,
        conference_abv: str = None,
        position: str = None,
        return_as_dict: bool = False):
    """
    Retrives a list of actual NFL Draft selections from the CFBD API.

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

    The following paramaters are optional, but it is highly reccomended to not call this function
    withiout settting one of these five optional paramaters to a non-null value.

    `season` (int, semi-optional):
        Semi-Optional argument. 
        This is the season you want NFL Draft information for. For example, if you only want 
        data for the 2020 NFL Draft, set `season` to `2020`.

    `nfl_team` (str, optional):
        Semi-Optional argument.
        If you only want NFL Draft selections from a specific NFL team, set `nfl_team` to the 
        name of that team. For example, if you want to only get NFL Draft information for 
        draft picks made by the Cincinnati Bengals, set `nfl_team` to `Cincinnati`.

    `college` (str, optional):
        Semi-Optional argument.
        If you only want NFL Draft selections from a specific CFB team, set `college` to the 
        name of that team. For example, if you want to only get NFL Draft information for 
        draft picks from the Clemson Tigers Football Program, set `college` to `Clemson`.

    `conference` (str, optional):
        Semi-Optional argument.
        If you only want NFL Draft selections from a specific CFB confrence, set `conference` to the abbreviation of that confrence. 
        A list of CFBD API confrence abbreviations can be found in the `conference_abbreviation` column from 
        the pandas DataFrame that is returned by calling `cfbd_json_py.conferences.get_cfbd_conference_info()`.
        For example, if you want to only get NFL Draft information for 
        draft picks that played in the Big 12, set `confrence` to `B12`.

    `position` (str, optional):
        Semi-Optional argument.
        If you only want NFL Draft selections who played a specific position, 
        set `position` to that position's abbreviation. 
        A list of CFBD API positions can be found in the `position_abbreviation` column from 
        the pandas DataFrame that is returned by calling `cfbd_json_py.draft.get_cfbd_nfl_positions()`.

    `return_as_dict` (bool, semi-optional):
        Semi-optional argument.
        If you want this function to return the data as a dictionary (read: JSON object), 
        instead of a pandas `DataFrame` object,
        set `return_as_dict` to `True`.
    Usage
    ---------- 

    ```
    import time

    from cfbd_json_py.draft import get_cfbd_nfl_draft_info

    cfbd_key = "tigersAreAwsome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwsome":
        print("Using the user's API key declared in this script for this example.")

        # Get NFL Draft selections from the 2020 NFL Draft.
        print("Get NFL Draft selections from the 2020 NFL Draft.")
        json_data = get_cfbd_nfl_draft_info(
            api_key=cfbd_key,
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get NFL Draft selections from the 2020 NFL Draft made by the
        # 2020 Cincinnati Bengals.
        print("Get NFL Draft selections from the 2020 NFL Draft made by the 2020 Cincinnati Bengals.")
        json_data = get_cfbd_nfl_draft_info(
            api_key=cfbd_key,
            season=2020,
            nfl_team="Cincinnati"
        )
        print(json_data)
        time.sleep(5)

        # Get NFL Draft selections from the 2020 NFL Draft made involving
        # Clemson Tigers football players.
        print("Get NFL Draft selections from the 2020 NFL Draft made involving Clemson Tigers football players.")
        json_data = get_cfbd_nfl_draft_info(
            api_key=cfbd_key,
            season=2020,
            college="Clemson"
        )
        print(json_data)
        time.sleep(5)

        # Get NFL Draft selections from the 2020 NFL Draft made involving
        # players who played in the Southeastern Confrence (SEC).
        print("Get NFL Draft selections from the 2020 NFL Draft made involving players who played in the Southeastern Confrence (SEC).")
        json_data = get_cfbd_nfl_draft_info(
            api_key=cfbd_key,
            season=2020,
            conference="SEC"
        )
        print(json_data)
        time.sleep(5)

        # Get NFL Draft selections from the 2020 NFL Draft made
        # where the selected player was a QB in college.
        print("Get NFL Draft selections from the 2020 NFL Draft made where the selected player was a QB in college.")
        json_data = get_cfbd_nfl_draft_info(
            api_key=cfbd_key,
            season=2020,
            position="QB"
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_nfl_draft_info(
            season=2020,
            position="QB",
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

        # Get NFL Draft selections from the 2020 NFL Draft.
        print("Get NFL Draft selections from the 2020 NFL Draft.")
        json_data = get_cfbd_nfl_draft_info(season=2020)
        print(json_data)
        time.sleep(5)

        # Get NFL Draft selections from the 2020 NFL Draft made by the
        # 2020 Cincinnati Bengals.
        print("Get NFL Draft selections from the 2020 NFL Draft made by the 2020 Cincinnati Bengals.")
        json_data = get_cfbd_nfl_draft_info(
            season=2020,
            nfl_team="Cincinnati"
        )
        print(json_data)
        time.sleep(5)

        # Get NFL Draft selections from the 2020 NFL Draft made involving
        # Clemson Tigers football players.
        print("Get NFL Draft selections from the 2020 NFL Draft made involving Clemson Tigers football players.")
        json_data = get_cfbd_nfl_draft_info(
            season=2020,
            college="Clemson"
        )
        print(json_data)
        time.sleep(5)

        # Get NFL Draft selections from the 2020 NFL Draft made involving
        # players who played in the Southeastern Confrence (SEC).
        print("Get NFL Draft selections from the 2020 NFL Draft made involving players who played in the Southeastern Confrence (SEC).")
        json_data = get_cfbd_nfl_draft_info(
            season=2020,
            conference="SEC"
        )
        print(json_data)
        time.sleep(5)

        # Get NFL Draft selections from the 2020 NFL Draft made
        # where the selected player was a QB in college.
        print("Get NFL Draft selections from the 2020 NFL Draft made where the selected player was a QB in college.")
        json_data = get_cfbd_nfl_draft_info(
            season=2020,
            position="QB"
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_nfl_draft_info(
            season=2020,
            position="QB",
            return_as_dict=True
        )
        print(json_data)
    ```

    Returns
    ----------
    A pandas `DataFrame` object with NFL Draft selection data, 
    or (if `return_as_dict` is set to `True`) 
    a dictionary object with NFL Draft selection data.

    """
    now = datetime.now()
    nfl_draft_df = pd.DataFrame()
    row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/draft/picks"

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

    if season == None and nfl_team == None and college == None and conference_abv == None:
        logging.warning(
            "Not specifying a `season`, `nfl_team`, `college`, or `confrence` will still result in a successful get request (assuming the API key is valid)" +
            ", but this is not a recomended method of calling this function.")

    if season < 1936 or season > now.year:
        raise ValueError(
            f"`season` must be an integer between 1936 and {now.year}.\nYou entered:\n{season}")

    # URL builder
    ########################################################################################################################################################################################################
    url_elements = 0

    if season != None and url_elements == 0:
        url += f"?year={season}"
        url_elements += 1
    elif season != None:
        url += f"&year={season}"
        url_elements += 1

    if nfl_team != None and url_elements == 0:
        url += f"?nflTeam={nfl_team}"  # nfl_team = "Cincinnati", not "CIN"
        url_elements += 1
    elif nfl_team != None:
        url += f"&nflTeam={nfl_team}"
        url_elements += 1

    if college != None and url_elements == 0:
        url += f"?college={college}"
        url_elements += 1
    elif college != None:
        url += f"&college={college}"
        url_elements += 1

    if conference_abv != None and url_elements == 0:
        # conference = "SEC", not "Southeastern Confrence"
        url += f"?conference={conference_abv}"
        url_elements += 1
    elif conference_abv != None:
        url += f"&conference={conference_abv}"
        url_elements += 1

    if position != None and url_elements == 0:
        url += f"?position={position}"
        url_elements += 1
    elif position != None:
        url += f"&position={position}"
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

    for p in tqdm(json_data):
        college_athlete_id = p['collegeAthleteId']
        row_df = pd.DataFrame(
            {
                "college_athlete_id": college_athlete_id
            }, index=[0]
        )
        del college_athlete_id

        row_df['nfl_athlete_id'] = p['nflAthleteId']
        row_df['college_id'] = p['collegeId']
        row_df['college_team'] = p['collegeTeam']
        row_df['college_conference'] = p['collegeConference']
        row_df['nfl_team'] = p['nflTeam']
        row_df['draft_year'] = p['year']
        row_df['draft_pick_overall'] = p['overall']
        row_df['draft_round'] = p['round']
        row_df['draft_round_pick'] = p['pick']
        row_df['player_name'] = p['name']
        row_df['player_position'] = p['position']
        row_df['player_height'] = p['height']
        row_df['player_weight'] = p['weight']
        row_df['pre_draft_ranking'] = p['preDraftRanking']
        row_df['pre_draft_position_ranking'] = p['preDraftPositionRanking']
        row_df['pre_draft_grade'] = p['preDraftGrade']
        row_df['player_hometown_city'] = p['hometownInfo']['city']
        row_df['player_hometown_state'] = p['hometownInfo']['state']
        row_df['player_hometown_country'] = p['hometownInfo']['country']
        row_df['player_hometown_latitude'] = p['hometownInfo']['latitude']
        row_df['player_hometown_longitude'] = p['hometownInfo']['longitude']
        row_df['player_hometown_county_fips'] = p['hometownInfo']['countyFips']

        nfl_draft_df = pd.concat([nfl_draft_df, row_df], ignore_index=True)
        del row_df

    if len(nfl_draft_df) == 0:
        logging.error(
            "The CFBD API accepted your inputs, " +
            "but found no data within your specified input paramaters." +
            " Please double check your input paramaters."
        )

    return nfl_draft_df
