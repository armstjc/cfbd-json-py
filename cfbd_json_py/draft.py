# Creation Date: 08/30/2023 01:13 EDT
# Last Updated Date: 08/13/2024 02:10 PM EDT
# Author: Joseph Armstrong (armstrongjoseph08@gmail.com)
# File Name: draft.py
# Purpose: Houses functions pertaining to NFL Draft data within the CFBD API.
###############################################################################

import logging
from datetime import datetime

import pandas as pd
import requests

# from tqdm import tqdm
from cfbd_json_py.utls import get_cfbd_api_token


def get_cfbd_nfl_teams(
    api_key: str = None, api_key_dir: str = None, return_as_dict: bool = False
):
    """
    Retrieves a list of NFL teams from the CFBD API.

    Parameters
    ----------
    `api_key` (str, optional):
        Semi-optional argument.
        If `api_key` is null, this function will attempt to load a CFBD API key
        from the python environment, or from a file on this computer.
        If `api_key` is not null,
        this function will automatically assume that the
        inputted `api_key` is a valid CFBD API key.

    `api_key_dir` (str, optional):
        Optional argument.
        If `api_key` is set to am empty string, this variable is ignored.
        If `api_key_dir` is null, and `api_key` is null,
        this function will try to find
        a CFBD API key file in this user's home directory.
        If `api_key_dir` is set to a string, and `api_key` is null,
        this function will assume that `api_key_dir` is a directory,
        and will try to find a CFBD API key file in that directory.

    `return_as_dict` (bool, semi-optional):
        Semi-optional argument.
        If you want this function to return the data
        as a dictionary (read: JSON object),
        instead of a pandas `DataFrame` object,
        set `return_as_dict` to `True`.

    Usage
    ----------
    ```
    import time

    from cfbd_json_py.draft import get_cfbd_nfl_teams

    cfbd_key = "tigersAreAwesome"  # placeholder for your CFBD API Key.

    if cfbd_key is not "tigersAreAwesome":
        print(
            "Using the user's API key declared in this script " +
            "for this example."
        )

        # Gets NFL team info from the CFBD API.
        print("Gets NFL team info from the CFBD API.")
        json_data = get_cfbd_nfl_teams(api_key=cfbd_key)
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call
        # as a Dictionary (read: JSON) object.
        print(
            "You can also tell this function to just return the API call " +
            "as a Dictionary (read: JSON) object."
        )
        json_data = get_cfbd_nfl_teams(
            api_key=cfbd_key,
            return_as_dict=True)
        print(json_data)

    else:
        # Alternatively, if the CFBD API key exists in this python environment,
        # or it's been set by cfbd_json_py.utls.set_cfbd_api_token(),
        # you could just call these functions directly,
        # without setting the API key in the script.
        print(
            "Using the user's API key supposedly loaded into " +
            "this python environment for this example."
        )

        # Gets NFL team info from the CFBD API.
        print("Gets NFL team info from the CFBD API.")
        json_data = get_cfbd_nfl_teams()
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call
        # as a Dictionary (read: JSON) object.
        print(
            "You can also tell this function to just return the API call " +
            "as a Dictionary (read: JSON) object."
        )
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
    # row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/draft/teams"

    # Input validation
    ##########################################################################

    if api_key is not None:
        real_api_key = api_key
        del api_key
    else:
        real_api_key = get_cfbd_api_token(api_key_dir=api_key_dir)

    if real_api_key == "tigersAreAwesome":
        raise ValueError(
            "You actually need to change `cfbd_key` to your CFBD API key."
        )
    elif "Bearer " in real_api_key:
        pass
    elif "Bearer" in real_api_key:
        real_api_key = real_api_key.replace("Bearer", "Bearer ")
    else:
        real_api_key = "Bearer " + real_api_key

    headers = {
        "Authorization": f"{real_api_key}",
        "accept": "application/json"
    }

    response = requests.get(url, headers=headers)

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

    if return_as_dict is True:
        return json_data

    nfl_teams_df = pd.json_normalize(json_data)
    nfl_teams_df.rename(columns={"displayName": "display_name"}, inplace=True)
    return nfl_teams_df


def get_cfbd_nfl_positions(
    api_key: str = None, api_key_dir: str = None, return_as_dict: bool = False
):
    """
    Retrieves a list of player positions for the NFL Draft from the CFBD API.

    Parameters
    ----------
    `api_key` (str, optional):
        Semi-optional argument.
        If `api_key` is null, this function will attempt to load a CFBD API key
        from the python environment, or from a file on this computer.
        If `api_key` is not null,
        this function will automatically assume that the
        inputted `api_key` is a valid CFBD API key.

    `api_key_dir` (str, optional):
        Optional argument.
        If `api_key` is set to am empty string, this variable is ignored.
        If `api_key_dir` is null, and `api_key` is null,
        this function will try to find
        a CFBD API key file in this user's home directory.
        If `api_key_dir` is set to a string, and `api_key` is null,
        this function will assume that `api_key_dir` is a directory,
        and will try to find a CFBD API key file in that directory.

    `return_as_dict` (bool, semi-optional):
        Semi-optional argument.
        If you want this function to return
        the data as a dictionary (read: JSON object),
        instead of a pandas `DataFrame` object,
        set `return_as_dict` to `True`.

    Usage
    ----------
    ```
    import time

    from cfbd_json_py.draft import get_cfbd_nfl_positions

    cfbd_key = "tigersAreAwesome"  # placeholder for your CFBD API Key.

    if cfbd_key is not "tigersAreAwesome":
        print(
            "Using the user's API key declared in this script " +
            "for this example."
        )

        # Gets a list of player positions for the NFL Draft from the CFBD API.
        print(
            "Gets a list of player positions for the NFL Draft " +
            "from the CFBD API."
        )
        json_data = get_cfbd_nfl_positions(api_key=cfbd_key)
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call
        # as a Dictionary (read: JSON) object.
        print(
            "You can also tell this function to just return the API call " +
            "as a Dictionary (read: JSON) object."
        )
        json_data = get_cfbd_nfl_positions(
            api_key=cfbd_key,
            return_as_dict=True)
        print(json_data)

    else:
        # Alternatively, if the CFBD API key exists in this python environment,
        # or it's been set by cfbd_json_py.utls.set_cfbd_api_token(),
        # you could just call these functions directly,
        # without setting the API key in the script.
        print(
            "Using the user's API key supposedly loaded into " +
            "this python environment for this example."
        )

        # Gets a list of player positions for the NFL Draft from the CFBD API.
        print(
            "Gets a list of player positions for the NFL Draft " +
            "from the CFBD API."
        )
        json_data = get_cfbd_nfl_positions()
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call
        # as a Dictionary (read: JSON) object.
        print(
            "You can also tell this function to just return the API call " +
            "as a Dictionary (read: JSON) object."
        )
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
    # row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/draft/positions"

    # Input validation
    ##########################################################################

    if api_key is not None:
        real_api_key = api_key
        del api_key
    else:
        real_api_key = get_cfbd_api_token(api_key_dir=api_key_dir)

    if real_api_key == "tigersAreAwesome":
        raise ValueError(
            "You actually need to change `cfbd_key` to your CFBD API key."
        )
    elif "Bearer " in real_api_key:
        pass
    elif "Bearer" in real_api_key:
        real_api_key = real_api_key.replace("Bearer", "Bearer ")
    else:
        real_api_key = "Bearer " + real_api_key

    headers = {
        "Authorization": f"{real_api_key}",
        "accept": "application/json"
    }

    response = requests.get(url, headers=headers)

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

    if return_as_dict is True:
        return json_data

    # for p in json_data:
    #     position_name = p['name']
    #     position_abbreviation = p['abbreviation']

    #     row_df = pd.DataFrame(
    #         {
    #             "position_name": position_name,
    #             "position_abbreviation": position_abbreviation
    #         }, index=[0]
    #     )
    #     positions_df = pd.concat([positions_df, row_df], ignore_index=True)

    #     del position_name, position_abbreviation
    #     del row_df
    positions_df = pd.json_normalize(json_data)
    positions_df.rename(
        columns={
            "name": "position_name",
            "abbreviation": "position_abbreviation",
        },
        inplace=True,
    )

    return positions_df


def get_cfbd_nfl_draft_info(
    api_key: str = None,
    api_key_dir: str = None,
    season: int = None,
    nfl_team: str = None,
    college: str = None,
    conference: str = None,
    position: str = None,
    year: int = None,
    return_as_dict: bool = False,
):
    """
    Retrieves a list of actual NFL Draft selections from the CFBD API.

    Parameters
    ----------

    `api_key` (str, optional):
        Semi-optional argument.
        If `api_key` is null, this function will attempt to load a CFBD API key
        from the python environment, or from a file on this computer.
        If `api_key` is not null,
        this function will automatically assume that the
        inputted `api_key` is a valid CFBD API key.

    `api_key_dir` (str, optional):
        Optional argument.
        If `api_key` is set to am empty string, this variable is ignored.
        If `api_key_dir` is null, and `api_key` is null,
        this function will try to find
        a CFBD API key file in this user's home directory.
        If `api_key_dir` is set to a string, and `api_key` is null,
        this function will assume that `api_key_dir` is a directory,
        and will try to find a CFBD API key file in that directory.

    The following parameters are optional,
    but it is highly recommended to not call this function
    without declaring one of these five optional parameters
    as a non-null value.

    `season` (int, semi-optional):
        Semi-Optional argument.
        This is the season you want NFL Draft information for.
        For example, if you only want data for the 2020 NFL Draft,
        set `season` to `2020`.

    `nfl_team` (str, optional):
        Semi-Optional argument.
        If you only want NFL Draft selections from a specific NFL team,
        set `nfl_team` to the name of that team.
        For example, if you want to only get NFL Draft information for
        draft picks made by the Cincinnati Bengals,
        set `nfl_team` to `Cincinnati`.

    `college` (str, optional):
        Semi-Optional argument.
        If you only want NFL Draft selections from a specific CFB team,
        set `college` to the name of that team.
        For example, if you want to only get NFL Draft information for
        draft picks from the Clemson Tigers Football Program,
        set `college` to `Clemson`.

    `conference` (str, optional):
        Semi-Optional argument.
        If you only want NFL Draft selections from a specific CFB conference,
        set `conference` to the abbreviation of that conference.
        A list of CFBD API conference abbreviations can be found
        in the `conference_abbreviation` column from
        the pandas DataFrame that is returned by calling
        `cfbd_json_py.conferences.get_cfbd_conference_info()`.
        For example, if you want to only get NFL Draft information for
        draft picks that played in the Big 12, set `conference` to `B12`.

    `year` (int):
        Alternative keyword for `season`

    `position` (str, optional):
        Semi-Optional argument.
        If you only want NFL Draft selections who played a specific position,
        set `position` to that position's abbreviation.
        A list of CFBD API positions can be found in the
        `position_abbreviation` column from
        the pandas DataFrame that is returned by calling
        `cfbd_json_py.draft.get_cfbd_nfl_positions()`.

    `return_as_dict` (bool, semi-optional):
        Semi-optional argument.
        If you want this function to return the data
        as a dictionary (read: JSON object),
        instead of a pandas `DataFrame` object,
        set `return_as_dict` to `True`.
    Usage
    ----------

    ```
    import time

    from cfbd_json_py.draft import get_cfbd_nfl_draft_info

    cfbd_key = "tigersAreAwesome"  # placeholder for your CFBD API Key.

    if cfbd_key is not "tigersAreAwesome":
        print(
            "Using the user's API key declared in this script " +
            "for this example."
        )

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
        print(
            "Get NFL Draft selections from the 2020 NFL Draft made " +
            "by the 2020 Cincinnati Bengals."
        )
        json_data = get_cfbd_nfl_draft_info(
            api_key=cfbd_key,
            season=2020,
            nfl_team="Cincinnati"
        )
        print(json_data)
        time.sleep(5)

        # Get NFL Draft selections from the 2020 NFL Draft made involving
        # Clemson Tigers football players.
        print(
            "Get NFL Draft selections from the 2020 NFL Draft made " +
            "involving Clemson Tigers football players."
        )
        json_data = get_cfbd_nfl_draft_info(
            api_key=cfbd_key,
            season=2020,
            college="Clemson"
        )
        print(json_data)
        time.sleep(5)

        # Get NFL Draft selections from the 2020 NFL Draft made involving
        # players who played in the Southeastern conference (SEC).
        print(
            "Get NFL Draft selections from the 2020 NFL Draft made " +
            "involving players who played " +
            "in the Southeastern conference (SEC)."
        )
        json_data = get_cfbd_nfl_draft_info(
            api_key=cfbd_key,
            season=2020,
            conference="SEC"
        )
        print(json_data)
        time.sleep(5)

        # Get NFL Draft selections from the 2020 NFL Draft made
        # where the selected player was a QB in college.
        print(
            "Get NFL Draft selections from the 2020 NFL Draft made " +
            "where the selected player was a QB in college."
        )
        json_data = get_cfbd_nfl_draft_info(
            api_key=cfbd_key,
            season=2020,
            position="QB"
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call
        # as a Dictionary (read: JSON) object.
        print(
            "You can also tell this function to just return the API call " +
            "as a Dictionary (read: JSON) object."
        )
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
        # you could just call these functions directly,
        # without setting the API key in the script.
        print(
            "Using the user's API key supposedly loaded " +
            "into this python environment for this example."
        )

        # Get NFL Draft selections from the 2020 NFL Draft.
        print("Get NFL Draft selections from the 2020 NFL Draft.")
        json_data = get_cfbd_nfl_draft_info(season=2020)
        print(json_data)
        time.sleep(5)

        # Get NFL Draft selections from the 2020 NFL Draft made by the
        # 2020 Cincinnati Bengals.
        print(
            "Get NFL Draft selections from the 2020 NFL Draft " +
            "made by the 2020 Cincinnati Bengals."
        )
        json_data = get_cfbd_nfl_draft_info(
            season=2020,
            nfl_team="Cincinnati"
        )
        print(json_data)
        time.sleep(5)

        # Get NFL Draft selections from the 2020 NFL Draft made involving
        # Clemson Tigers football players.
        print(
            "Get NFL Draft selections from the 2020 NFL Draft made " +
            "involving Clemson Tigers football players."
        )
        json_data = get_cfbd_nfl_draft_info(
            season=2020,
            college="Clemson"
        )
        print(json_data)
        time.sleep(5)

        # Get NFL Draft selections from the 2020 NFL Draft made involving
        # players who played in the Southeastern conference (SEC).
        print(
            "Get NFL Draft selections from the 2020 NFL Draft made " +
            "involving players who played " +
            "in the Southeastern conference (SEC)."
        )
        json_data = get_cfbd_nfl_draft_info(
            season=2020,
            conference="SEC"
        )
        print(json_data)
        time.sleep(5)

        # Get NFL Draft selections from the 2020 NFL Draft made
        # where the selected player was a QB in college.
        print(
            "Get NFL Draft selections from the 2020 NFL Draft made " +
            "where the selected player was a QB in college."
        )
        json_data = get_cfbd_nfl_draft_info(
            season=2020,
            position="QB"
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call
        # as a Dictionary (read: JSON) object.
        print(
            "You can also tell this function to just return the API call " +
            "as a Dictionary (read: JSON) object."
        )
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
    # row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/draft/picks"

    # Input validation
    ##########################################################################

    # `year` to `season`
    if season is not None and year is not None and (year is not season):
        raise ValueError(
            "When using this function, "
            + "please specify a season in EITHER `year` or `season`."
        )
    if season is not None:
        pass
    elif year is not None:
        season = year
    else:
        raise ValueError("No year/season inputted for this function.")

    if api_key is not None:
        real_api_key = api_key
        del api_key
    else:
        real_api_key = get_cfbd_api_token(api_key_dir=api_key_dir)

    if real_api_key == "tigersAreAwesome":
        raise ValueError(
            "You actually need to change `cfbd_key` to your CFBD API key."
        )
    elif "Bearer " in real_api_key:
        pass
    elif "Bearer" in real_api_key:
        real_api_key = real_api_key.replace("Bearer", "Bearer ")
    else:
        real_api_key = "Bearer " + real_api_key

    if season is None \
            and nfl_team is None \
            and college is None \
            and conference is None:

        logging.warning(
            "Not specifying a `season`, `nfl_team`, `college`, "
            + "or `conference` will still result in "
            + "a successful get request (assuming the API key is valid)"
            + ", but this is not a recommended method "
            + "of calling this function."
        )

    if season < 1936 or season > now.year:
        raise ValueError(
            f"`season` must be an integer between 1936 and {now.year}.\n" +
            f"You entered:\n{season}"
        )

    # URL builder
    ##########################################################################

    url_elements = 0

    if season is not None and url_elements == 0:
        url += f"?year={season}"
        url_elements += 1
    elif season is not None:
        url += f"&year={season}"
        url_elements += 1

    if nfl_team is not None and url_elements == 0:
        url += f"?nflTeam={nfl_team}"  # nfl_team = "Cincinnati", not "CIN"
        url_elements += 1
    elif nfl_team is not None:
        url += f"&nflTeam={nfl_team}"
        url_elements += 1

    if college is not None and url_elements == 0:
        url += f"?college={college}"
        url_elements += 1
    elif college is not None:
        url += f"&college={college}"
        url_elements += 1

    if conference is not None and url_elements == 0:
        # conference = "SEC", not "Southeastern conference"
        url += f"?conference={conference}"
        url_elements += 1
    elif conference is not None:
        url += f"&conference={conference}"
        url_elements += 1

    if position is not None and url_elements == 0:
        url += f"?position={position}"
        url_elements += 1
    elif position is not None:
        url += f"&position={position}"
        url_elements += 1

    headers = {
        "Authorization": f"{real_api_key}",
        "accept": "application/json"
    }

    response = requests.get(url, headers=headers)

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

    if return_as_dict is True:
        return json_data

    nfl_draft_df = pd.json_normalize(json_data)
    # print(nfl_draft_df.columns)
    nfl_draft_df.rename(
        columns={
            "collegeAthleteId": "college_athlete_id",
            "nflAthleteId": "nfl_athlete_id",
            "collegeId": "college_id",
            "collegeTeam": "college_team_name",
            "collegeConference": "college_conference_name",
            "preDraftRanking": "pre_draft_ranking",
            "preDraftPositionRanking": "pre_draft_position_ranking",
            "preDraftGrade": "pre_draft_grade",
            "hometownInfo.city": "player_hometown_city",
            "hometownInfo.state": "player_hometown_state",
            "hometownInfo.country": "player_hometown_country",
            "hometownInfo.latitude": "player_hometown_latitude",
            "hometownInfo.longitude": "player_hometown_longitude",
            "hometownInfo.countyFips": "player_hometown_county_fips",
        },
        inplace=True,
    )
    if len(nfl_draft_df) == 0:
        logging.error(
            "The CFBD API accepted your inputs, "
            + "but found no data within your specified input parameters."
            + " Please double check your input parameters."
        )

    return nfl_draft_df
