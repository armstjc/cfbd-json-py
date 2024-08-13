# Creation Date: 08/30/2023 01:13 EDT
# Last Updated Date: 08/13/2024 02:10 PM EDT
# Author: Joseph Armstrong (armstrongjoseph08@gmail.com)
# File Name: plays.py
# Purpose: Houses functions pertaining to CFB play data within the CFBD API.
###############################################################################

import logging
from datetime import datetime

import pandas as pd
import requests
from tqdm import tqdm

from cfbd_json_py.utls import get_cfbd_api_token


def get_cfbd_pbp_data(
    season: int,
    week: int,
    api_key: str = None,
    api_key_dir: str = None,
    season_type: str = "regular",
    # required if team, offense, or defense, not specified
    team: str = None,
    offensive_team: str = None,
    defensive_team: str = None,
    conference: str = None,
    offensive_conference: str = None,
    defensive_conference: str = None,
    play_type: int = None,
    ncaa_division: str = "fbs",
    return_as_dict: bool = False,
):
    """
    Allows you to get CFB play-by-play (PBP) data from the CFBD API.

    Parameters
    ----------
    `season` (int, mandatory):
        Required argument.
        Specifies the season you want CFB PBP data from.
        This must be specified, otherwise this package, and by extension
        the CFBD API, will not accept the request to get CFB PBP data.

    `week` (int, optional):
        Required argument.
        This is the week you want CFB PBP data from.
        For a list of valid season-week combinations,
        use `cfbd_json_py.games.get_cfbd_season_weeks()`.

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

    `week` (int, optional):
        Optional argument.
        If `week` is set to an integer, this function will attempt
        to load CFB poll rankings data from games in that season,
        and in that week.

    `season_type` (str, semi-optional):
        Semi-optional argument.
        By default, this will be set to "regular", for the CFB regular season.
        If you want CFB poll rankings data for non-regular season games,
        set `season_type` to "postseason".
        If `season_type` is set to anything but "regular" or "postseason",
        a `ValueError()` will be raised.

    `offensive_team` (str, optional):
        Optional argument.
        If you only want CFB drive data from a team, while they are on offense,
        regardless if they are the home/away team,
        set `team` to the name of the team you want CFB drive data from.

    `defensive_team` (str, optional):
        Optional argument.
        If you only want CFB drive data from a team, while they are on defense,
        regardless if they are the home/away team,
        set `team` to the name of the team you want CFB drive data from.

    `conference` (str, optional):
        Optional argument.
        If you only want CFB drive data from games
        involving teams from a specific conference,
        set `conference` to the abbreviation
        of the conference you want CFB drive data from.
        For a list of conferences,
        use the `cfbd_json_py.conferences.get_cfbd_conference_info()`
        function.

    `offensive_conference` (str, optional):
        Optional argument.
        If you only want CFB drive data from games
        where the offensive team is from a specific conference,
        set `conference` to the abbreviation
        of the conference you want CFB drive data from.
        For a list of conferences,
        use the `cfbd_json_py.conferences.get_cfbd_conference_info()`
        function.

    `defensive_conference` (str, optional):
        Optional argument.
        If you only want CFB drive data from games
        where the defensive team is from a specific conference,
        set `conference` to the abbreviation
        of the conference you want CFB drive data from.
        For a list of conferences,
        use the `cfbd_json_py.conferences.get_cfbd_conference_info()`
        function.

    `play_type` (int, optional):
        Optional argument.
        If want to drill down, and only get plays of a specific type,
        (like rushing, passing, kicking plays),
        set `play_type` to the ID for the play type you want returned.
        To retrieve a list of valid play type IDs,
        use `cfbd_json_py.plays.get_cfbd_pbp_play_types()`.

    `ncaa_division` (str, semi-optional):
        Semi-optional argument.
        By default, `ncaa_division` will be set to "fbs",
        short for the Football Bowl Subdivision (FBS),
        formerly known as D1-A (read as "division one single A"),
        the highest level in the NCAA football pyramid,
        where teams can scholarship up to 85 players
        on their football team solely for athletic ability,
        and often have the largest athletics budgets
        within the NCAA.

        Other valid inputs are:
        - "fcs": Football Championship Subdivision (FCS),
            formerly known as D1-AA (read as "division one double A").
            An FCS school is still in the 1st division of the NCAA,
            making them eligible for the March Madness tournament,
            but may not have the resources to compete at the FBS level
            at this time. FCS schools are limited to 63 athletic scholarships
            for football.
        - "ii": NCAA Division II. Schools in this and D3 are not
            eligible for the March Madness tournament,
            and are limited to 36 athletic scholarships
            for their football team.
        - "iii": NCAA Division III. The largest single division within the
            NCAA football pyramid.
            D3 schools have the distinction of being part of
            the only NCAA division that cannot give out scholarships solely
            for athletic ability.


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

    from cfbd_json_py.plays import get_cfbd_pbp_data


    cfbd_key = "tigersAreAwesome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwesome":
        print(
            "Using the user's API key declared in this script " +
            "for this example."
        )

        # Get CFB PBP data for
        # the University of Cincinnati Football Team
        # for week 10 of the 2021 season
        print("Get CFB PBP data for week 10 of the 2021 season.")
        json_data = get_cfbd_pbp_data(
            api_key=cfbd_key,
            season=2021,
            week=10,
            team="Cincinnati"
        )
        print(json_data)
        time.sleep(5)

        # Get CFB PBP data for when the Ohio State Buckeyes Football Team
        # was on offense for week 10 of the 2021 season
        print(
            "Get CFB PBP data for when the Ohio State Buckeyes " +
            "Football Team was on offense for week 10 of the 2021 season"
        )
        json_data = get_cfbd_pbp_data(
            api_key=cfbd_key,
            season=2021,
            week=10,
            offensive_team="Ohio State"
        )
        print(json_data)
        time.sleep(5)

        # Get CFB PBP data for when the LSU Tigers Football Team
        # was on defense for week 10 of the 2021 season
        print(
            "Get CFB PBP data for when the LSU Tigers Football Team " +
            "was on defense for week 10 of the 2021 season"
        )
        json_data = get_cfbd_pbp_data(
            api_key=cfbd_key,
            season=2021,
            week=10,
            defensive_team="LSU"
        )
        print(json_data)
        time.sleep(5)

        # Get CFB PBP data for teams in the Southeastern Conference (SEC)
        # for week 10 of the 2021 CFB season.
        print(
            "Get CFB PBP data for teams in " +
            "the Southeastern Conference (SEC) " +
            "for week 10 of the 2021 CFB season."
        )
        json_data = get_cfbd_pbp_data(
            api_key=cfbd_key,
            season=2021,
            week=10,
            conference="SEC"
        )
        print(json_data)
        time.sleep(5)

        # Get CFB PBP data for teams in the Big 10 (B1G) Conference,
        # while on offense, for week 10 of the 2021 CFB season.
        print(
            "Get CFB PBP data for teams in the Big 10 (B1G) Conference " +
            "while on offense, for week 10 of the 2021 CFB season."
        )
        json_data = get_cfbd_pbp_data(
            api_key=cfbd_key,
            season=2021,
            week=10,
            offensive_conference="B1G"
        )
        print(json_data)
        time.sleep(5)

        # Get CFB PBP data for teams in the Atlantic Coast Conference (ACC),
        # while on defense, for week 10 of the 2021 CFB season.
        print(
            "Get CFB PBP data for teams in " +
            "the Atlantic Coast Conference (ACC), while on defense, " +
            "for week 10 of the 2021 CFB season."
        )
        json_data = get_cfbd_pbp_data(
            api_key=cfbd_key,
            season=2021,
            week=10,
            defensive_conference="ACC"
        )
        print(json_data)
        time.sleep(5)

        # Get every run play for week 10 of the 2021 CFB season.
        print("Get every run play for week 10 of the 2021 CFB season.")
        json_data = get_cfbd_pbp_data(
            api_key=cfbd_key,
            season=2021,
            week=10,
            play_type=5 # ID for run plays.
            # See `cfbd_json_py.plays.get_cfbd_pbp_play_types()`
            # for a list of play type IDs.
        )
        print(json_data)
        time.sleep(5)

        # Get CFB PBP data for Football Championship Subdivision (FCS)
        # teams in week 10 of the 2021 CFB season.
        print(
            "Get CFB PBP data for Football Championship Subdivision (FCS)" +
            " teams in week 10 of the 2021 CFB season."
        )
        json_data = get_cfbd_pbp_data(
            api_key=cfbd_key,
            season=2021,
            week=10,
            ncaa_division="fcs"
        )
        print(json_data)
        time.sleep(5)

        # Get CFB PBP data for week 10 of the 2021 season
        print("Get CFB PBP data for week 10 of the 2021 season.")
        json_data = get_cfbd_pbp_data(
            api_key=cfbd_key,
            season=2021,
            week=10
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print(
            "You can also tell this function to just return the API call " +
            "as a Dictionary (read: JSON) object."
        )
        json_data = get_cfbd_pbp_data(
            api_key=cfbd_key,
            season=2020,
            week=10,
            defensive_team="LSU",
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

        # Get CFB PBP data for the University of Cincinnati Football Team
        # for week 10 of the 2021 season
        print(
            "Get CFB play-by-play (PBP) data for " +
            "the University of Cincinnati Football Team " +
            "for week 10 of the 2021 season"
        )
        json_data = get_cfbd_pbp_data(
            season=2021,
            week=10,
            team="Cincinnati"
        )
        print(json_data)
        time.sleep(5)

        # Get CFB PBP data for when the Ohio State Buckeyes Football Team
        # was on offense for week 10 of the 2021 season
        print(
            "Get CFB PBP data for when " +
            "the Ohio State Buckeyes Football Team was on offense " +
            "for week 10 of the 2021 season"
        )
        json_data = get_cfbd_pbp_data(
            season=2021,
            week=10,
            offensive_team="Ohio State"
        )
        print(json_data)
        time.sleep(5)

        # Get CFB PBP data for when the LSU Tigers Football Team
        # was on defense for week 10 of the 2021 season
        print(
            "Get CFB PBP data for when the LSU Tigers Football Team " +
            "was on defense for week 10 of the 2021 season"
        )
        json_data = get_cfbd_pbp_data(
            season=2021,
            week=10,
            defensive_team="LSU"
        )
        print(json_data)
        time.sleep(5)

        # Get CFB PBP data for teams in the Southeastern Conference (SEC)
        # for week 10 of the 2021 CFB season.
        print(
            "Get CFB PBP data for teams in " +
            "the Southeastern Conference (SEC) " +
            "for week 10 of the 2021 CFB season."
        )
        json_data = get_cfbd_pbp_data(
            season=2021,
            week=10,
            conference="SEC"
        )
        print(json_data)
        time.sleep(5)

        # Get CFB PBP data for teams in the Big 10 (B1G) Conference,
        # while on offense, for week 10 of the 2021 CFB season.
        print(
            "Get CFB PBP data for teams in the Big 10 (B1G) Conference " +
            "while on offense, for week 10 of the 2021 CFB season."
        )
        json_data = get_cfbd_pbp_data(
            season=2021,
            week=10,
            offensive_conference="B1G"
        )
        print(json_data)
        time.sleep(5)

        # Get CFB PBP data for teams in the Atlantic Coast Conference (ACC),
        # while on defense, for week 10 of the 2021 CFB season.
        print(
            "Get CFB PBP data for teams in " +
            "the Atlantic Coast Conference (ACC), while on defense, " +
            "for week 10 of the 2021 CFB season."
        )
        json_data = get_cfbd_pbp_data(
            season=2021,
            week=10,
            defensive_conference="ACC"
        )
        print(json_data)
        time.sleep(5)

        # Get every run play for week 10 of the 2021 CFB season.
        print("Get every run play for week 10 of the 2021 CFB season.")
        json_data = get_cfbd_pbp_data(
            season=2021,
            week=10,
            play_type=5 # ID for run plays.
            # See `cfbd_json_py.plays.get_cfbd_pbp_play_types()`
            # for a list of play type IDs.
        )
        print(json_data)
        time.sleep(5)

        # Get CFB PBP data for Football Championship Subdivision (FCS)
        # teams in week 10 of the 2021 CFB season.
        print(
            "Get CFB PBP data for Football Championship Subdivision (FCS)" +
            " teams in week 10 of the 2021 CFB season."
        )
        json_data = get_cfbd_pbp_data(
            season=2021,
            week=10,
            ncaa_division="fcs"
        )
        print(json_data)
        time.sleep(5)

        # Get CFB PBP data for week 10 of the 2021 season
        print("Get CFB PBP data for week 10 of the 2021 season.")
        json_data = get_cfbd_pbp_data(
            season=2021,
            week=10
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print(
            "You can also tell this function to just return the API call " +
            "as a Dictionary (read: JSON) object."
        )
        json_data = get_cfbd_pbp_data(
            season=2020,
            week=10,
            defensive_team="LSU",
            return_as_dict=True
        )
        print(json_data)

    ```
    Returns
    ----------
    A pandas `DataFrame` object with CFB PBP data,
    or (if `return_as_dict` is set to `True`)
    a dictionary object with CFB PBP data.

    """

    now = datetime.now()
    pbp_df = pd.DataFrame()
    # row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/plays"

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

    if season is None:
        # This should never happen without user tampering, but if it does,
        # we need to raise an error,
        # because the CFBD API will refuse this call without a valid season.
        raise SystemError(
            "I don't know how, I don't know why, "
            + "but you managed to call this function "
            + "while `season` was `None` (NULL),"
            + " and the function got to this point in the code."
            + "\nIf you have a GitHub account, "
            + "please raise an issue on this python package's GitHub page:\n"
            + "https://github.com/armstjc/cfbd-json-py/issues"
        )
    elif season > (now.year + 1):
        raise ValueError(f"`season` cannot be greater than {season}.")
    elif season < 1869:
        raise ValueError("`season` cannot be less than 1869.")

    if season_type != "regular" and season_type != "postseason":
        raise ValueError(
            '`season_type` must be set to either ' +
            '"regular" or "postseason" for this function to work.'
        )

    if (
        ncaa_division.lower() == "fbs"
        or ncaa_division.lower() == "fcs"
        or ncaa_division.lower() == "ii"
        or ncaa_division.lower() == "iii"
    ):
        pass
    else:
        raise ValueError(
            "An invalid NCAA Division was inputted when calling this function."
            + '\nValid inputs are:\n-"fbs"\n-"fcs"\n-"ii"\n-"iii"'
            + f"\n\nYou entered:\n{ncaa_division}"
        )

    if week is None and (
        team is None and offensive_team is None and defensive_team is None
    ):
        raise ValueError(
            "If `week` is set to `None` when calling this function, "
            + "the following variables must be set "
            + "to a valid non-null variable:"
            + "\n- `team`"
            + "\n- `offensive_team`"
            + "\n- `defensive_team`"
        )
    # URL builder
    ##########################################################################

    # Required by API
    url += f"?seasonType={season_type}"

    url += f"&year={season}"

    url += f"&week={week}"

    if team is not None:
        url += f"&team={team}"

    if offensive_team is not None:
        url += f"&offense={offensive_team}"

    if defensive_team is not None:
        url += f"&defense={defensive_team}"

    if conference is not None:
        url += f"&conference={conference}"

    if offensive_conference is not None:
        url += f"&offenseConference={offensive_conference}"

    if defensive_conference is not None:
        url += f"&defenseConference={defensive_conference}"

    if ncaa_division is not None:
        url += f"&classification={ncaa_division}"

    if play_type is not None:
        url += f"&playType={play_type}"

    headers = {
        "Authorization": f"{real_api_key}",
        "accept": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        pass
    elif response.status_code == 401:
        raise ConnectionRefusedError(
            "Could not connect. The connection was refused." +
            "\nHTTP Status Code 401."
        )
    else:
        raise ConnectionError(
            f"Could not connect.\nHTTP Status code {response.status_code}"
        )

    json_data = response.json()

    if return_as_dict is True:
        return json_data

    pbp_df = pd.json_normalize(json_data)
    pbp_df.rename(
        columns={
            "id": "play_id",
            "offense": "offensive_team_name",
            "offense_conference": "offensive_conference_name",
            "defense": "defensive_team_name",
            "defense_conference": "defensive_conference_name",
            "home": "home_team_name",
            "away": "away_team_name",
            "clock.minutes": "clock_minutes",
            "clock.seconds": "clock_seconds",
        },
        inplace=True,
    )
    return pbp_df


def get_cfbd_pbp_play_types(
    api_key: str = None, api_key_dir: str = None, return_as_dict: bool = False
):
    """
    Allows you to get CFBD PBP play types from the CFBD API.

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
    ```
    Returns
    ----------
    A pandas `DataFrame` object with CFBD PBP play types,
    or (if `return_as_dict` is set to `True`)
    a dictionary object with CFBD PBP play types.

    """
    # now = datetime.now()
    plays_df = pd.DataFrame()
    row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/play/types"

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
            "Could not connect. The connection was refused." +
            "\nHTTP Status Code 401."
        )
    else:
        raise ConnectionError(
            f"Could not connect.\nHTTP Status code {response.status_code}"
        )

    json_data = response.json()

    if return_as_dict is True:
        return json_data

    for p in tqdm(json_data):
        p_id = p["id"]
        row_df = pd.DataFrame({"play_type_id": p_id}, index=[0])
        row_df["play_type_text"] = p["text"]
        row_df["play_type_abv"] = p["abbreviation"]
        plays_df = pd.concat([plays_df, row_df], ignore_index=True)

        del row_df
        del p_id

    return plays_df


def get_cfbd_pbp_stats(
    api_key: str = None,
    api_key_dir: str = None,
    season: int = None,
    week: int = None,
    team: str = None,
    game_id: int = None,
    athlete_id: int = None,
    stat_type_id: int = None,
    season_type: str = "both",  # "regular", "postseason", or "both"
    conference: str = None,
    return_as_dict: bool = False,
):
    """
    Allows you to get stats for various players
    from CFB play-by-play (PBP) data within the CFBD API.
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

    `season` (int, optional):
        Semi-optional argument.
        Specifies the season you want CFB PBP data from.
        This must be specified, otherwise this package, and by extension
        the CFBD API, will not accept the request to get CFB PBP data.

    `week` (int, optional):
        Optional argument.
        If `week` is set to an integer, this function will attempt
        to load CFB poll rankings data from games in that season,
        and in that week.

    `team` (str, optional):
        Optional argument.
        If you only want stats for a specific team,
        set `team` to the name of that specific team.

    `game_id` (int, optional):
        Optional argument.
        If you only want stats for a specific game,
        set `game_id` to the ID of that specific game.

    `athlete_id` (int, optional):
        Optional argument.
        If you only want stats for a specific player,
        set `athlete_id` to the ID of the player you want stats for.

    `stats_type_id` (int, optional):
        Optional argument.
        If want to drill down, and only get plays of a specific type,
        (like rushing, passing, kicking plays),
        set `play_type` to the ID for the play type you want returned.
        To retrieve a list of valid play type IDs,
        use `cfbd_json_py.plays.get_cfbd_pbp_play_types()`.

    `season_type` (str, semi-optional):
        Semi-optional argument.
        By default, this will be set to "regular", for the CFB regular season.
        If you want CFB poll rankings data for non-regular season games,
        set `season_type` to "postseason".
        If `season_type` is set to anything but "regular" or "postseason",
        a `ValueError()` will be raised.

    `conference` (str, optional):
        Optional argument.
        If you only want CFB drive data from games
        involving teams from a specific conference,
        set `conference` to the abbreviation
        of the conference you want CFB drive data from.
        For a list of conferences,
        use the `cfbd_json_py.conferences.get_cfbd_conference_info()`
        function.

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

    from cfbd_json_py.plays import get_cfbd_pbp_stats


    cfbd_key = "tigersAreAwesome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwesome":
        print(
            "Using the user's API key declared in this script " +
            "for this example."
        )

        # Get CFB PBP stats data for the 2020 CFB season.
        print("Get CFB PBP stats data for the 2020 CFB season.")
        json_data = get_cfbd_pbp_stats(
            api_key=cfbd_key,
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get CFB PBP stats data for week 10 of the 2020 CFB season.
        print("Get CFB PBP stats data for week 10 of the 2020 CFB season.")
        json_data = get_cfbd_pbp_stats(
            api_key=cfbd_key,
            season=2020,
            week=10
        )
        print(json_data)
        time.sleep(5)

        # Get CFB PBP stats data for a 2019 game between
        # the Ohio State Buckeyes and Clemson Tigers football teams.
        print(
            "Get CFB PBP stats data for a 2019 game between " +
            "the Ohio State Buckeyes and Clemson Tigers football teams."
        )
        json_data = get_cfbd_pbp_stats(
            api_key=cfbd_key,
            game_id=401135279
        )
        print(json_data)
        time.sleep(5)

        # Get CFB PBP stats data for Trevor Lawrence (athlete ID #4360310)
        # during the 2020 CFB Season.
        print("Get CFB PBP stats data for the 2020 CFB season.")
        json_data = get_cfbd_pbp_stats(
            api_key=cfbd_key,
            season=2020,
            athlete_id=4360310
        )
        print(json_data)
        time.sleep(5)

        # Get CFB PBP stats data for Trevor Lawrence (athlete ID #4360310)
        # during the 2020 CFB Season,
        # but only return plays where Lawrence scored a touchdown.
        print("Get CFB PBP stats data for the 2020 CFB season.")
        json_data = get_cfbd_pbp_stats(
            api_key=cfbd_key,
            season=2020,
            athlete_id=4360310,
            stat_type_id=22
        )
        print(json_data)
        time.sleep(5)

        # Get CFB PBP stats data for the 2020 CFB season,
        # but only for postseason games.
        print("Get CFB PBP stats data for the 2020 CFB season.")
        json_data = get_cfbd_pbp_stats(
            api_key=cfbd_key,
            season=2020,
            season_type="postseason"
        )
        print(json_data)
        time.sleep(5)

        # Get CFB PBP stats data for the 2020 CFB season,
        # but only for Big 10 (B1G) games.
        print("Get CFB PBP stats data for the 2020 CFB season.")
        json_data = get_cfbd_pbp_stats(
            api_key=cfbd_key,
            season=2020,
            conference="B1G"
        )
        print(json_data)
        time.sleep(5)

        # Get CFB PBP stats data for the 2020 CFB season.
        print("Get CFB PBP stats data for the 2020 CFB season.")
        json_data = get_cfbd_pbp_stats(
            api_key=cfbd_key,
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print(
            "You can also tell this function to just return the API call " +
            "as a Dictionary (read: JSON) object."
        )
        json_data = get_cfbd_pbp_stats(
            api_key=cfbd_key,
            season=2020,
            week=10,
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

        # Get CFB PBP stats data for the 2020 CFB season.
        print("Get CFB PBP stats data for the 2020 CFB season.")
        json_data = get_cfbd_pbp_stats(
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get CFB PBP stats data for week 10 of the 2020 CFB season.
        print("Get CFB PBP stats data for week 10 of the 2020 CFB season.")
        json_data = get_cfbd_pbp_stats(
            season=2020,
            week=10
        )
        print(json_data)
        time.sleep(5)

        # Get CFB PBP stats data for a 2019 game between
        # the Ohio State Buckeyes and Clemson Tigers football teams.
        print(
            "Get CFB PBP stats data for a 2019 game between " +
            "the Ohio State Buckeyes and Clemson Tigers football teams."
        )
        json_data = get_cfbd_pbp_stats(
            game_id=401135279
        )
        print(json_data)
        time.sleep(5)

        # Get CFB PBP stats data for Trevor Lawrence (athlete ID #4360310)
        # during the 2020 CFB Season.
        print("Get CFB PBP stats data for the 2020 CFB season.")
        json_data = get_cfbd_pbp_stats(
            season=2020,
            athlete_id=4360310
        )
        print(json_data)
        time.sleep(5)

        # Get CFB PBP stats data for Trevor Lawrence (athlete ID #4360310)
        # during the 2020 CFB Season,
        # but only return plays where Lawrence scored a touchdown.
        print("Get CFB PBP stats data for the 2020 CFB season.")
        json_data = get_cfbd_pbp_stats(
            season=2020,
            athlete_id=4360310,
            stat_type_id=22
        )
        print(json_data)
        time.sleep(5)

        # Get CFB PBP stats data for the 2020 CFB season,
        # but only for postseason games.
        print("Get CFB PBP stats data for the 2020 CFB season.")
        json_data = get_cfbd_pbp_stats(
            season=2020,
            season_type="postseason"
        )
        print(json_data)
        time.sleep(5)

        # Get CFB PBP stats data for the 2020 CFB season,
        # but only for Big 10 (B1G) games.
        print("Get CFB PBP stats data for the 2020 CFB season.")
        json_data = get_cfbd_pbp_stats(
            season=2020,
            conference="B1G"
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print(
            "You can also tell this function to just return the API call " +
            "as a Dictionary (read: JSON) object."
        )
        json_data = get_cfbd_pbp_stats(
            season=2020,
            week=10,
            return_as_dict=True
        )
        print(json_data)

    ```
    Returns
    ----------
    A pandas `DataFrame` object with CFB PBP data,
    or (if `return_as_dict` is set to `True`)
    a dictionary object with CFB PBP data.

    """
    now = datetime.now()
    pbp_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/play/stats"

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

    if season is not None and (season > (now.year + 1)):
        raise ValueError(f"`season` cannot be greater than {season}.")
    elif season is not None and season < 1869:
        raise ValueError("`season` cannot be less than 1869.")

    if (
        season_type != "regular"
        and season_type != "postseason"
        and season_type != "both"
    ):
        raise ValueError(
            '`season_type` must be set to either ' +
            '"regular", "postseason", or "both" for this function to work.'
        )

    if season is None and game_id is None:
        logging.warn(
            "This endpoint only returns the top 1,000 results. "
            + "Not setting a value for `season` or `game_id` "
            + "is not a recommended practice."
        )
    elif season is not None and game_id is None:
        logging.warn(
            "Setting a value for both `season` and `game_id` "
            + "may not yeld the results you want. "
            + "If you just want PBP stats for a valid game ID, "
            + "just set `game_id` to a valid game ID."
        )

    # URL builder
    ##########################################################################

    url_elements = 0

    if season_type is not None and url_elements == 0:
        url += f"?seasonType={season_type}"
        url_elements += 1
    elif season_type is not None:
        url += f"&seasonType={season_type}"
        url_elements += 1

    if season is not None and url_elements == 0:
        url += f"?year={season}"
        url_elements += 1
    elif season is not None:
        url += f"&year={season}"
        url_elements += 1

    if week is not None and url_elements == 0:
        url += f"?week={week}"
        url_elements += 1
    elif week is not None:
        url += f"&week={week}"
        url_elements += 1

    if team is not None and url_elements == 0:
        url += f"?team={team}"
        url_elements += 1
    elif team is not None:
        url += f"&team={team}"
        url_elements += 1

    if conference is not None and url_elements == 0:
        url += f"&conference={conference}"
        url_elements += 1
    elif conference is not None:
        url += f"&conference={conference}"
        url_elements += 1

    if game_id is not None and url_elements == 0:
        url += f"&gameId={game_id}"
        url_elements += 1
    elif game_id is not None:
        url += f"&gameId={game_id}"
        url_elements += 1

    if athlete_id is not None and url_elements == 0:
        url += f"&athleteId={athlete_id}"
        url_elements += 1
    elif athlete_id is not None:
        url += f"&athleteId={athlete_id}"
        url_elements += 1

    if stat_type_id is not None and url_elements == 0:
        url += f"&statTypeId={stat_type_id}"
        url_elements += 1
    elif stat_type_id is not None:
        url += f"&statTypeId={stat_type_id}"
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
            "Could not connect. The connection was refused." +
            "\nHTTP Status Code 401."
        )
    else:
        raise ConnectionError(
            f"Could not connect.\nHTTP Status code {response.status_code}"
        )

    json_data = response.json()

    if return_as_dict is True:
        return json_data

    pbp_df = pd.json_normalize(json_data)
    pbp_df.rename(
        columns={
            "gameId": "game_id",
            "teamScore": "team_score",
            "opponentScore": "opponent_score",
            "driveId": "drive_id",
            "playId": "play_id",
            "yardsToGoal": "yards_to_goal",
            "athleteId": "athlete_id",
            "athleteName": "athlete_name",
            "statType": "stat_type",
        },
        inplace=True,
    )
    # TODO: Implement an option to put all stats for
    # a specific game on a single line.
    return pbp_df


def get_cfbd_pbp_stat_types(
    api_key: str = None, api_key_dir: str = None, return_as_dict: bool = False
):
    """
    Allows you to get CFBD PBP stat types from the CFBD API.

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
    ```
    Returns
    ----------
    A pandas `DataFrame` object with CFBD PBP stat types,
    or (if `return_as_dict` is set to `True`)
    a dictionary object with CFBD PBP stat types.

    """
    # now = datetime.now()
    plays_df = pd.DataFrame()
    row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/play/types"

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
            "Could not connect. The connection was refused." +
            "\nHTTP Status Code 401."
        )
    else:
        raise ConnectionError(
            f"Could not connect.\nHTTP Status code {response.status_code}"
        )

    json_data = response.json()

    if return_as_dict is True:
        return json_data

    for p in tqdm(json_data):
        p_id = p["id"]
        row_df = pd.DataFrame({"stat_type_id": p_id}, index=[0])
        row_df["stat_type_text"] = p["name"]
        plays_df = pd.concat([plays_df, row_df], ignore_index=True)

        del row_df
        del p_id

    return plays_df


###############################################################################
# Patreon Only Functions.
#   No caching, because the entire point of these functions are to get people
#   data ASAP, and right before kickoff.
###############################################################################


def get_cfbd_live_pbp_data(
    game_id: int,
    api_key: str = None,
    api_key_dir: str = None,
    # return_as_dict: bool = False,
):
    """ """
    url = f"https://api.collegefootballdata.com/live/plays?id={game_id}"

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
    return json_data
