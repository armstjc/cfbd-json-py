# Creation Date: 08/30/2023 01:13 PM EDT
# Last Updated Date: 08/13/2024 02:10 PM EDT
# Author: Joseph Armstrong (armstrongjoseph08@gmail.com)
# File Name: stats.py
# Purpose: Houses functions pertaining to CFB team/player
#    stats data within the CFBD API.
###############################################################################

import logging
from datetime import datetime

import pandas as pd
import requests
from tqdm import tqdm

from cfbd_json_py.utls import get_cfbd_api_token


def get_cfbd_team_season_stats(
    api_key: str = None,
    api_key_dir: str = None,
    season: int = None,
    team: str = None,
    # `year` and/or `team` need to be not null for this function to work.
    conference: str = None,
    start_week: int = None,
    end_week: int = None,
    return_as_dict: bool = False,
    use_original_column_names: bool = False,
):
    """
    Allows you to get CFB team season stats data from the CFBD API.

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

    `season` (int, semi-mandatory):
        Semi-required argument.
        Specifies the season you want CFB team season stats data from.
        This must be specified, otherwise this package, and by extension
        the CFBD API, will not accept
        the request to get CFB team season stats data.
        This or `team` must be set
        to a valid non-null variable for this to function.

    `team` (str, semi-mandatory):
        Semi-required argument.
        Specifies the season you want CFB team season stats data from.
        This must be specified, otherwise this package, and by extension
        the CFBD API, will not accept
        the request to get CFB team season stats data.
        This or `season` must be set
        to a valid non-null variable for this to function.

    `conference` (str, optional):
        Optional argument.
        If you only want team season stats from games
        involving teams a specific conference,
        set `conference` to the abbreviation
        of the conference you want stats from.

    `start_week` (int, semi-optional):
        Optional argument.
        If you only want team stats for a range of weeks,
        set `start_week` and `end_week` to
        the range of weeks you want season-level data for.

    `end_week` (int, semi-optional):
        Optional argument.
        If you only want team stats for a range of weeks,
        set `start_week` and `end_week` to
        the range of weeks you want season-level data for.

    **NOTE**: If the following conditions are `True`, a `ValueError()`
    will be raised when calling this function:
    - `start_week < 0`
    - `end_week < 0`
    - `start_week is not None and end_week is None`
        (will be changed in a future version)
    - `start_week is None and end_week is not None`
        (will be changed in a future version)
    - `end_week < start_week`
    - `end_week = start_week`

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

    from cfbd_json_py.stats import get_cfbd_team_season_stats


    cfbd_key = "tigersAreAwesome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwesome":
        print(
            "Using the user's API key declared in this script " +
            "for this example."
        )

        # Get team season stats for the 2020 CFB season.
        print("Get team season stats for the 2020 CFB season.")
        json_data = get_cfbd_team_season_stats(
            api_key=cfbd_key,
            season=2020
        )
        print(json_data)
        time.sleep(5)


        # Get team season stats for teams competing in
        # the Big 10 (B1G) conference the 2020 CFB season.
        print(
            "Get team season stats for teams competing in " +
            "the Big 10 (B1G) conference the 2020 CFB season."
        )
        json_data = get_cfbd_team_season_stats(
            api_key=cfbd_key,
            conference="B1G",
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get team season stats for the 2020 CFB season,
        # but only between weeks 5 and 10.
        print("Get team season stats for the 2020 CFB season.")
        json_data = get_cfbd_team_season_stats(
            api_key=cfbd_key,
            season=2020,
            start_week=5,
            end_week=10
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print(
            "You can also tell this function to just return the API call " +
            "as a Dictionary (read: JSON) object."
        )
        json_data = get_cfbd_team_season_stats(
            api_key=cfbd_key,
            season=2020,
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


        # Get team season stats for the 2020 CFB season.
        print("Get team season stats for the 2020 CFB season.")
        json_data = get_cfbd_team_season_stats(
            season=2020
        )
        print(json_data)
        time.sleep(5)


        # Get team season stats for teams competing in
        # the Big 10 (B1G) conference the 2020 CFB season.
        print(
            "Get team season stats for teams competing in " +
            "the Big 10 (B1G) conference the 2020 CFB season."
        )
        json_data = get_cfbd_team_season_stats(
            conference="B1G",
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get team season stats for the 2020 CFB season,
        # but only between weeks 5 and 10.
        print("Get team season stats for the 2020 CFB season.")
        json_data = get_cfbd_team_season_stats(
            season=2020,
            start_week=5,
            end_week=10
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print(
            "You can also tell this function to just return the API call " +
            "as a Dictionary (read: JSON) object."
        )
        json_data = get_cfbd_team_season_stats(
            season=2020,
            return_as_dict=True
        )
        print(json_data)
    ```
    Returns
    ----------
    A pandas `DataFrame` object with team season stats data,
    or (if `return_as_dict` is set to `True`)
    a dictionary object with a with team season stats data.

    """

    rebuilt_json = {}
    stat_columns = [
        "season",
        "team_name",
        "conference_name",
        "games",
        # Passing
        "passing_COMP",
        "passing_ATT",
        "passing_NET_YDS",
        "passing_TD",
        "passing_INT",
        # Rushing
        "rushing_CAR",
        "rushing_YDS",
        "rushing_TD",
        # Misc. Offense
        "total_yards",
        # Fumbles
        "fumbles_LOST",
        "fumbles_REC",
        # Defense
        "defensive_TFL",
        "defensive_SACKS",
        # Interceptions
        "interceptions_INT",
        "interceptions_YDS",
        "interceptions_TD",
        # Kick Returns
        "kickReturns_NO",
        "kickReturns_YDS",
        "kickReturns_TD",
        # Punt Returns
        "puntReturns_NO",
        "puntReturns_YDS",
        "puntReturns_TD",
        # Situational
        "situational_first_downs",
        "situational_third_down_conversions",
        "situational_third_downs_attempted",
        "situational_fourth_down_conversions",
        "situational_fourth_downs_attempted",
        "situational_penalties",
        "situational_penalty_yards",
        "situational_turnovers",
        "situational_possession_time",
    ]

    now = datetime.now()
    url = "https://api.collegefootballdata.com/stats/season"
    row_df = pd.DataFrame()
    final_df = pd.DataFrame()

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

    if start_week is not None and end_week is not None:
        if start_week > end_week:
            raise ValueError("`start_week` cannot be greater than `end_week`.")
        elif start_week == end_week:
            raise ValueError(
                "`start_week` cannot be equal to `end_week`."
                + "\n Use " +
                "`cfbd_json_py.games.get_cfbd_player_game_stats()` instead "
                + "if you want player stats for a specific week in ."
            )
        elif start_week < 0:
            raise ValueError("`start_week` cannot be less than 0.")
        elif end_week < 0:
            raise ValueError("`end_week` cannot be less than 0.")
    # URL builder
    ##########################################################################

    # Required by the API

    if season is not None and team is not None:
        url += f"?year={season}&team={team}"
    elif season is not None:
        url += f"?year={season}"
    elif team is not None:
        url += f"?team={team}"

    if conference is not None:
        url += f"&conference={conference}"

    if start_week is not None:
        url += f"&startWeek={start_week}"

    if end_week is not None:
        url += f"&endWeek={end_week}"

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

    for stat in tqdm(json_data):
        t_season = stat["season"]
        t_team_name = stat["team"]
        t_conference = stat["conference"]
        stat_name = stat["statName"]
        stat_value = stat["statValue"]
        composite_key = f"{t_season}_{t_team_name}"

        if rebuilt_json.get(composite_key) is None:
            rebuilt_json[composite_key] = {}

        match stat_name:
            # General
            case "games":
                rebuilt_json[composite_key]["season"] = t_season
                rebuilt_json[composite_key]["team_name"] = t_team_name
                rebuilt_json[composite_key]["conference_name"] = t_conference
                rebuilt_json[composite_key]["games"] = stat_value

            # Passing
            case "passCompletions":
                rebuilt_json[composite_key]["season"] = t_season
                rebuilt_json[composite_key]["team_name"] = t_team_name
                rebuilt_json[composite_key]["conference_name"] = t_conference
                rebuilt_json[composite_key]["passing_COMP"] = stat_value

            case "passAttempts":
                rebuilt_json[composite_key]["season"] = t_season
                rebuilt_json[composite_key]["team_name"] = t_team_name
                rebuilt_json[composite_key]["conference_name"] = t_conference
                rebuilt_json[composite_key]["passing_ATT"] = stat_value

            case "netPassingYards":
                rebuilt_json[composite_key]["season"] = t_season
                rebuilt_json[composite_key]["team_name"] = t_team_name
                rebuilt_json[composite_key]["conference_name"] = t_conference
                rebuilt_json[composite_key]["passing_NET_YDS"] = stat_value

            case "passingTDs":
                rebuilt_json[composite_key]["season"] = t_season
                rebuilt_json[composite_key]["team_name"] = t_team_name
                rebuilt_json[composite_key]["conference_name"] = t_conference
                rebuilt_json[composite_key]["passing_TD"] = stat_value

            case "passesIntercepted":
                rebuilt_json[composite_key]["season"] = t_season
                rebuilt_json[composite_key]["team_name"] = t_team_name
                rebuilt_json[composite_key]["conference_name"] = t_conference
                rebuilt_json[composite_key]["passing_INT"] = stat_value

            # Rushing
            case "rushingAttempts":
                rebuilt_json[composite_key]["season"] = t_season
                rebuilt_json[composite_key]["team_name"] = t_team_name
                rebuilt_json[composite_key]["conference_name"] = t_conference
                rebuilt_json[composite_key]["rushing_CAR"] = stat_value

            case "rushingYards":
                rebuilt_json[composite_key]["season"] = t_season
                rebuilt_json[composite_key]["team_name"] = t_team_name
                rebuilt_json[composite_key]["conference_name"] = t_conference
                rebuilt_json[composite_key]["rushing_YDS"] = stat_value

            case "rushingTDs":
                rebuilt_json[composite_key]["season"] = t_season
                rebuilt_json[composite_key]["team_name"] = t_team_name
                rebuilt_json[composite_key]["conference_name"] = t_conference
                rebuilt_json[composite_key]["rushing_TD"] = stat_value

            # Misc Offense
            case "totalYards":
                rebuilt_json[composite_key]["season"] = t_season
                rebuilt_json[composite_key]["team_name"] = t_team_name
                rebuilt_json[composite_key]["conference_name"] = t_conference
                rebuilt_json[composite_key]["total_yards"] = stat_value

            # Fumbles
            case "fumblesLost":
                rebuilt_json[composite_key]["season"] = t_season
                rebuilt_json[composite_key]["team_name"] = t_team_name
                rebuilt_json[composite_key]["conference_name"] = t_conference
                rebuilt_json[composite_key]["fumbles_LOST"] = stat_value

            case "fumblesRecovered":
                rebuilt_json[composite_key]["season"] = t_season
                rebuilt_json[composite_key]["team_name"] = t_team_name
                rebuilt_json[composite_key]["conference_name"] = t_conference
                rebuilt_json[composite_key]["fumbles_REC"] = stat_value

            # Defense
            case "tacklesForLoss":
                rebuilt_json[composite_key]["season"] = t_season
                rebuilt_json[composite_key]["team_name"] = t_team_name
                rebuilt_json[composite_key]["conference_name"] = t_conference
                rebuilt_json[composite_key]["defensive_TFL"] = stat_value

            case "sacks":
                rebuilt_json[composite_key]["season"] = t_season
                rebuilt_json[composite_key]["team_name"] = t_team_name
                rebuilt_json[composite_key]["conference_name"] = t_conference
                rebuilt_json[composite_key]["defensive_SACKS"] = stat_value

            # Interceptions
            case "interceptions":
                rebuilt_json[composite_key]["season"] = t_season
                rebuilt_json[composite_key]["team_name"] = t_team_name
                rebuilt_json[composite_key]["conference_name"] = t_conference
                rebuilt_json[composite_key]["interceptions_INT"] = stat_value

            case "interceptionYards":
                rebuilt_json[composite_key]["season"] = t_season
                rebuilt_json[composite_key]["team_name"] = t_team_name
                rebuilt_json[composite_key]["conference_name"] = t_conference
                rebuilt_json[composite_key]["interceptions_YDS"] = stat_value

            case "interceptionTDs":
                rebuilt_json[composite_key]["season"] = t_season
                rebuilt_json[composite_key]["team_name"] = t_team_name
                rebuilt_json[composite_key]["conference_name"] = t_conference
                rebuilt_json[composite_key]["interceptions_TD"] = stat_value

            # Kick Returns
            case "kickReturns":
                rebuilt_json[composite_key]["season"] = t_season
                rebuilt_json[composite_key]["team_name"] = t_team_name
                rebuilt_json[composite_key]["conference_name"] = t_conference
                rebuilt_json[composite_key]["kickReturns_NO"] = stat_value

            case "kickReturnYards":
                rebuilt_json[composite_key]["season"] = t_season
                rebuilt_json[composite_key]["team_name"] = t_team_name
                rebuilt_json[composite_key]["conference_name"] = t_conference
                rebuilt_json[composite_key]["kickReturns_YDS"] = stat_value

            case "kickReturnTDs":
                rebuilt_json[composite_key]["season"] = t_season
                rebuilt_json[composite_key]["team_name"] = t_team_name
                rebuilt_json[composite_key]["conference_name"] = t_conference
                rebuilt_json[composite_key]["kickReturns_TD"] = stat_value

            # Punt Returns
            case "puntReturns":
                rebuilt_json[composite_key]["season"] = t_season
                rebuilt_json[composite_key]["team_name"] = t_team_name
                rebuilt_json[composite_key]["conference_name"] = t_conference
                rebuilt_json[composite_key]["puntReturns_NO"] = stat_value

            case "puntReturnYards":
                rebuilt_json[composite_key]["season"] = t_season
                rebuilt_json[composite_key]["team_name"] = t_team_name
                rebuilt_json[composite_key]["conference_name"] = t_conference
                rebuilt_json[composite_key]["puntReturns_YDS"] = stat_value

            case "puntReturnTDs":
                rebuilt_json[composite_key]["season"] = t_season
                rebuilt_json[composite_key]["team_name"] = t_team_name
                rebuilt_json[composite_key]["conference_name"] = t_conference
                rebuilt_json[composite_key]["puntReturns_TD"] = stat_value

            # Situational
            case "firstDowns":
                rebuilt_json[composite_key]["season"] = t_season
                rebuilt_json[composite_key]["team_name"] = t_team_name
                rebuilt_json[composite_key]["conference_name"] = t_conference
                rebuilt_json[composite_key][
                    "situational_first_downs"] = stat_value

            case "turnovers":
                rebuilt_json[composite_key]["season"] = t_season
                rebuilt_json[composite_key]["team_name"] = t_team_name
                rebuilt_json[composite_key]["conference_name"] = t_conference
                rebuilt_json[composite_key][
                    "situational_turnovers"] = stat_value

            case "thirdDownConversions":
                rebuilt_json[composite_key]["season"] = t_season
                rebuilt_json[composite_key]["team_name"] = t_team_name
                rebuilt_json[composite_key]["conference_name"] = t_conference
                rebuilt_json[composite_key][
                    "situational_third_down_conversions"
                ] = stat_value

            case "thirdDowns":
                rebuilt_json[composite_key]["season"] = t_season
                rebuilt_json[composite_key]["team_name"] = t_team_name
                rebuilt_json[composite_key]["conference_name"] = t_conference
                rebuilt_json[composite_key][
                    "situational_third_downs_attempted"
                ] = stat_value

            case "fourthDownConversions":
                rebuilt_json[composite_key]["season"] = t_season
                rebuilt_json[composite_key]["team_name"] = t_team_name
                rebuilt_json[composite_key]["conference_name"] = t_conference
                rebuilt_json[composite_key][
                    "situational_fourth_down_conversions"
                ] = stat_value

            case "fourthDowns":
                rebuilt_json[composite_key]["season"] = t_season
                rebuilt_json[composite_key]["team_name"] = t_team_name
                rebuilt_json[composite_key]["conference_name"] = t_conference
                rebuilt_json[composite_key][
                    "situational_fourth_downs_attempted"
                ] = stat_value

            case "penalties":
                rebuilt_json[composite_key]["season"] = t_season
                rebuilt_json[composite_key]["team_name"] = t_team_name
                rebuilt_json[composite_key]["conference_name"] = t_conference
                rebuilt_json[composite_key][
                    "situational_penalties"] = stat_value

            case "penaltyYards":
                rebuilt_json[composite_key]["season"] = t_season
                rebuilt_json[composite_key]["team_name"] = t_team_name
                rebuilt_json[composite_key]["conference_name"] = t_conference
                rebuilt_json[composite_key][
                    "situational_penalty_yards"] = stat_value

            case "possessionTime":
                rebuilt_json[composite_key]["season"] = t_season
                rebuilt_json[composite_key]["team_name"] = t_team_name
                rebuilt_json[composite_key]["conference_name"] = t_conference
                rebuilt_json[composite_key][
                    "situational_possession_time"] = stat_value

            case _:
                raise ValueError(f"Unhandled stat name `{stat_name}`")

        del t_season, t_team_name, t_conference
        del (
            stat_name,
            stat_value,
        )
        del composite_key

    for key, value in tqdm(rebuilt_json.items()):
        row_df = pd.DataFrame(value, index=[0])
        final_df = pd.concat([final_df, row_df], ignore_index=True)
        # print()

    final_df = final_df[stat_columns]
    return final_df


def get_cfbd_advanced_team_season_stats(
    api_key: str = None,
    api_key_dir: str = None,
    season: int = None,
    team: str = None,
    # `year` and/or `team` need to be not null for this function to work.
    exclude_garbage_time: bool = False,
    start_week: int = None,
    end_week: int = None,
    return_as_dict: bool = False,
):
    """
    Allows you to get advanced CFB team season stats data from the CFBD API.

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

    `season` (int, semi-mandatory):
        Semi-required argument.
        Specifies the season you want CFB team season stats data from.
        This must be specified, otherwise this package, and by extension
        the CFBD API, will not accept the request
        to get CFB team season stats data.
        This or `team` must be set
        to a valid non-null variable for this to function.

    `team` (str, semi-mandatory):
        Semi-required argument.
        Specifies the season you want advanced CFB team season stats data from.
        This must be specified, otherwise this package, and by extension
        the CFBD API, will not accept
        the request to get CFB team season stats data.
        This or `season` must be set
        to a valid non-null variable for this to function.

    `exclude_garbage_time` (bool, optional):
        Optional argument.
        If you want to filter out plays where
        the result of the game is largely decided,
        set `exclude_garbage_time = True`.
        Default behavior is that this variable is set to
        `False` when this function is called.

    `start_week` (int, semi-optional):
        Optional argument.
        If you only want team stats for a range of weeks,
        set `start_week` and `end_week` to
        the range of weeks you want season-level data for.

    `end_week` (int, semi-optional):
        Optional argument.
        If you only want team stats for a range of weeks,
        set `start_week` and `end_week` to
        the range of weeks you want season-level data for.

    **NOTE**: If the following conditions are `True`, a `ValueError()`
    will be raised when calling this function:
    - `start_week < 0`
    - `end_week < 0`
    - `start_week is not None and end_week is None`
        (will be changed in a future version)
    - `start_week is None and end_week is not None`
        (will be changed in a future version)
    - `end_week < start_week`
    - `end_week = start_week`

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

    from cfbd_json_py.stats import get_cfbd_advanced_team_season_stats


    cfbd_key = "tigersAreAwesome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwesome":
        print(
            "Using the user's API key declared in this script " +
            "for this example."
        )

        # Get advanced team season stats for the 2020 CFB season.
        print("Get team season stats for the 2020 CFB season.")
        json_data = get_cfbd_advanced_team_season_stats(
            api_key=cfbd_key,
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get advanced team season stats for the 2020 CFB season,
        # but remove plays that happen in garbage time.
        print(
            "Get advanced team season stats for the 2020 CFB season, " +
            "but remove plays that happen in garbage time."
        )
        json_data = get_cfbd_advanced_team_season_stats(
            api_key=cfbd_key,
            season=2020,
            exclude_garbage_time=True
        )
        print(json_data)
        time.sleep(5)

        # Get advanced team season stats for the 2020 CFB season,
        # but only between weeks 5 and 10.
        print(
            "Get advanced team season stats for the 2020 CFB season, " +
            "but only between weeks 5 and 10."
        )
        json_data = get_cfbd_advanced_team_season_stats(
            api_key=cfbd_key,
            season=2020,
            start_week=5,
            end_week=10
        )
        print(json_data)
        time.sleep(5)

        # Get advanced team season stats for just
        # the Ohio State Buckeyes Football Team.
        print(
            "Get advanced team season stats for just" +
            " the Ohio State Buckeyes Football Team."
        )
        json_data = get_cfbd_advanced_team_season_stats(
            api_key=cfbd_key,
            team="Ohio State"
        )
        print(json_data)
        time.sleep(5)


        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print(
            "You can also tell this function to just return the API call " +
            "as a Dictionary (read: JSON) object."
        )
        json_data = get_cfbd_advanced_team_season_stats(
            api_key=cfbd_key,
            season=2020,
            team="Cincinnati",
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

    # Get advanced team season stats for the 2020 CFB season.
        print("Get team season stats for the 2020 CFB season.")
        json_data = get_cfbd_advanced_team_season_stats(
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get advanced team season stats for the 2020 CFB season,
        # but remove plays that happen in garbage time.
        print(
            "Get advanced team season stats for the 2020 CFB season, " +
            "but remove plays that happen in garbage time."
        )
        json_data = get_cfbd_advanced_team_season_stats(
            season=2020,
            exclude_garbage_time=True
        )
        print(json_data)
        time.sleep(5)

        # Get advanced team season stats for the 2020 CFB season,
        # but only between weeks 5 and 10.
        print(
            "Get advanced team season stats for the 2020 CFB season, " +
            "but only between weeks 5 and 10."
        )
        json_data = get_cfbd_advanced_team_season_stats(
            season=2020,
            start_week=5,
            end_week=10
        )
        print(json_data)
        time.sleep(5)

        # Get advanced team season stats for the just
        # the Ohio State Buckeyes Football Team.
        print(
            "Get advanced team season stats for the just " +
            "the Ohio State Buckeyes Football Team."
        )
        json_data = get_cfbd_advanced_team_season_stats(
            team="Ohio State"
        )
        print(json_data)
        time.sleep(5)


        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print(
            "You can also tell this function to just return the API call " +
            "as a Dictionary (read: JSON) object."
        )
        json_data = get_cfbd_advanced_team_season_stats(
            season=2020,
            team="Cincinnati",
            return_as_dict=True
        )
        print(json_data)
    ```
    Returns
    ----------
    A pandas `DataFrame` object with advanced team season stats data,
    or (if `return_as_dict` is set to `True`)
    a dictionary object with a with advanced team season stats data.

    """
    now = datetime.now()
    url = "https://api.collegefootballdata.com/stats/season/advanced"
    row_df = pd.DataFrame()
    final_df = pd.DataFrame()

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

    if start_week is not None and end_week is not None:
        if start_week > end_week:
            raise ValueError("`start_week` cannot be greater than `end_week`.")
        elif start_week == end_week:
            raise ValueError(
                "`start_week` cannot be equal to `end_week`."
                + "\n Use " +
                "`cfbd_json_py.games.get_cfbd_player_game_stats()` instead "
                + "if you want player stats for a specific week in ."
            )
        elif start_week < 0:
            raise ValueError("`start_week` cannot be less than 0.")
        elif end_week < 0:
            raise ValueError("`end_week` cannot be less than 0.")

    gt_str = ""

    # URL builder
    ##########################################################################

    if exclude_garbage_time is True:
        gt_str = "true"
    elif exclude_garbage_time is False:
        gt_str = "false"

    if season is not None and team is not None:
        url += f"?year={season}&team={team}"
    elif season is not None:
        url += f"?year={season}"
    elif team is not None:
        url += f"?team={team}"

    if exclude_garbage_time is not None:
        url += f"&excludeGarbageTime={gt_str}"

    if start_week is not None:
        url += f"&startWeek={start_week}"

    if end_week is not None:
        url += f"&endWeek={end_week}"

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

    # final_df = pd.json_normalize(json_data)

    # print(final_df.columns)

    for team in tqdm(json_data):
        t_season = team["season"]
        t_team = team["team"]
        t_conf = team["conference"]
        row_df = pd.DataFrame(
            {
                "season": t_season,
                "team": t_team,
                "conference": t_conf
            },
            index=[0]
        )

        # offense
        if "offense" not in team:
            logging.debug(
                f"Key `[offense]` not found for the {t_season} {t_team}."
            )
        else:
            row_df["offense_plays"] = team["offense"]["plays"]
            row_df["offense_drives"] = team["offense"]["drives"]
            # row_df["offense_plays"] = team["offense"]["plays"]
            row_df["offense_ppa"] = team["offense"]["ppa"]
            row_df["offense_total_ppa"] = team["offense"]["totalPPA"]
            row_df["offense_success_rate"] = team["offense"]["successRate"]
            row_df["offense_explosiveness"] = team["offense"]["explosiveness"]
            row_df["offense_power_success"] = team["offense"]["powerSuccess"]
            row_df["offense_stuff_rate"] = team["offense"]["stuffRate"]
            row_df["offense_line_yards_avg"] = team["offense"]["lineYards"]
            row_df["offense_line_yards_total"] = team["offense"][
                "lineYardsTotal"
            ]
            row_df["offense_second_level_yards_avg"] = team["offense"][
                "secondLevelYards"
            ]
            row_df["offense_second_level_yards_total"] = team["offense"][
                "secondLevelYardsTotal"
            ]
            row_df["offense_open_field_yards_avg"] = team["offense"][
                "openFieldYards"
            ]
            row_df["offense_open_field_yards_total"] = team["offense"][
                "secondLevelYardsTotal"
            ]
            row_df["offense_total_opportunities"] = team["offense"][
                "totalOpportunies"
            ]
            row_df["offense_points_per_opportunity"] = team["offense"][
                "pointsPerOpportunity"
            ]

            row_df["offense_field_position_avg_start"] = team["offense"][
                "fieldPosition"]["averageStart"]
            row_df["offense_field_position_avg_predicted_points"] = team[
                "offense"]["fieldPosition"]["averagePredictedPoints"]

            row_df["offense_havoc_total"] = team["offense"]["havoc"]["total"]
            row_df["offense_havoc_front_7"] = team["offense"]["havoc"][
                "frontSeven"
            ]
            row_df["offense_havoc_db"] = team["offense"]["havoc"]["db"]

            row_df["offense_standard_downs_rate"] = team[
                "offense"]["standardDowns"]["rate"]
            row_df["offense_standard_downs_ppa"] = team[
                "offense"]["standardDowns"]["ppa"]
            row_df["offense_standard_downs_success_rate"] = team["offense"][
                "standardDowns"
            ]["successRate"]
            row_df["offense_standard_downs_explosiveness"] = team["offense"][
                "standardDowns"
            ]["explosiveness"]

            row_df["offense_passing_downs_rate"] = team[
                "offense"]["passingDowns"]["rate"]
            row_df["offense_passing_downs_ppa"] = team[
                "offense"]["passingDowns"]["ppa"]
            row_df["offense_passing_downs_success_rate"] = team["offense"][
                "passingDowns"
            ]["successRate"]
            row_df["offense_passing_downs_explosiveness"] = team["offense"][
                "passingDowns"
            ]["explosiveness"]

            row_df["offense_rushing_plays_rate"] = team[
                "offense"]["rushingPlays"]["rate"]
            row_df["offense_rushing_plays_ppa"] = team[
                "offense"]["rushingPlays"]["ppa"]
            row_df["offense_rushing_plays_total_ppa"] = team[
                "offense"]["rushingPlays"]["totalPPA"]
            row_df["offense_rushing_plays_success_rate"] = team[
                "offense"]["rushingPlays"]["successRate"]
            row_df["offense_rushing_plays_explosiveness"] = team[
                "offense"]["rushingPlays"]["explosiveness"]

            row_df["offense_passing_plays_rate"] = team[
                "offense"]["passingPlays"]["rate"]
            row_df["offense_passing_plays_ppa"] = team[
                "offense"]["passingPlays"]["ppa"]
            row_df["offense_passing_plays_total_ppa"] = team[
                "offense"]["passingPlays"]["totalPPA"]
            row_df["offense_passing_plays_success_rate"] = team[
                "offense"]["passingPlays"]["successRate"]
            row_df["offense_passing_plays_explosiveness"] = team[
                "offense"]["rushingPlays"]["explosiveness"]

        # defense
        if "defense" not in team:
            logging.debug(
                f"Key `[defense]` not found for the {t_season} {t_team}."
            )
        else:

            row_df["defense_plays"] = team["defense"]["plays"]
            row_df["defense_drives"] = team["defense"]["drives"]
            # row_df["defense_plays"] = team["defense"]["plays"]
            row_df["defense_ppa"] = team["defense"]["ppa"]
            row_df["defense_total_ppa"] = team["defense"]["totalPPA"]
            row_df["defense_success_rate"] = team["defense"]["successRate"]
            row_df["defense_explosiveness"] = team["defense"]["explosiveness"]
            row_df["defense_power_success"] = team["defense"]["powerSuccess"]
            row_df["defense_stuff_rate"] = team["defense"]["stuffRate"]
            row_df["defense_line_yards_avg"] = team["defense"]["lineYards"]
            row_df["defense_line_yards_total"] = team["defense"][
                "lineYardsTotal"
            ]
            row_df["defense_second_level_yards_avg"] = team["defense"][
                "secondLevelYards"
            ]
            row_df["defense_second_level_yards_total"] = team["defense"][
                "secondLevelYardsTotal"
            ]
            row_df["defense_open_field_yards_avg"] = team["defense"][
                "openFieldYards"
            ]
            row_df["defense_open_field_yards_total"] = team["defense"][
                "secondLevelYardsTotal"
            ]
            row_df["defense_total_opportunities"] = team["defense"][
                "totalOpportunies"
            ]
            row_df["defense_points_per_opportunity"] = team["defense"][
                "pointsPerOpportunity"
            ]

            row_df["defense_field_position_avg_start"] = team["defense"][
                "fieldPosition"
            ]["averageStart"]
            row_df["defense_field_position_avg_predicted_points"] = team[
                "defense"]["fieldPosition"]["averagePredictedPoints"]

            row_df["defense_havoc_total"] = team["defense"]["havoc"]["total"]
            row_df["defense_havoc_front_7"] = team["defense"]["havoc"][
                "frontSeven"
            ]
            row_df["defense_havoc_db"] = team["defense"]["havoc"]["db"]

            row_df["defense_standard_downs_rate"] = team[
                "defense"]["standardDowns"]["rate"]
            row_df["defense_standard_downs_ppa"] = team[
                "defense"]["standardDowns"]["ppa"]
            row_df["defense_standard_downs_success_rate"] = team["defense"][
                "standardDowns"
            ]["successRate"]
            row_df["defense_standard_downs_explosiveness"] = team["defense"][
                "standardDowns"
            ]["explosiveness"]

            row_df["defense_passing_downs_rate"] = team[
                "defense"]["passingDowns"]["rate"]
            row_df["defense_passing_downs_ppa"] = team[
                "defense"]["passingDowns"]["ppa"]
            row_df["defense_passing_downs_success_rate"] = team["defense"][
                "passingDowns"
            ]["successRate"]
            row_df["defense_passing_downs_explosiveness"] = team["defense"][
                "passingDowns"
            ]["explosiveness"]

            row_df["defense_rushing_plays_rate"] = team[
                "defense"]["rushingPlays"]["rate"]
            row_df["defense_rushing_plays_ppa"] = team[
                "defense"]["rushingPlays"]["ppa"]
            row_df["defense_rushing_plays_total_ppa"] = team[
                "defense"]["rushingPlays"]["totalPPA"]
            row_df["defense_rushing_plays_success_rate"] = team["defense"][
                "rushingPlays"
            ]["successRate"]
            row_df["defense_rushing_plays_explosiveness"] = team["defense"][
                "rushingPlays"
            ]["explosiveness"]

            row_df["defense_passing_plays_rate"] = team[
                "defense"]["passingPlays"]["rate"]
            row_df["defense_passing_plays_ppa"] = team[
                "defense"]["passingPlays"]["ppa"]
            row_df["defense_passing_plays_total_ppa"] = team[
                "defense"]["passingPlays"]["totalPPA"]
            row_df["defense_passing_plays_success_rate"] = team["defense"][
                "passingPlays"
            ]["successRate"]
            row_df["defense_passing_plays_explosiveness"] = team["defense"][
                "rushingPlays"
            ]["explosiveness"]

        final_df = pd.concat([final_df, row_df], ignore_index=True)
        del row_df
        del t_season, t_conf, t_team

    return final_df


def get_cfbd_advanced_team_game_stats(
    api_key: str = None,
    api_key_dir: str = None,
    season: int = None,
    team: str = None,
    # `year` and/or `team` need to be not null for this function to work.
    week: int = None,
    opponent: str = None,
    exclude_garbage_time: bool = False,
    season_type: str = "both",  # "regular", "postseason", or "both"
    return_as_dict: bool = False,
):
    """
    Allows you to get advanced CFB team game stats data from the CFBD API.

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

    `season` (int, semi-mandatory):
        Semi-required argument.
        Specifies the season you want CFB team game stats data from.
        This must be specified, otherwise this package, and by extension
        the CFBD API, will not accept the request
        to get CFB team season stats data.
        This or `team` must be set
        to a valid non-null variable for this to function.

    `team` (str, semi-mandatory):
        Semi-required argument.
        Specifies the season you want advanced CFB team game stats data from.
        This must be specified, otherwise this package, and by extension
        the CFBD API, will not accept
        the request to get CFB team season stats data.
        This or `season` must be set
        to a valid non-null variable for this to function.

    `week` (int, optional):
        Optional argument.
        If `week` is set to an integer, this function will attempt
        to load CFB team game from games in that season, and that week.

    `opponent` (str, optional):
        Optional argument.
        If you only want games from a specific opponent,
        set `opponent` to the name of that team.


    `exclude_garbage_time` (bool, optional):
        Optional argument.
        If you want to filter out plays where
        the result of the game is largely decided,
        set `exclude_garbage_time = True`.
        Default behavior is that this variable is set to
        `False` when this function is called.

    `season_type` (str, semi-optional):
        Semi-optional argument.
        By default, this will be set to "regular", for the CFB regular season.
        If you want CFB team game stats, set `season_type` to "postseason".
        If `season_type` is set to anything but "regular" or "postseason",
        a `ValueError()` will be raised.

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

    from cfbd_json_py.stats import get_cfbd_advanced_team_game_stats


    cfbd_key = "tigersAreAwesome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwesome":
        print(
            "Using the user's API key declared in this script " +
            "for this example."
        )

        # Get advanced CFBD team game stats for week 10 of the 2020 CFB season.
        print("Get advanced CFBD team game stats for the 2020 CFB season.")
        json_data = get_cfbd_advanced_team_game_stats(
            api_key=cfbd_key,
            season=2020,
            week=10
        )
        print(json_data)
        time.sleep(5)

        # Get advanced CFBD team game stats for week 10 of the 2020 CFB season,
        # but exclude plays that happen in garbage time.
        print("Get advanced CFBD team game stats for the 2020 CFB season.")
        json_data = get_cfbd_advanced_team_game_stats(
            api_key=cfbd_key,
            season=2020,
            week=10,
            exclude_garbage_time=True
        )
        print(json_data)
        time.sleep(5)

        # Get advanced CFBD team game stats for the 2020 CFB season.
        print("Get advanced CFBD team game stats for the 2020 CFB season.")
        json_data = get_cfbd_advanced_team_game_stats(
            api_key=cfbd_key,
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get advanced CFBD team game stats for
        # the University of Cincinnati Football Team in the 2020 CFB season.
        print(
            "Get advanced CFBD team game stats for " +
            "the University of Cincinnati Football Team " +
            "in the 2020 CFB season."
        )
        json_data = get_cfbd_advanced_team_game_stats(
            api_key=cfbd_key,
            season=2020,
            opponent="Ohio"
        )
        print(json_data)
        time.sleep(5)

        # Get advanced CFBD team game stats for teams that faced off
        # against the Ohio Bobcats Football Team in the 2020 CFB season.
        print(
            "Get advanced CFBD team game stats for teams that " +
            "faced off against the Ohio Bobcats Football Team " +
            "in the 2020 CFB season."
        )
        json_data = get_cfbd_advanced_team_game_stats(
            api_key=cfbd_key,
            season=2020,
            opponent="Ohio"
        )
        print(json_data)
        time.sleep(5)

        # Get advanced CFBD team game stats for just
        # postseason games in the 2020 CFB season.
        print(
            "Get advanced CFBD team game stats for just postseason games " +
            "in the 2020 CFB season."
        )
        json_data = get_cfbd_advanced_team_game_stats(
            api_key=cfbd_key,
            season=2020,
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
        json_data = get_cfbd_advanced_team_game_stats(
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

        # Get advanced CFBD team game stats for week 10 of the 2020 CFB season.
        print("Get advanced CFBD team game stats for the 2020 CFB season.")
        json_data = get_cfbd_advanced_team_game_stats(
            season=2020,
            week=10
        )
        print(json_data)
        time.sleep(5)

        # Get advanced CFBD team game stats for week 10 of the 2020 CFB season,
        # but exclude plays that happen in garbage time.
        print("Get advanced CFBD team game stats for the 2020 CFB season.")
        json_data = get_cfbd_advanced_team_game_stats(
            season=2020,
            week=10,
            exclude_garbage_time=True
        )
        print(json_data)
        time.sleep(5)

        # Get advanced CFBD team game stats for the 2020 CFB season.
        print("Get advanced CFBD team game stats for the 2020 CFB season.")
        json_data = get_cfbd_advanced_team_game_stats(
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get advanced CFBD team game stats for
        # the University of Cincinnati Football Team in the 2020 CFB season.
        print(
            "Get advanced CFBD team game stats for " +
            "the University of Cincinnati Football Team " +
            "in the 2020 CFB season."
        )
        json_data = get_cfbd_advanced_team_game_stats(
            season=2020,
            opponent="Ohio"
        )
        print(json_data)
        time.sleep(5)

        # Get advanced CFBD team game stats for teams that faced off
        # against the Ohio Bobcats Football Team in the 2020 CFB season.
        print(
            "Get advanced CFBD team game stats for teams that " +
            "faced off against the Ohio Bobcats Football Team " +
            "in the 2020 CFB season."
        )
        json_data = get_cfbd_advanced_team_game_stats(
            season=2020,
            opponent="Ohio"
        )
        print(json_data)
        time.sleep(5)

        # Get advanced CFBD team game stats for just
        # postseason games in the 2020 CFB season.
        print(
            "Get advanced CFBD team game stats for just postseason games " +
            "in the 2020 CFB season."
        )
        json_data = get_cfbd_advanced_team_game_stats(
            season=2020,
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
        json_data = get_cfbd_advanced_team_game_stats(
            season=2020,
            week=10,
            return_as_dict=True
        )
        print(json_data)

    ```
    Returns
    ----------
    A pandas `DataFrame` object with advanced team season stats data,
    or (if `return_as_dict` is set to `True`)
    a dictionary object with a with advanced team season stats data.
    """
    now = datetime.now()
    url = "https://api.collegefootballdata.com/stats/game/advanced"
    row_df = pd.DataFrame()
    final_df = pd.DataFrame()

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

    if season_type == "regular" or season_type == "postseason" \
            or season_type == "both":
        pass
    else:
        raise ValueError(
            '`season_type` must be set to either ' +
            '"regular","postseason", or "both".'
        )

    gt_str = ""

    # URL builder
    ##########################################################################

    if exclude_garbage_time is True:
        gt_str = "true"
    elif exclude_garbage_time is False:
        gt_str = "false"

    if season is not None and team is not None:
        url += f"?year={season}&team={team}"
    elif season is not None:
        url += f"?year={season}"
    elif team is not None:
        url += f"?team={team}"

    if exclude_garbage_time is not None:
        url += f"&excludeGarbageTime={gt_str}"

    if week is not None:
        url += f"&week={week}"

    if opponent is not None:
        url += f"&opponent={opponent}"

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

    for team in tqdm(json_data):
        t_game_id = team["gameId"]
        t_week = team["week"]
        t_team = team["team"]
        t_opponent = team["opponent"]

        if season is not None:
            row_df = pd.DataFrame(
                {
                    "season": season,
                    "game_id": t_game_id,
                    "week": t_week,
                    "team_name": t_team,
                    "opponent_name": t_opponent,
                },
                index=[0],
            )
        else:

            row_df = pd.DataFrame(
                {
                    "game_id": t_game_id,
                    "week": t_week,
                    "team_name": t_team,
                    "opponent_name": t_opponent,
                },
                index=[0],
            )

        # offense
        if "offense" not in team:
            logging.debug(
                "Key `[offense]` not found for " +
                f"Game ID #{t_game_id} and {t_team}, "
                + f"which happened in week {t_week}."
            )
        else:
            row_df["offense_plays"] = team["offense"]["plays"]
            row_df["offense_drives"] = team["offense"]["drives"]
            row_df["offense_ppa"] = team["offense"]["ppa"]
            row_df["offense_total_ppa"] = team["offense"]["totalPPA"]
            row_df["offense_success_rate"] = team["offense"]["successRate"]
            row_df["offense_explosiveness"] = team["offense"]["explosiveness"]
            row_df["offense_power_success"] = team["offense"]["powerSuccess"]
            row_df["offense_stuff_rate"] = team["offense"]["stuffRate"]
            row_df["offense_line_yards_avg"] = team["offense"]["lineYards"]
            row_df["offense_line_yards_total"] = team["offense"][
                "lineYardsTotal"
            ]
            row_df["offense_second_level_yards_avg"] = team["offense"][
                "secondLevelYards"
            ]
            row_df["offense_second_level_yards_total"] = team["offense"][
                "secondLevelYardsTotal"
            ]
            row_df["offense_open_field_yards_avg"] = team["offense"][
                "openFieldYards"
            ]
            row_df["offense_open_field_yards_total"] = team["offense"][
                "secondLevelYardsTotal"
            ]

            row_df["offense_standard_downs_ppa"] = team[
                "offense"]["standardDowns"]["ppa"]
            row_df["offense_standard_downs_success_rate"] = team[
                "offense"]["standardDowns"]["successRate"]
            row_df["offense_standard_downs_explosiveness"] = team["offense"][
                "standardDowns"
            ]["explosiveness"]

            row_df["offense_passing_downs_ppa"] = team[
                "offense"]["passingDowns"]["ppa"]
            row_df["offense_passing_downs_success_rate"] = team[
                "offense"]["passingDowns"]["successRate"]
            row_df["offense_passing_downs_explosiveness"] = team["offense"][
                "passingDowns"
            ]["explosiveness"]

            row_df["offense_rushing_plays_ppa"] = team[
                "offense"]["rushingPlays"]["ppa"]
            row_df["offense_rushing_plays_total_ppa"] = team[
                "offense"]["rushingPlays"]["totalPPA"]
            row_df["offense_rushing_plays_success_rate"] = team[
                "offense"]["rushingPlays"]["successRate"]
            row_df["offense_rushing_plays_explosiveness"] = team[
                "offense"]["rushingPlays"]["explosiveness"]

            row_df["offense_passing_plays_ppa"] = team[
                "offense"]["passingPlays"]["ppa"]
            row_df["offense_passing_plays_total_ppa"] = team[
                "offense"]["passingPlays"]["totalPPA"]
            row_df["offense_passing_plays_success_rate"] = team[
                "offense"]["passingPlays"]["successRate"]
            row_df["offense_passing_plays_explosiveness"] = team[
                "offense"]["rushingPlays"]["explosiveness"]

        # defense
        if "defense" not in team:
            logging.debug(
                "Key `[defense]` not found for " +
                f"Game ID #{t_game_id} and {t_team}, "
                + f"which happened in week {t_week}."
            )
        else:
            row_df["defense_plays"] = team["defense"]["plays"]
            row_df["defense_drives"] = team["defense"]["drives"]
            row_df["defense_ppa"] = team["defense"]["ppa"]
            row_df["defense_total_ppa"] = team["defense"]["totalPPA"]
            row_df["defense_success_rate"] = team["defense"]["successRate"]
            row_df["defense_explosiveness"] = team["defense"]["explosiveness"]
            row_df["defense_power_success"] = team["defense"]["powerSuccess"]
            row_df["defense_stuff_rate"] = team["defense"]["stuffRate"]
            row_df["defense_line_yards_avg"] = team["defense"]["lineYards"]
            row_df["defense_line_yards_total"] = team["defense"][
                "lineYardsTotal"
            ]
            row_df["defense_second_level_yards_avg"] = team["defense"][
                "secondLevelYards"
            ]
            row_df["defense_second_level_yards_total"] = team["defense"][
                "secondLevelYardsTotal"
            ]
            row_df["defense_open_field_yards_avg"] = team["defense"][
                "openFieldYards"
            ]
            row_df["defense_open_field_yards_total"] = team["defense"][
                "secondLevelYardsTotal"
            ]
            row_df["defense_total_opportunities"] = team["defense"][
                "totalOpportunies"
            ]
            row_df["defense_points_per_opportunity"] = team["defense"][
                "pointsPerOpportunity"
            ]

            row_df["defense_standard_downs_ppa"] = team[
                "defense"]["standardDowns"]["ppa"]
            row_df["defense_standard_downs_success_rate"] = team["defense"][
                "standardDowns"
            ]["successRate"]
            row_df["defense_standard_downs_explosiveness"] = team["defense"][
                "standardDowns"
            ]["explosiveness"]

            row_df["defense_passing_downs_ppa"] = team[
                "defense"]["passingDowns"]["ppa"]
            row_df["defense_passing_downs_success_rate"] = team["defense"][
                "passingDowns"
            ]["successRate"]
            row_df["defense_passing_downs_explosiveness"] = team["defense"][
                "passingDowns"
            ]["explosiveness"]

            row_df["defense_rushing_plays_ppa"] = team[
                "defense"]["rushingPlays"]["ppa"]
            row_df["defense_rushing_plays_total_ppa"] = team[
                "defense"]["rushingPlays"]["totalPPA"]
            row_df["defense_rushing_plays_success_rate"] = team["defense"][
                "rushingPlays"
            ]["successRate"]
            row_df["defense_rushing_plays_explosiveness"] = team["defense"][
                "rushingPlays"
            ]["explosiveness"]

            row_df["defense_passing_plays_ppa"] = team[
                "defense"]["passingPlays"]["ppa"]
            row_df["defense_passing_plays_total_ppa"] = team[
                "defense"]["passingPlays"]["totalPPA"]
            row_df["defense_passing_plays_success_rate"] = team["defense"][
                "passingPlays"
            ]["successRate"]
            row_df["defense_passing_plays_explosiveness"] = team["defense"][
                "rushingPlays"
            ]["explosiveness"]

        final_df = pd.concat([final_df, row_df], ignore_index=True)
        del row_df
        del t_game_id, t_week, t_team, t_opponent

    return final_df


def get_cfbd_team_stat_categories(
    api_key: str = None, api_key_dir: str = None, return_as_dict: bool = False
):
    """
    Returns a list of stat categories
    for team stats directly from the CFBD API.

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

    from cfbd_json_py.stats import get_cfbd_team_stat_categories


    cfbd_key = "tigersAreAwesome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwesome":
        print(
            "Using the user's API key declared in this script " +
            "for this example."
        )

        # Get a list of CFBD stat categories for team stats.
        print("Get a list of CFBD stat categories for team stats.")
        json_data = get_cfbd_team_stat_categories(
            api_key=cfbd_key
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print(
            "You can also tell this function to just return the API call " +
            "as a Dictionary (read: JSON) object."
        )
        json_data = get_cfbd_team_stat_categories(
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

        # Get a list of CFBD stat categories for team stats.
        print("Get a list of CFBD stat categories for team stats.")
        json_data = get_cfbd_team_stat_categories()
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print(
            "You can also tell this function to just return the API call " +
            "as a Dictionary (read: JSON) object."
        )
        json_data = get_cfbd_team_stat_categories(
            return_as_dict=True
        )
        print(json_data)

    ```
    Returns
    ----------
    A pandas `DataFrame` object with CFBD stat categories,
    or (if `return_as_dict` is set to `True`)
    a dictionary object with CFBD stat categories.

    """
    url = "https://api.collegefootballdata.com/stats/categories"

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

    return pd.DataFrame(json_data, columns=["stat_category"])
