# Creation Date: 08/30/2023 01:13 EDT
# Last Updated Date: 12/27/2023 11:09 PM EDT
# Author: Joseph Armstrong (armstrongjoseph08@gmail.com)
# File Name: players.py
# Purpose: Houses functions pertaining to CFB player data within the CFBD API.
####################################################################################################


from datetime import datetime
import logging

import pandas as pd
import requests
from tqdm import tqdm

# from cfbd_json_py.games import get_cfbd_player_game_stats
from cfbd_json_py.utls import get_cfbd_api_token


def cfbd_player_search(
    search_str: str,
    api_key: str = None,
    api_key_dir: str = None,
    position: str = None,
    team: str = None,
    season: int = None,
    return_as_dict: bool = False,
):
    """
    Given a string, search for players who's
    name matches that string in some capacity.

    Parameters
    ----------
    `search_str` (int, mandatory):
        Mandatory argument.
        This is the name of the player you are trying to find.

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

    `position` (bool, semi-optional):
        Semi-optional argument.
        If you only want players from a specific position,
        set `position` to the position you want to find players from.

    `team` (bool, semi-optional):
        Semi-optional argument.
        If you only want players from a specific team,
        set `team` to the name of the team you want to find players from.

    `season` (bool, semi-optional):
        Semi-optional argument.
        If you only want players from a specific CFB season,
        set `season` to the season you want to find players from.

    `return_as_dict` (bool, semi-optional):
        Semi-optional argument.
        If you want this function to return the data as a dictionary (read: JSON object),
        instead of a pandas `DataFrame` object,
        set `return_as_dict` to `True`.

    Usage
    ----------
    ```
    import time

    from cfbd_json_py.players import cfbd_player_search


    cfbd_key = "tigersAreAwsome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwsome":
        print("Using the user's API key declared in this script for this example.")

        # Get a list of every known "Joe" in the CFBD API.
        print("Get a list of every known \"Joe\" in the CFBD API.")
        json_data = cfbd_player_search(
            api_key=cfbd_key,
            search_str="Joe"
        )
        print(json_data)
        time.sleep(5)

        # Get a list of every known "Joe" in the CFBD API, who's last name starts with "B".
        print("Get a list of every known \"Joe\" in the CFBD API, who's last name starts with \"B\".")
        json_data = cfbd_player_search(
            api_key=cfbd_key,
            search_str="Joe B"
        )
        print(json_data)
        time.sleep(5)

        # Get a list of every known "Jim" in the CFBD API, who happened to play with the University of Cincinnati Football Team at some point in their career.
        print("Get a list of every known \"Jim\" in the CFBD API, who happened to play with the University of Cincinnati Football Team at some point in their career.")
        json_data = cfbd_player_search(
            api_key=cfbd_key,
            search_str="Jim",
            position="QB"
        )
        print(json_data)
        time.sleep(5)


        # Get a list of every known player of the University of Cincinnati Football Team, that had the letter "A" in their name.
        print("Get a list of every known player of the University of Cincinnati Football Team, that had the letter \"A\" in their name.")
        json_data = cfbd_player_search(
            api_key=cfbd_key,
            search_str="A",
            team="Cincinnati"
        )
        print(json_data)
        time.sleep(5)


        # Get a list of every known "Jim" in the CFBD API, who happened to play QB at some point in their career.
        print("Get a list of every known \"Jim\" in the CFBD API, who happened to play QB at some point in their career.")
        json_data = cfbd_player_search(
            api_key=cfbd_key,
            search_str="Jim",
            position="QB"
        )
        print(json_data)
        time.sleep(5)

        # Get a list of every known "Joe" in the CFBD API, who happened to play in the 2020 CFB sesason.
        print("Get a list of every known \"Joe\" in the CFBD API, who happened to play in the 2020 CFB sesason.")
        json_data = cfbd_player_search(
            api_key=cfbd_key,
            search_str="Joe",
            season=2020
        )
        print(json_data)
        time.sleep(5)


        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = cfbd_player_search(
            api_key=cfbd_key,
            search_str="Justin F",
            season=2020,
            return_as_dict=True
        )
        print(json_data)

    else:
        # Alternatively, if the CFBD API key exists in this python environment,
        # or it's been set by cfbd_json_py.utls.set_cfbd_api_token(),
        # you could just call these functions directly, without setting the API key
        # in the script.
        print("Using the user's API key suposedly loaded into this python environment for this example.")

        # Get a list of every known "Joe" in the CFBD API.
        print("Get a list of every known \"Joe\" in the CFBD API.")
        json_data = cfbd_player_search(
            search_str="Joe"
        )
        print(json_data)
        time.sleep(5)

        # Get a list of every known "Joe" in the CFBD API, who's last name starts with "B".
        print("Get a list of every known \"Joe\" in the CFBD API, who's last name starts with \"B\".")
        json_data = cfbd_player_search(
            search_str="Joe B"
        )
        print(json_data)
        time.sleep(5)

        # Get a list of every known "Jim" in the CFBD API, who happened to play with the University of Cincinnati Football Team at some point in their career.
        print("Get a list of every known \"Jim\" in the CFBD API, who happened to play with the University of Cincinnati Football Team at some point in their career.")
        json_data = cfbd_player_search(
            search_str="Jim",
            position="QB"
        )
        print(json_data)
        time.sleep(5)


        # Get a list of every known player of the University of Cincinnati Football Team, that had the letter "A" in their name.
        print("Get a list of every known player of the University of Cincinnati Football Team, that had the letter \"A\" in their name.")
        json_data = cfbd_player_search(
            search_str="A",
            team="Cincinnati"
        )
        print(json_data)
        time.sleep(5)


        # Get a list of every known "Jim" in the CFBD API, who happened to play QB at some point in their career.
        print("Get a list of every known \"Jim\" in the CFBD API, who happened to play QB at some point in their career.")
        json_data = cfbd_player_search(
            search_str="Jim",
            position="QB"
        )
        print(json_data)
        time.sleep(5)

        # Get a list of every known "Joe" in the CFBD API, who happened to play in the 2020 CFB sesason.
        print("Get a list of every known \"Joe\" in the CFBD API, who happened to play in the 2020 CFB sesason.")
        json_data = cfbd_player_search(
            search_str="Joe",
            season=2020
        )
        print(json_data)
        time.sleep(5)


        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = cfbd_player_search(
            search_str="Justin F",
            season=2020,
            return_as_dict=True
        )
        print(json_data)

    ```
    Returns
    ----------
    A pandas `DataFrame` object with a list of players who matched the search string,
    or (if `return_as_dict` is set to `True`)
    a dictionary object with a list of players who matched the search string.

    """
    now = datetime.now()
    players_df = pd.DataFrame()
    # row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/player/search"

    ########################################################################################################################################################################################################

    if api_key != None:
        real_api_key = api_key
        del api_key
    else:
        real_api_key = get_cfbd_api_token(api_key_dir=api_key_dir)

    if real_api_key == "tigersAreAwsome":
        raise ValueError("You actually need to change `cfbd_key` to your CFBD API key.")
    elif "Bearer " in real_api_key:
        pass
    elif "Bearer" in real_api_key:
        real_api_key = real_api_key.replace("Bearer", "Bearer ")
    else:
        real_api_key = "Bearer " + real_api_key

    if season == None:
        # Rare, but in this endpoint,
        # you don't need to input the season.
        pass
    elif season > (now.year + 1):
        raise ValueError(f"`season` cannot be greater than {season}.")
    elif season < 1869:
        raise ValueError(f"`season` cannot be less than 1869.")

    # URL builder
    ########################################################################################################################################################################################################

    # Required by API
    url += f"?searchTerm={search_str}"

    url = url.replace(" ", "%20")  # For sanity reasons with URLs.

    if position != None:
        url += f"&position={position}"

    if team != None:
        url += f"&team={team}"

    if season != None:
        url += f"&year={season}"

    headers = {"Authorization": f"{real_api_key}", "accept": "application/json"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        pass
    elif response.status_code == 401:
        raise ConnectionRefusedError(
            f"Could not connect. The connection was refused.\nHTTP Status Code 401."
        )
    else:
        raise ConnectionError(
            f"Could not connect.\nHTTP Status code {response.status_code}"
        )

    json_data = response.json()

    if return_as_dict == True:
        return json_data

    # for player in tqdm(json_data):
    #     p_id = player["id"]
    #     row_df = pd.DataFrame({"player_id": p_id}, index=[0])
    #     row_df["team"] = player["team"]
    #     row_df["player_full_name"] = player["name"]
    #     row_df["player_first_name"] = player["firstName"]
    #     row_df["player_last_name"] = player["lastName"]
    #     row_df["weight_lbs"] = player["weight"]
    #     row_df["height_in"] = player["height"]
    #     row_df["jersey"] = player["jersey"]
    #     row_df["position"] = player["position"]
    #     row_df["hometown"] = player["hometown"]
    #     row_df["team_color_primary"] = player["teamColor"]
    #     row_df["team_color_secondary"] = player["teamColorSecondary"]

    #     players_df = pd.concat([players_df, row_df], ignore_index=True)

    #     del row_df
    #     del p_id
    players_df = pd.json_normalize(json_data)
    players_df.rename(
        columns={
            "id": "player_id",
            "team": "team_name",
            "name": "player_name",
            "firstName": "first_name",
            "lastName": "last_name",
            "weight": "weight_lbs",
            "height": "height_in",
            "jersey": "jersey_num",
            "position": "position_abv",
            "teamColor": "team_color",
            "teamColorSecondary": "team_secondary_color",
        },
        inplace=True,
    )
    return players_df


def get_cfbd_player_usage(
    season: int,
    api_key: str = None,
    api_key_dir: str = None,
    team: str = None,
    conference: str = None,
    position: str = None,
    player_id: int = None,
    exclude_garbage_time: bool = False,
    return_as_dict: bool = False,
):
    """
    Get player usage data (A.K.A., the percentages for how often a player touched the ball),
    for a given season, at the season level, from the CFBD API.

    Parameters
    ----------
    `season` (int, optional):
        Mandatory argument.
        Specifies the season you want player usage data from.
        You MUST set `season` or `team` to a non-null value for
        this function to work. If you don't, a `ValueError()`
        will be raised.

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

    `team` (str, optional):
        Semi-ptional argument.
        If you only want player usage data for a specific team,
        set `team` to the name of the team you want player usage data from.
        You MUST set `season` or `team` to a non-null value for
        this function to work. If you don't, a `ValueError()`
        will be raised.

    `position` (str, optional):
        Semi-Optional argument.
        If you only want player usage data
        for players who played a specific position,
        set `position` to that position's abbreviation.
        A list of CFBD API positions can be found in the `position_abbreviation` column from
        the pandas DataFrame that is returned by calling `cfbd_json_py.draft.get_cfbd_nfl_positions()`.

    `conference` (str, optional):
        Optional argument.
        If you only want player usage data from games
        involving teams from a specific confrence,
        set `conference` to the abbreviation
        of the conference you want player usage data from.
        For a list of confrences,
        use the `cfbd_json_py.conferences.get_cfbd_conference_info()`
        function.

    `player_id` (int, optional):
        Optional argument.
        If you only want player usage data for a specific player ID,
        set this variable to the player ID of the player you want player usage data from.

    `exclude_garbage_time` (bool, optional):
        Optional argument.
        If you want to filter out plays where the result of the game is largely decided,
        set `exclude_garbage_time = True`.
        Default behavior is that this variable is set to
        `False` when this function is called.

    `return_as_dict` (bool, semi-optional):
        Semi-optional argument.
        If you want this function to return the data as a dictionary (read: JSON object),
        instead of a pandas `DataFrame` object,
        set `return_as_dict` to `True`.

    Usage
    ----------
    ```
    import time

    from cfbd_json_py.players import get_cfbd_player_usage


    cfbd_key = "tigersAreAwsome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwsome":
        print("Using the user's API key declared in this script for this example.")

        # Get player usage data from the 2020 CFB season.
        print("Get player usage data from the 2020 CFB season.")
        json_data = get_cfbd_player_usage(
            api_key=cfbd_key,
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get player usage data for the
        # University of Cincinnati Bearcats Football Team,
        # during the 2020 CFB season.
        print("Get player usage data for the University of Cincinnati Bearcats Football Team, during the 2020 CFB season.")
        json_data = get_cfbd_player_usage(
            api_key=cfbd_key,
            season=2020,
            team="Cincinnati"
        )
        print(json_data)
        time.sleep(5)

        # Get player usage data from players who
        # primarily played running back (RB) in the 2020 CFB season.
        print("Get player usage data from players who primarily played running back (RB) in the 2020 CFB season.")
        json_data = get_cfbd_player_usage(
            api_key=cfbd_key,
            season=2020,
            position="RB"
        )
        print(json_data)
        time.sleep(5)

        # Get player usage data from players who played on
        # Big 10 Confrence (B1G) teams during the 2020 CFB Season.
        print("Get player usage data from players who played on Big 10 Confrence (B1G) teams during the 2020 CFB Season.")
        json_data = get_cfbd_player_usage(
            api_key=cfbd_key,
            season=2020,
            conference="B1G"
        )
        print(json_data)
        time.sleep(5)

        # Get player usage data from
        # former LSU Tigers quarterback Joe Burrow (player ID #3915511),
        # during the 2019 CFB season.
        print("Get player usage data from former LSU Tigers quarterback Joe Burrow (player ID #3915511), during the 2019 CFB season.")
        json_data = get_cfbd_player_usage(
            api_key=cfbd_key,
            season=2019,
            player_id=3915511
        )
        print(json_data)
        time.sleep(5)

        # Get player usage data from
        # former LSU Tigers quarterback Joe Burrow (player ID #3915511),
        # during the 2019 CFB season,
        # but filter out plays that occured in garbage time.
        print("Get player usage data from former LSU Tigers quarterback Joe Burrow (player ID #3915511), during the 2019 CFB season.")
        json_data = get_cfbd_player_usage(
            api_key=cfbd_key,
            season=2019,
            player_id=3915511,
            exclude_garbage_time=True
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_player_usage(
            api_key=cfbd_key,
            season=2020,
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

        # Get player usage data from the 2020 CFB season.
        print("Get player usage data from the 2020 CFB season.")
        json_data = get_cfbd_player_usage(
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get player usage data for the
        # University of Cincinnati Bearcats Football Team,
        # during the 2020 CFB season.
        print("Get player usage data for the University of Cincinnati Bearcats Football Team, during the 2020 CFB season.")
        json_data = get_cfbd_player_usage(
            season=2020,
            team="Cincinnati"
        )
        print(json_data)
        time.sleep(5)

        # Get player usage data from players who
        # primarily played running back (RB) in the 2020 CFB season.
        print("Get player usage data from players who primarily played running back (RB) in the 2020 CFB season.")
        json_data = get_cfbd_player_usage(
            season=2020,
            position="RB"
        )
        print(json_data)
        time.sleep(5)

        # Get player usage data from players who played on
        # Big 10 Confrence (B1G) teams during the 2020 CFB Season.
        print("Get player usage data from players who played on Big 10 Confrence (B1G) teams during the 2020 CFB Season.")
        json_data = get_cfbd_player_usage(
            season=2020,
            conference="B1G"
        )
        print(json_data)
        time.sleep(5)

        # Get player usage data from
        # former LSU Tigers quarterback Joe Burrow (player ID #3915511),
        # during the 2019 CFB season.
        print("Get player usage data from former LSU Tigers quarterback Joe Burrow (player ID #3915511), during the 2019 CFB season.")
        json_data = get_cfbd_player_usage(
            season=2019,
            player_id=3915511
        )
        print(json_data)
        time.sleep(5)

        # Get player usage data from
        # former LSU Tigers quarterback Joe Burrow (player ID #3915511),
        # during the 2019 CFB season,
        # but filter out plays that occured in garbage time.
        print("Get player usage data from former LSU Tigers quarterback Joe Burrow (player ID #3915511), during the 2019 CFB season.")
        json_data = get_cfbd_player_usage(
            season=2019,
            player_id=3915511,
            exclude_garbage_time=True
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_player_usage(
            season=2020,
            team="LSU",
            return_as_dict=True
        )
        print(json_data)

    ```
    Returns
    ----------
    A pandas `DataFrame` object with player usage data,
    or (if `return_as_dict` is set to `True`)
    a dictionary object with player usage data.

    """

    now = datetime.now()
    players_df = pd.DataFrame()
    row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/player/usage"

    ########################################################################################################################################################################################################

    if api_key != None:
        real_api_key = api_key
        del api_key
    else:
        real_api_key = get_cfbd_api_token(api_key_dir=api_key_dir)

    if real_api_key == "tigersAreAwsome":
        raise ValueError("You actually need to change `cfbd_key` to your CFBD API key.")
    elif "Bearer " in real_api_key:
        pass
    elif "Bearer" in real_api_key:
        real_api_key = real_api_key.replace("Bearer", "Bearer ")
    else:
        real_api_key = "Bearer " + real_api_key

    if season == None:
        # This should never happen without user tampering, but if it does,
        # we need to raise an error, because the CFBD API will refuse this call without a valid season.
        raise SystemError(
            "I don't know how, I don't know why, but you managed to call this function while `season` was `None` (NULL),"
            + " and the function got to this point in the code."
            + "\nIf you have a GitHub account, please raise an issue on this python package's GitHub page:\n"
            + "https://github.com/armstjc/cfbd-json-py/issues"
        )
    elif season > (now.year + 1):
        raise ValueError(f"`season` cannot be greater than {season}.")
    elif season < 1869:
        raise ValueError(f"`season` cannot be less than 1869.")

    gt_str = ""
    if exclude_garbage_time == True:
        gt_str = "true"
    elif exclude_garbage_time == False:
        gt_str = "false"

    # URL builder
    ########################################################################################################################################################################################################

    url += f"?year={season}"

    if team != None:
        url += f"&team={team}"

    if conference != None:
        url += f"&conference={conference}"

    if position != None:
        url += f"&position={position}"

    if player_id != None:
        url += f"&playerId={player_id}"
        # print()
    if exclude_garbage_time != None:
        url += f"&excludeGarbageTime={gt_str}"

    headers = {"Authorization": f"{real_api_key}", "accept": "application/json"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        pass
    elif response.status_code == 401:
        raise ConnectionRefusedError(
            f"Could not connect. The connection was refused.\nHTTP Status Code 401."
        )
    else:
        raise ConnectionError(
            f"Could not connect.\nHTTP Status code {response.status_code}"
        )

    json_data = response.json()

    if return_as_dict == True:
        return json_data

    # for player in tqdm(json_data):
    #     row_df = pd.DataFrame({"season": season}, index=[0])
    #     row_df["player_id"] = player["id"]
    #     row_df["player_name"] = player["name"]
    #     row_df["player_position"] = player["position"]
    #     row_df["team"] = player["team"]
    #     row_df["conference"] = player["conference"]
    #     row_df["player_usage_overall"] = player["usage"]["overall"]
    #     row_df["player_usage_passing"] = player["usage"]["pass"]
    #     row_df["player_usage_rushing"] = player["usage"]["rush"]
    #     row_df["player_usage_1st_downs"] = player["usage"]["firstDown"]
    #     row_df["player_usage_2nd_downs"] = player["usage"]["secondDown"]
    #     row_df["player_usage_3rd_downs"] = player["usage"]["thirdDown"]
    #     row_df["player_usage_standard_downs"] = player["usage"]["standardDowns"]
    #     row_df["player_usage_pasing_downs"] = player["usage"]["passingDowns"]

    #     players_df = pd.concat([players_df, row_df], ignore_index=True)
    #     del row_df
    players_df = pd.json_normalize(json_data)
    players_df.rename(
        columns={
            "id": "player_id",
            "name": "player_name",
            "position": "position_abv",
            "team": "team_name",
            "conference": "conference_name",
            "usage.overall": "usage_overall",
            "usage.pass": "usage_pass",
            "usage.rush": "usage_rush",
            "usage.firstDown": "usage_first_down",
            "usage.secondDown": "usage_second_down",
            "usage.thirdDown": "usage_third_down",
            "usage.standardDowns": "usage_standard_downs",
            "usage.passingDowns": "usage_passing_downs",
        },
        inplace=True,
    )
    return players_df


def get_cfbd_returning_production(
    api_key: str = None,
    api_key_dir: str = None,
    season: int = None,
    team: str = None,
    # `season` or `team` must be specified.
    conference: str = None,
    return_as_dict: bool = False,
):
    """
    Get data from the CFBD API
    on how much returning production a team has going into a CFB season.

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
        Semi-optional argument.
        Specifies the season you want team PPA data from.
        You MUST set `season` or `team` to a non-null value for
        this function to work. If you don't, a `ValueError()`
        will be raised.

    `team` (str, optional):
        Semi-ptional argument.
        If you only want team PPA data for a specific team,
        set `team` to the name of the team you want team PPA data from.
        You MUST set `season` or `team` to a non-null value for
        this function to work. If you don't, a `ValueError()`
        will be raised.

    `conference` (str, optional):
        Optional argument.
        If you only want team PPA data from games
        involving teams from a specific confrence,
        set `conference` to the abbreviation
        of the conference you want team PPA data from.
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

    from cfbd_json_py.players import get_cfbd_returning_production


    cfbd_key = "tigersAreAwsome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwsome":
        print("Using the user's API key declared in this script for this example.")

        # Get returning production for teams who competed in the 2020 CFB season.
        print("Get returning production for teams who competed in the 2020 CFB season.")
        json_data = get_cfbd_returning_production(
            api_key=cfbd_key,
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get historical returning production for the Ohio Bobcats Football Team.
        print("Get historical returning production for the Ohio Bobcats Football Team.")
        json_data = get_cfbd_returning_production(
            api_key=cfbd_key,
            team="Ohio"
        )
        print(json_data)
        time.sleep(5)

        # Get returning production for the 2019 LSU Tigers.
        print("Get returning production for the 2019 LSU Tigers.")
        json_data = get_cfbd_returning_production(
            api_key=cfbd_key,
            season=2019,
            team="LSU"
        )
        print(json_data)
        time.sleep(5)

        # Get returning production for Maryland, for seasons where Maryland is a member of the Big 10 (B1G) Conference.
        print("Get returning production for Maryland, for seasons where Maryland is a member of the Big 10 (B1G) Conference.")
        json_data = get_cfbd_returning_production(
            api_key=cfbd_key,
            team="Maryland",
            conference="B1G"
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_returning_production(
            api_key=cfbd_key,
            season=2020,
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

        # Get returning production for teams who competed in the 2020 CFB season.
        print("Get returning production for teams who competed in the 2020 CFB season.")
        json_data = get_cfbd_returning_production(
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get historical returning production for the Ohio Bobcats Football Team.
        print("Get historical returning production for the Ohio Bobcats Football Team.")
        json_data = get_cfbd_returning_production(
            team="Ohio"
        )
        print(json_data)
        time.sleep(5)

        # Get returning production for the 2019 LSU Tigers.
        print("Get returning production for the 2019 LSU Tigers.")
        json_data = get_cfbd_returning_production(
            season=2019,
            team="LSU"
        )
        print(json_data)
        time.sleep(5)

        # Get returning production for Maryland, for seasons where Maryland is a member of the Big 10 (B1G) Conference.
        print("Get returning production for Maryland, for seasons where Maryland is a member of the Big 10 (B1G) Conference.")
        json_data = get_cfbd_returning_production(
            team="Maryland",
            conference="B1G"
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_returning_production(
            season=2020,
            team="LSU",
            return_as_dict=True
        )
        print(json_data)


    ```
    Returns
    ----------
    A pandas `DataFrame` object with returning production data,
    or (if `return_as_dict` is set to `True`)
    a dictionary object with returning production data.

    """
    now = datetime.now()
    team_df = pd.DataFrame()
    row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/player/returning"

    ########################################################################################################################################################################################################

    if api_key != None:
        real_api_key = api_key
        del api_key
    else:
        real_api_key = get_cfbd_api_token(api_key_dir=api_key_dir)

    if real_api_key == "tigersAreAwsome":
        raise ValueError("You actually need to change `cfbd_key` to your CFBD API key.")
    elif "Bearer " in real_api_key:
        pass
    elif "Bearer" in real_api_key:
        real_api_key = real_api_key.replace("Bearer", "Bearer ")
    else:
        real_api_key = "Bearer " + real_api_key

    if season == None and team == None:
        raise ValueError(
            "To use this function, `season` and/or `team` must be set to a "
            + "non-null variable."
        )

    if season == None:
        # Rare, but in this endpoint,
        # you don't need to input the season.
        pass
    elif season > (now.year + 1):
        raise ValueError(f"`season` cannot be greater than {season}.")
    elif season < 1869:
        raise ValueError(f"`season` cannot be less than 1869.")

    # URL Builder
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

    if conference != None and url_elements == 0:
        url += f"?conference={conference}"
        url_elements += 1
    elif conference != None:
        url += f"&conference={conference}"
        url_elements += 1

    headers = {"Authorization": f"{real_api_key}", "accept": "application/json"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        pass
    elif response.status_code == 401:
        raise ConnectionRefusedError(
            f"Could not connect. The connection was refused.\nHTTP Status Code 401."
        )
    else:
        raise ConnectionError(
            f"Could not connect.\nHTTP Status code {response.status_code}"
        )

    json_data = response.json()

    if return_as_dict == True:
        return json_data

    # for team in tqdm(json_data):
    #     t_season = team["season"]
    #     t_conference = team["conference"]
    #     t_name = team["team"]

    #     row_df = pd.DataFrame(
    #         {"season": t_season, "team_name": t_name, "team_conference": t_conference},
    #         index=[0],
    #     )
    #     row_df["total_ppa"] = team["totalPPA"]
    #     row_df["total_ppa_passing"] = team["totalPassingPPA"]
    #     row_df["total_ppa_rushing"] = team["totalRushingPPA"]
    #     row_df["total_ppa_receiving"] = team["totalReceivingPPA"]
    #     row_df["percent_ppa"] = team["percentPPA"]
    #     row_df["percent_ppa_passing"] = team["percentPassingPPA"]
    #     row_df["percent_ppa_rushing"] = team["percentRushingPPA"]
    #     row_df["percent_ppa_receiving"] = team["percentReceivingPPA"]
    #     row_df["usage"] = team["usage"]
    #     row_df["passing_usage"] = team["passingUsage"]
    #     row_df["rushing_usage"] = team["rushingUsage"]
    #     row_df["receiving_usage"] = team["receivingUsage"]

    #     team_df = pd.concat([team_df, row_df], ignore_index=True)

    #     del row_df
    #     del t_season, t_conference, t_name
    team_df = pd.json_normalize(json_data)
    team_df.rename(
        columns={
            "team": "team_name",
            "conference": "conference_name",
            "totalPPA": "returning_total_ppa",
            "totalPassingPPA": "returning_total_passing_ppa",
            "totalReceivingPPA": "returning_total_receiving_ppa",
            "totalRushingPPA": "returning_total_rush_ppa",
            "percentPPA": "returning_ppa_percent",
            "percentPassingPPA": "returning_percent_passing_ppa",
            "percentReceivingPPA": "returning_percent_receiving_ppa",
            "percentRushingPPA": "returning_percent_rushing_ppa",
            "usage": "returning_usage",
            "passingUsage": "returning_passing_usage",
            "receivingUsage": "returning_receiving_usage",
            "rushingUsage": "returning_rushing_usage",
        },
        inplace=True,
    )
    return team_df


def get_cfbd_player_season_stats(
    season: int,
    api_key: str = None,
    api_key_dir: str = None,
    team: str = None,
    conference: str = None,
    start_week: int = None,
    end_week: int = None,
    season_type: str = "both",  # "regular", "postseason", or "both"
    stat_category: str = None,
    return_as_dict: bool = False,
):
    """
    Get player season stats, or the stats of players in a specific timeframe, from the CFBD API.

    Parameters
    ----------
    `season` (int, mandatory):
        Required argument.
        Specifies the season you want CFB player season stats from.
        This must be specified, otherwise this package, and by extension
        the CFBD API, will not accept the request to get CFB player season stats.

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

    `team` (str, optional):
        Optional argument.
        If you only want CFB player season stats for a team,
        regardless if they are the home/away team,
        set `team` to the name of the team you want CFB player season stats from.

    `conference` (str, optional):
        Optional argument.
        If you only want player season stats from games
        involving teams a specific confrence,
        set `conference` to the abbreviation
        of the conference you want stats from.

    `start_week` (int, semi-optional):
        Optional argument.
        If you only want player stats for a range of weeks,
        set `start_week` and `end_week` to
        the range of weeks you want season-level data for.

    `end_week` (int, semi-optional):
        Optional argument.
        If you only want player stats for a range of weeks,
        set `start_week` and `end_week` to
        the range of weeks you want season-level data for.

    **NOTE**: If the following conditions are `True`, a `ValueError()`
    will be raised when calling this function:
    - `start_week < 0`
    - `end_week < 0`
    - `start_week != None and end_week == None` (will be changed in a future version)
    - `start_week == None and end_week != None` (will be changed in a future version)
    - `end_week < start_week`
    - `end_week = start_week`

    `season_type` (str, semi-optional):
        Semi-optional argument.
        By defualt, this will be set to "regular", for the CFB regular season.
        If you want CFB media information for non-regular season games,
        set `season_type` to "postseason".
        If you want ***both*** regular and postseason stats, set `season_type = "both"`.
        If `season_type` is set to anything but "regular", "postseason",  or "both",
        a `ValueError()` will be raised.

    `stat_category` (str, optional):
        Optional argument.
        If only want stats for a specific stat category,
        set this variable to that category.

        Valid inputs are:
        - `passing`
        - `rushing`
        - `receiving`
        - `fumbles`
        - `defensive`
        - `interceptions`
        - `punting`
        - `kicking`
        - `kickReturns`
        - `puntReturns`

    `return_as_dict` (bool, semi-optional):
        Semi-optional argument.
        If you want this function to return the data as a dictionary (read: JSON object),
        instead of a pandas `DataFrame` object,
        set `return_as_dict` to `True`.

    Usage
    ----------
    ```
    import time

    from cfbd_json_py.players import get_cfbd_player_season_stats


    cfbd_key = "tigersAreAwsome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwsome":
        print("Using the user's API key declared in this script for this example.")

        # Get player season stats for the Ohio Bobcats Football team in the 2020 CFB season.
        print("Get player season stats for the Ohio Bobcats Football team in the 2020 CFB season.")
        json_data = get_cfbd_player_season_stats(
            api_key=cfbd_key,
            season=2020,
            team="Ohio"
        )
        print(json_data)
        time.sleep(5)

        # Get player season stats for teams who competed in
        # the Southeastern Confrence (SEC) in the 2023 CFB season.
        print("Get player season stats for teams who competed in the Southeastern Confrence (SEC) in the 2023 CFB season.")
        json_data = get_cfbd_player_season_stats(
            api_key=cfbd_key,
            season=2020,
            conference="SEC"
        )
        print(json_data)
        time.sleep(5)

        # Get player season stats for teams who competed in
        # the Southeastern Confrence (SEC) in the 2023 CFB season,
        # but only between weeks 1 and 5.
        print("Get player season stats for teams who competed in the Southeastern Confrence (SEC) in the 2023 CFB season.")
        json_data = get_cfbd_player_season_stats(
            api_key=cfbd_key,
            season=2020,
            conference="SEC",
            start_week=1,
            end_week=5
        )
        print(json_data)
        time.sleep(5)

        # Get player season stats for the 2020 CFB season.
        print("Get player season stats for the 2020 CFB season.")
        json_data = get_cfbd_player_season_stats(
            api_key=cfbd_key,
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get player season stats for
        # the Ohio Bobcats Football team in the 2022 CFB season,
        # but only use regular season games when calculating season stats.
        print("Get player season stats for the Ohio Bobcats Football team in the 2020 CFB season, but only use regular season games when calculating season stats.")
        json_data = get_cfbd_player_season_stats(
            api_key=cfbd_key,
            season=2022,
            team="Ohio",
            season_type="regular"
        )
        print(json_data)
        time.sleep(5)

        # Get passing stats for teams who competed in
        # the Southeastern Confrence (SEC) in the 2023 CFB season.
        print("Get passing stats for teams who competed in the Southeastern Confrence (SEC) in the 2023 CFB season.")
        json_data = get_cfbd_player_season_stats(
            api_key=cfbd_key,
            season=2020,
            conference="SEC",
            stat_category="passing"
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_player_season_stats(
            api_key=cfbd_key,
            season=2020,
            team="LSU",
            stat_category="kicking",
            return_as_dict=True
        )
        print(json_data)

    else:
        # Alternatively, if the CFBD API key exists in this python environment,
        # or it's been set by cfbd_json_py.utls.set_cfbd_api_token(),
        # you could just call these functions directly, without setting the API key
        # in the script.
        print("Using the user's API key suposedly loaded into this python environment for this example.")

        # Get player season stats for the Ohio Bobcats Football team in the 2020 CFB season.
        print("Get player season stats for the Ohio Bobcats Football team in the 2020 CFB season.")
        json_data = get_cfbd_player_season_stats(
            season=2020,
            team="Ohio"
        )
        print(json_data)
        time.sleep(5)

        # Get player season stats for teams who competed in
        # the Southeastern Confrence (SEC) in the 2023 CFB season.
        print("Get player season stats for teams who competed in the Southeastern Confrence (SEC) in the 2023 CFB season.")
        json_data = get_cfbd_player_season_stats(
            season=2020,
            conference="SEC"
        )
        print(json_data)
        time.sleep(5)

        # Get player season stats for teams who competed in
        # the Southeastern Confrence (SEC) in the 2023 CFB season,
        # but only between weeks 1 and 5.
        print("Get player season stats for teams who competed in the Southeastern Confrence (SEC) in the 2023 CFB season.")
        json_data = get_cfbd_player_season_stats(
            season=2020,
            conference="SEC",
            start_week=1,
            end_week=5
        )
        print(json_data)
        time.sleep(5)

        # Get player season stats for the 2020 CFB season.
        print("Get player season stats for the 2020 CFB season.")
        json_data = get_cfbd_player_season_stats(
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get player season stats for
        # the Ohio Bobcats Football team in the 2022 CFB season,
        # but only use regular season games when calculating season stats.
        print("Get player season stats for the Ohio Bobcats Football team in the 2020 CFB season, but only use regular season games when calculating season stats.")
        json_data = get_cfbd_player_season_stats(
            season=2022,
            team="Ohio",
            season_type="regular"
        )
        print(json_data)
        time.sleep(5)

        # Get passing stats for teams who competed in
        # the Southeastern Confrence (SEC) in the 2023 CFB season.
        print("Get passing stats for teams who competed in the Southeastern Confrence (SEC) in the 2023 CFB season.")
        json_data = get_cfbd_player_season_stats(
            season=2020,
            conference="SEC",
            stat_category="passing"
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_player_season_stats(
            season=2020,
            team="LSU",
            stat_category="kicking",
            return_as_dict=True
        )
        print(json_data)

    ```
    Returns
    ----------
    A pandas `DataFrame` object with a list of players who matched the search string,
    or (if `return_as_dict` is set to `True`)
    a dictionary object with a list of players who matched the search string.

    """

    rebuilt_json = {}
    stat_columns = [
        "season",
        "team_name",
        "team_confrence",
        "player_id",
        "player_name",
        # PASS
        "passing_COMP",
        "passing_ATT",
        "passing_COMP%",
        "passing_YDS",
        "passing_AVG",
        "passing_TD",
        "passing_INT",
        # RUSH
        "rushing_CAR",
        "rushing_YDS",
        "rushing_AVG",
        "rushing_TD",
        "rushing_LONG",
        # REC
        "receiving_REC",
        "receiving_YDS",
        "receiving_AVG",
        "receiving_TD",
        "receiving_LONG",
        # FUM
        "fumbles_FUM",
        "fumbles_LOST",
        "fumbles_REC",
        # DEFENSE
        "defensive_TOT",
        "defensive_SOLO",
        "defensive_TFL",
        "defensive_QB HUR",
        "defensive_SACKS",
        "defensive_PD",
        "defensive_TD",
        # INT
        "interceptions_INT",
        "interceptions_YDS",
        "interceptions_TD",
        # PUNT
        "punting_NO",
        "punting_YDS",
        "punting_AVG",
        "punting_TB",
        "punting_In 20",
        "punting_LONG",
        # KICK
        "kicking_FGM",
        "kicking_FGA",
        "kicking_FG%",
        "kicking_LONG",
        "kicking_XPM",
        "kicking_XPA",
        "kicking_XP%",
        # KR
        "kickReturns_NO",
        "kickReturns_YDS",
        "kickReturns_AVG",
        "kickReturns_TD",
        "kickReturns_LONG",
        # PR
        "puntReturns_NO",
        "puntReturns_YDS",
        "puntReturns_AVG",
        "puntReturns_TD",
        "puntReturns_LONG",
    ]

    now = datetime.now()
    url = "https://api.collegefootballdata.com/stats/player/season"

    final_df = pd.DataFrame()

    if api_key != None:
        real_api_key = api_key
        del api_key
    else:
        real_api_key = get_cfbd_api_token(api_key_dir=api_key_dir)

    if real_api_key == "tigersAreAwsome":
        raise ValueError("You actually need to change `cfbd_key` to your CFBD API key.")
    elif "Bearer " in real_api_key:
        pass
    elif "Bearer" in real_api_key:
        real_api_key = real_api_key.replace("Bearer", "Bearer ")
    else:
        real_api_key = "Bearer " + real_api_key

    if season == None:
        # This should never happen without user tampering, but if it does,
        # we need to raise an error, because the CFBD API will refuse this call without a valid season.
        raise SystemError(
            "I don't know how, I don't know why, "
            + "but you managed to call this function while `season` was `None` (NULL),"
            + " and the function got to this point in the code."
            + "\nIf you have a GitHub account, "
            + "please raise an issue on this python package's GitHub page:\n"
            + "https://github.com/armstjc/cfbd-json-py/issues"
        )
    elif season > (now.year + 1):
        raise ValueError(f"`season` cannot be greater than {season}.")
    elif season < 1869:
        raise ValueError(f"`season` cannot be less than 1869.")

    if (
        season_type != "regular"
        and season_type != "postseason"
        and season_type != "both"
    ):
        raise ValueError(
            '`season_type` must be set to either "regular" or '
            + '"postseason" for this function to work.'
        )

    filter_by_stat_category = False

    if stat_category == None:
        pass
    elif stat_category == "passing":
        filter_by_stat_category = True
    elif stat_category == "rushing":
        filter_by_stat_category = True
    elif stat_category == "receiving":
        filter_by_stat_category = True
    elif stat_category == "fumbles":
        filter_by_stat_category = True
    elif stat_category == "passing":
        filter_by_stat_category = True
    elif stat_category == "defensive":
        filter_by_stat_category = True
    elif stat_category == "interceptions":
        filter_by_stat_category = True
    elif stat_category == "punting":
        filter_by_stat_category = True
    elif stat_category == "kicking":
        filter_by_stat_category = True
    elif stat_category == "kickReturns":
        filter_by_stat_category = True
    elif stat_category == "puntReturns":
        filter_by_stat_category = True
    else:
        raise ValueError(
            "Invalid input for `stat_category`."
            + "\nValid inputs are:"
            + """
            - `passing`
            - `rushing`
            - `receiving`
            - `fumbles`
            - `defensive`
            - `interceptions`
            - `punting`
            - `kicking`
            - `kickReturns`
            - `puntReturns`
            """
        )

    if start_week != None and end_week != None:
        if start_week > end_week:
            raise ValueError("`start_week` cannot be greater than `end_week`.")
        elif start_week == end_week:
            raise ValueError(
                "`start_week` cannot be equal to `end_week`."
                + "\n Use `cfbd_json_py.games.get_cfbd_player_game_stats()` instead "
                + "if you want player stats for a specific week in ."
            )
        elif start_week < 0:
            raise ValueError("`start_week` cannot be less than 0.")
        elif end_week < 0:
            raise ValueError("`end_week` cannot be less than 0.")
    #
    # elif start_week != None and end_week == None:
    #     raise ValueError(
    #         "At this time, if you want to get season stats for a range of weeks " +
    #         "`start_week` and `end_week` must be set to valid integers," +
    #         " and not just `start_week`."
    #     )
    # elif start_week == None and end_week != None:
    #     raise ValueError(
    #         "At this time, if you want to get season stats for a range of weeks " +
    #         "`start_week` and `end_week` must be set to valid integers," +
    #         " and not just `end_week`."
    #     )

    if filter_by_stat_category == True:
        pass

    # URL builder
    ########################################################################################################################################################################################################

    # Required by the API
    url += f"?year={season}"

    if team != None:
        url += f"&team={team}"

    if conference != None:
        url += f"&conference={conference}"

    if season_type != None:
        url += f"&seasonType={season_type}"

    if stat_category != None:
        url += f"&category={stat_category}"

    if start_week != None:
        url += f"&startWeek={start_week}"

    if end_week != None:
        url += f"&endWeek={end_week}"

    headers = {"Authorization": f"{real_api_key}", "accept": "application/json"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        pass
    elif response.status_code == 401:
        raise ConnectionRefusedError(
            f"Could not connect. The connection was refused.\nHTTP Status Code 401."
        )
    else:
        raise ConnectionError(
            f"Could not connect.\nHTTP Status code {response.status_code}"
        )

    json_data = response.json()

    if return_as_dict == True:
        return json_data

    for player in tqdm(json_data):
        player_id = int(player["playerId"])
        player_name = player["player"]
        team_name = player["team"]
        team_confrence = player["conference"]
        s_category = player["category"]
        s_type = player["statType"]
        s_num = player["stat"]

        if rebuilt_json.get(player_id) == None:
            rebuilt_json[player_id] = {}

        if s_category == "passing":
            if s_type == "COMPLETIONS":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["passing_COMP"] = s_num

            elif s_type == "ATT":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["passing_ATT"] = s_num

            elif s_type == "YDS":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["passing_YDS"] = s_num

            elif s_type == "TD":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["passing_TD"] = s_num

            elif s_type == "INT":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["passing_INT"] = s_num
            # we can calculate these two later
            elif s_type == "PCT":
                pass

            elif s_type == "YPA":
                pass

            else:
                raise ValueError(f"Unhandled stat type: {s_type}")

        elif s_category == "rushing":
            if s_type == "CAR":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["rushing_CAR"] = s_num

            elif s_type == "YDS":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["rushing_YDS"] = s_num

            elif s_type == "TD":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["rushing_TD"] = s_num

            elif s_type == "LONG":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["rushing_LONG"] = s_num
            # we can calculate this later
            elif s_type == "YPC":
                pass

            else:
                raise ValueError(f"Unhandled stat type: {s_type}")

        elif s_category == "receiving":
            if s_type == "REC":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["receiving_REC"] = s_num

            elif s_type == "YDS":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["receiving_YDS"] = s_num

            elif s_type == "TD":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["receiving_TD"] = s_num

            elif s_type == "LONG":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["receiving_LONG"] = s_num
            # we can calculate this later
            elif s_type == "YPR":
                pass

            else:
                raise ValueError(f"Unhandled stat type: {s_type}")

        elif s_category == "fumbles":
            if s_type == "FUM":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["fumbles_FUM"] = s_num

            elif s_type == "LOST":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["fumbles_LOST"] = s_num

            elif s_type == "REC":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["fumbles_LOST"] = s_num

            else:
                raise ValueError(f"Unhandled stat type: {s_type}")

        elif s_category == "defensive":
            if s_type == "TOT":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["defensive_TOT"] = s_num

            elif s_type == "SOLO":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["defensive_SOLO"] = s_num

            elif s_type == "TFL":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["defensive_TFL"] = s_num

            elif s_type == "QB HUR":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["defensive_QB HUR"] = s_num

            elif s_type == "SACKS":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["defensive_SACKS"] = s_num

            elif s_type == "PD":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["defensive_PD"] = s_num

            elif s_type == "TD":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["defensive_TD"] = s_num

            else:
                raise ValueError(f"Unhandled stat type: {s_type}")

        elif s_category == "interceptions":
            if s_type == "INT":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["interceptions_INT"] = s_num

            elif s_type == "YDS":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["interceptions_YDS"] = s_num

            elif s_type == "TD":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["interceptions_TD"] = s_num

            elif s_type == "AVG":
                pass

            else:
                raise ValueError(f"Unhandled stat type: {s_type}")

        elif s_category == "punting":
            if s_type == "NO":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["punting_NO"] = s_num

            elif s_type == "YDS":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["punting_YDS"] = s_num

            elif s_type == "TB":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["punting_TB"] = s_num

            elif s_type == "In 20":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["punting_In 20"] = s_num

            elif s_type == "LONG":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["punting_LONG"] = s_num

            elif s_type == "YPP":
                pass

            else:
                raise ValueError(f"Unhandled stat type: {s_type}")

        elif s_category == "kicking":
            if s_type == "FGM":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["kicking_FGM"] = s_num

            elif s_type == "FGA":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["kicking_FGA"] = s_num

            elif s_type == "LONG":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["kicking_LONG"] = s_num

            elif s_type == "XPM":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["kicking_XPM"] = s_num

            elif s_type == "XPA":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["kicking_XPA"] = s_num

            elif s_type == "PTS":
                pass

            elif s_type == "PCT":
                pass

            else:
                raise ValueError(f"Unhandled stat type: {s_type}")

        elif s_category == "kickReturns":
            if s_type == "NO":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["kickReturns_NO"] = s_num

            elif s_type == "YDS":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["kickReturns_YDS"] = s_num

            elif s_type == "TD":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["kickReturns_TD"] = s_num

            elif s_type == "LONG":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["kickReturns_LONG"] = s_num
            # we can calculate this later
            elif s_type == "AVG":
                pass

            else:
                raise ValueError(f"Unhandled stat type: {s_type}")

        elif s_category == "puntReturns":
            if s_type == "NO":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["puntReturns_NO"] = s_num

            elif s_type == "YDS":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["puntReturns_YDS"] = s_num

            elif s_type == "TD":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["puntReturns_TD"] = s_num

            elif s_type == "LONG":
                rebuilt_json[player_id]["player_name"] = player_name
                rebuilt_json[player_id]["team_name"] = team_name
                rebuilt_json[player_id]["team_confrence"] = team_confrence
                rebuilt_json[player_id]["puntReturns_LONG"] = s_num
            # we can calculate this later
            elif s_type == "AVG":
                pass

            else:
                raise ValueError(f"Unhandled stat type: {s_type}")

        else:
            raise ValueError(f"Unhandled stat category: {s_category}")

        del player_id, player_name, team_name, team_confrence, s_category, s_type, s_num

    for key, value in tqdm(rebuilt_json.items()):
        row_df = pd.json_normalize(value)
        final_df = pd.concat([final_df, row_df], ignore_index=True)
        del row_df

    # final_df=final_df.astype({
    #     "passing_COMP": "int32",
    #     "passing_ATT": "int32",
    # })
    final_df = final_df.fillna(0)

    final_df["season"] = season

    if filter_by_stat_category == False:
        final_df = final_df.reindex(columns=stat_columns)
        final_df = final_df.astype(
            {
                "passing_COMP": "int",
                "passing_ATT": "int",
                "rushing_CAR": "int",
                "rushing_YDS": "int",
                "receiving_REC": "int",
                "receiving_YDS": "int",
                "punting_NO": "int",
                "punting_YDS": "int",
                "kicking_FGM": "int",
                "kicking_FGA": "int",
                "kicking_XPM": "int",
                "kicking_XPA": "int",
                "kickReturns_NO": "int",
                "kickReturns_YDS": "int",
                "puntReturns_NO": "int",
                "puntReturns_YDS": "int",
            }
        )

        final_df.loc[final_df["passing_ATT"] > 0, "passing_COMP%"] = (
            final_df["passing_COMP"] / final_df["passing_ATT"]
        )

        final_df.loc[final_df["rushing_CAR"] > 0, "rushing_AVG"] = (
            final_df["rushing_YDS"] / final_df["rushing_CAR"]
        )

        final_df.loc[final_df["receiving_REC"] > 0, "receiving_AVG"] = (
            final_df["receiving_YDS"] / final_df["receiving_REC"]
        )

        final_df.loc[final_df["punting_NO"] > 0, "punting_AVG"] = (
            final_df["punting_YDS"] / final_df["punting_NO"]
        )

        final_df.loc[final_df["kicking_FGA"] > 0, "kicking_FG%"] = (
            final_df["kicking_FGM"] / final_df["kicking_FGA"]
        )

        final_df.loc[final_df["kicking_XPA"] > 0, "kicking_XP%"] = (
            final_df["kicking_XPM"] / final_df["kicking_XPA"]
        )

        final_df.loc[final_df["kickReturns_NO"] > 0, "kickReturns_AVG"] = (
            final_df["kickReturns_YDS"] / final_df["kickReturns_NO"]
        )

        final_df.loc[final_df["puntReturns_NO"] > 0, "puntReturns_AVG"] = (
            final_df["puntReturns_YDS"] / final_df["puntReturns_NO"]
        )

    elif filter_by_stat_category == True and stat_category == "passing":
        try:
            final_df = final_df.astype(
                {
                    "passing_COMP": "int",
                    "passing_ATT": "int",
                }
            )
        except:
            logging.warning(
                "Could not reformat [passing_COMP] and [passing_ATT] into integers."
            )

        final_df.loc[final_df["passing_ATT"] >= 1, "passing_COMP%"] = (
            final_df["passing_COMP"] / final_df["passing_ATT"]
        )

        final_df = final_df[
            [
                "season",
                "team_name",
                "team_confrence",
                # "player_id",
                "player_name",
                # PASS
                "passing_COMP",
                "passing_ATT",
                "passing_YDS",
                "passing_TD",
                "passing_INT",
            ]
        ]

    elif filter_by_stat_category == True and stat_category == "rushing":
        try:
            final_df = final_df.astype(
                {
                    "rushing_CAR": "int",
                    "rushing_YDS": "int",
                }
            )
        except:
            logging.warning(
                "Could not reformat [rushing_CAR] and [rushing_YDS] into integers."
            )

        final_df.loc[final_df["rushing_CAR"] >= 1, "rushing_AVG"] = (
            final_df["rushing_YDS"] / final_df["rushing_CAR"]
        )

        final_df = final_df[
            [
                "season",
                "team_name",
                "team_confrence",
                "player_id",
                "player_name",
                # RUSH
                "rushing_CAR",
                "rushing_YDS",
                "rushing_AVG",
                "rushing_TD",
                "rushing_LONG",
            ]
        ]

    elif filter_by_stat_category == True and stat_category == "receiving":
        try:
            final_df = final_df.astype(
                {
                    "receiving_REC": "int",
                    "receiving_YDS": "int",
                }
            )
        except:
            logging.warning(
                "Could not reformat [receiving_REC] and [receiving_YDS] into integers."
            )

        final_df.loc[final_df["receiving_REC"] > 0, "receiving_AVG"] = (
            final_df["receiving_YDS"] / final_df["receiving_REC"]
        )

        final_df = final_df[
            [
                "season",
                "team_name",
                "team_confrence",
                "player_id",
                "player_name",
                # REC
                "receiving_REC",
                "receiving_YDS",
                "receiving_AVG",
                "receiving_TD",
                "receiving_LONG",
            ]
        ]

    elif filter_by_stat_category == True and stat_category == "fumbles":
        final_df = final_df[
            [
                "season",
                "team_name",
                "team_confrence",
                "player_id",
                "player_name",
                # FUM
                "fumbles_FUM",
                "fumbles_LOST",
                "fumbles_REC",
            ]
        ]

    elif filter_by_stat_category == True and stat_category == "defensive":
        final_df = final_df[
            [
                "season",
                "team_name",
                "team_confrence",
                "player_id",
                "player_name",
                # DEFENSE
                "defensive_TOT",
                "defensive_SOLO",
                "defensive_TFL",
                "defensive_QB HUR",
                "defensive_SACKS",
                "defensive_PD",
                "defensive_TD",
            ]
        ]

    elif filter_by_stat_category == True and stat_category == "interceptions":
        final_df = final_df[
            [
                "season",
                "team_name",
                "team_confrence",
                "player_id",
                "player_name",
                # INT
                "interceptions_INT",
                "interceptions_YDS",
                "interceptions_TD",
            ]
        ]

    elif filter_by_stat_category == True and stat_category == "punting":
        try:
            final_df = final_df.astype(
                {
                    "punting_NO": "int",
                    "punting_YDS": "int",
                }
            )
        except:
            logging.warning(
                "Could not reformat [punting_YDS] and [punting_NO] into integers."
            )

        final_df.loc[final_df["punting_NO"] > 0, "punting_AVG"] = (
            final_df["punting_YDS"] / final_df["punting_NO"]
        )

        final_df = final_df[
            [
                "season",
                "team_name",
                "team_confrence",
                "player_id",
                "player_name",
                # PUNT
                "punting_NO",
                "punting_YDS",
                "punting_AVG",
                "punting_TB",
                "punting_In 20",
                "punting_LONG",
            ]
        ]

    elif filter_by_stat_category == True and stat_category == "kicking":
        try:
            final_df = final_df.astype(
                {
                    "kicking_FGM": "int",
                    "kicking_FGA": "int",
                    "kicking_XPM": "int",
                    "kicking_XPA": "int",
                }
            )
        except:
            logging.warning(
                "Could not reformat the following columns into integers.:"
                + "\n-[kicking_FGM]"
                + "\n-[kicking_FGA]"
                + "\n-[kicking_XPM]"
                + "\n-[kicking_XPA]"
            )

        final_df.loc[final_df["kicking_FGA"] > 0, "kicking_FG%"] = (
            final_df["kicking_FGM"] / final_df["kicking_FGA"]
        )

        final_df.loc[final_df["kicking_XPA"] > 0, "kicking_XP%"] = (
            final_df["kicking_XPM"] / final_df["kicking_XPA"]
        )

        final_df = final_df[
            [
                "season",
                "team_name",
                "team_confrence",
                "player_id",
                "player_name",
                # KICK
                "kicking_FGM",
                "kicking_FGA",
                "kicking_FG%",
                "kicking_LONG",
                "kicking_XPM",
                "kicking_XPA" "kicking_XP%",
            ]
        ]

    elif filter_by_stat_category == True and stat_category == "kickReturns":
        try:
            final_df = final_df.astype(
                {
                    "kickReturns_NO": "int",
                    "kickReturns_YDS": "int",
                }
            )
        except:
            logging.warning(
                "Could not reformat [passing_COMP] and [kickReturns_YDS] into integers."
            )

        final_df.loc[final_df["kickReturns_NO"] > 0, "kickReturns_AVG"] = (
            final_df["kickReturns_YDS"] / final_df["kickReturns_NO"]
        )

        final_df = final_df[
            [
                "season",
                "team_name",
                "team_confrence",
                "player_id",
                "player_name",
                # KR
                "kickReturns_NO",
                "kickReturns_YDS",
                "kickReturns_AVG",
                "kickReturns_TD",
                "kickReturns_LONG",
            ]
        ]

    elif filter_by_stat_category == True and stat_category == "puntReturns":
        try:
            final_df = final_df.astype(
                {
                    "puntReturns_NO": "int",
                    "puntReturns_YDS": "int",
                }
            )
        except:
            logging.warning(
                "Could not reformat [passing_COMP] and [puntReturns_YDS] into integers."
            )

        final_df.loc[final_df["puntReturns_NO"] > 0, "puntReturns_AVG"] = (
            final_df["puntReturns_YDS"] / final_df["puntReturns_NO"]
        )

        final_df = final_df[
            [
                "season",
                "team_name",
                "team_confrence",
                "player_id",
                "player_name",
                # KR
                "puntReturns_NO",
                "puntReturns_YDS",
                "puntReturns_AVG",
                "puntReturns_TD",
                "puntReturns_LONG",
            ]
        ]

    return final_df


def get_cfbd_transfer_portal_data(
    season: int,
    api_key: str = None,
    api_key_dir: str = None,
    return_as_dict: bool = False,
):
    """
    Get player usage data (A.K.A., the percentages for how often a player touched the ball),
    for a given season, from the CFBD API.

    Parameters
    ----------
    `season` (int, mandatory):
        Required argument.
        Specifies the season you want CFB transfer portal data from.
        This must be specified, otherwise this package, and by extension
        the CFBD API, will not accept the request to get CFB transfer portal data stats.

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

    from cfbd_json_py.players import get_cfbd_transfer_portal_data


    cfbd_key = "tigersAreAwsome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwsome":
        print("Using the user's API key declared in this script for this example.")

        # Get Transfer Portal data for the 2021 CFB season.
        print("Get Transfer Portal data for the 2021 CFB season.")
        json_data = get_cfbd_transfer_portal_data(
            api_key=cfbd_key,
            season=2021
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_transfer_portal_data(
            api_key=cfbd_key,
            season=2021,
            return_as_dict=True
        )
        print(json_data)

    else:
        # Alternatively, if the CFBD API key exists in this python environment,
        # or it's been set by cfbd_json_py.utls.set_cfbd_api_token(),
        # you could just call these functions directly, without setting the API key
        # in the script.
        print("Using the user's API key suposedly loaded into this python environment for this example.")

        # Get Transfer Portal data for the 2021 CFB season.
        print("Get Transfer Portal data for the 2021 CFB season.")
        json_data = get_cfbd_transfer_portal_data(
            season=2021
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_transfer_portal_data(
            season=2021,
            return_as_dict=True
        )
        print(json_data)

    ```
    Returns
    ----------
    A pandas `DataFrame` object with transfer portal data,
    or (if `return_as_dict` is set to `True`)
    a dictionary object with transfer portal data.

    """
    now = datetime.now()
    url = "https://api.collegefootballdata.com/player/portal"

    portal_df = pd.DataFrame()
    row_df = pd.DataFrame()

    if api_key != None:
        real_api_key = api_key
        del api_key
    else:
        real_api_key = get_cfbd_api_token(api_key_dir=api_key_dir)

    if real_api_key == "tigersAreAwsome":
        raise ValueError("You actually need to change `cfbd_key` to your CFBD API key.")
    elif "Bearer " in real_api_key:
        pass
    elif "Bearer" in real_api_key:
        real_api_key = real_api_key.replace("Bearer", "Bearer ")
    else:
        real_api_key = "Bearer " + real_api_key

    if season == None:
        # This should never happen without user tampering, but if it does,
        # we need to raise an error, because the CFBD API will refuse this call without a valid season.
        raise SystemError(
            "I don't know how, I don't know why, "
            + "but you managed to call this function while `season` was `None` (NULL),"
            + " and the function got to this point in the code."
            + "\nIf you have a GitHub account, "
            + "please raise an issue on this python package's GitHub page:\n"
            + "https://github.com/armstjc/cfbd-json-py/issues"
        )
    elif season > (now.year + 1):
        raise ValueError(f"`season` cannot be greater than {season}.")
    elif season < 2017:
        raise ValueError(f"Transfer portal wasn't really a thing in {season}.")

    # URL builder
    ########################################################################################################################################################################################################

    ## required by API
    url += f"?year={season}"

    headers = {"Authorization": f"{real_api_key}", "accept": "application/json"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        pass
    elif response.status_code == 401:
        raise ConnectionRefusedError(
            f"Could not connect. The connection was refused.\nHTTP Status Code 401."
        )
    else:
        raise ConnectionError(
            f"Could not connect.\nHTTP Status code {response.status_code}"
        )

    json_data = response.json()

    if return_as_dict == True:
        return json_data

    # for player in tqdm(json_data):
    #     row_df = pd.DataFrame({"season": season}, index=[0])
    #     row_df["first_name"] = player["firstName"]
    #     row_df["last_name"] = player["lastName"]
    #     row_df["position"] = player["position"]
    #     row_df["origin_team"] = player["origin"]
    #     row_df["destination_team"] = player["destination"]
    #     row_df["transferDate"] = player["transferDate"]
    #     row_df["player_rating"] = player["rating"]
    #     row_df["player_stars"] = player["stars"]
    #     row_df["player_eligibility"] = player["eligibility"]
    #     portal_df = pd.concat([portal_df, row_df], ignore_index=True)

    #     del row_df
    portal_df = pd.json_normalize(json_data)
    portal_df.rename(
        columns={
            "firstName":"first_name",
            "lastName":"last_name",
            "position":"position_abv",
            "origin":"origin_team",
            "destination":"destination_team",
            "transferDate":"transfer_date",
            "rating":"rating",
            "stars":"stars",
            "eligibility":"eligibility",
        },
        inplace=True,
    )
    return portal_df
