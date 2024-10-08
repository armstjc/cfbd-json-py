# Creation Date: 08/30/2023 01:13 EDT
# Last Updated Date: 09/16/2024 06:10 PM EDT
# Author: Joseph Armstrong (armstrongjoseph08@gmail.com)
# File Name: games.py
# Purpose: Houses functions pertaining to CFB game data within the CFBD API.
###############################################################################

import logging
from datetime import datetime

import numpy as np
import pandas as pd
import requests
from tqdm import tqdm

from cfbd_json_py.utls import get_cfbd_api_token


def get_cfbd_games(
    api_key: str = None,
    api_key_dir: str = None,
    season: int = None,
    season_type: str = "regular",
    week: int = None,
    team: str = None,
    home_team: str = None,
    away_team: str = None,
    conference: str = None,
    ncaa_division: str = "fbs",
    game_id: int = None,
    return_as_dict: bool = False,
):
    """
    Retrieves game schedule data from the CFBD API.

    Parameters
    ----------
    `season` (int, mandatory):
        Required argument.
        Specifies the season you want CFB game information from.
        This must be specified, otherwise this package, and by extension
        the CFBD API, will not accept the request to get CFB game information.

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

    `season_type` (str, semi-optional):
        Semi-optional argument.
        By default, this will be set to "regular", for the CFB regular season.
        If you want CFB game information for non-regular season games,
        set `season_type` to "postseason".
        If `season_type` is set to anything but "regular" or "postseason",
        a `ValueError()` will be raised.

    `week` (int, optional):
        Optional argument.
        If `week` is set to an integer, this function will attempt
        to load CFB game data from games in that season, and in that week.

    `team` (str, optional):
        Optional argument.
        If you only want CFB game information for a team,
        regardless if they are the home/away team,
        set `team` to the name of the team you want CFB game information from.

    `home_team` (str, optional):
        Optional argument.
        If you only want game information for a team,
        where that team was the home team in this season,
        set `home_team` to the name of the team you want game information for.

    `away_team` (str, optional):
        Optional argument.
        If you only want game information for a team,
        where that team was the away team in this season,
        set `away_team` to the name of the team you want game information for.

    `conference` (str, optional):
        Optional argument.
        If you only want game information from games
        involving teams a specific conference,
        set `conference` to the abbreviation
        of the conference you want game information from.

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

    `game_id` (int, optional):
        Optional argument.
        If `game_id` is set to a game ID,
        `get_cfb_betting_lines()` will try to get
        game information just for that game ID.

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

    from cfbd_json_py.games import get_cfbd_games


    cfbd_key = "tigersAreAwesome"  # placeholder for your CFBD API Key.

    if cfbd_key is not "tigersAreAwesome":
        print(
            "Using the user's API key declared in this script " +
            "for this example."
        )

        # Get CFB games from the 2020 CFB season.
        print("Get CFB games from the 2020 CFB season.")
        json_data = get_cfbd_games(
            api_key=cfbd_key,
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get CFB games from week 10 of the 2020 CFB season.
        print("Get CFB games from week 10 of the 2020 CFB season.")
        json_data = get_cfbd_games(
            api_key=cfbd_key,
            season=2020,
            week=10
        )
        print(json_data)
        time.sleep(5)

        # Get CFB games from the 2019 CFB season
        # that involved the 2019 LSU Tigers.
        print(
            "Get CFB games from the 2019 CFB season " +
            "that involved the 2019 LSU Tigers."
        )
        json_data = get_cfbd_games(
            api_key=cfbd_key,
            season=2019,
            team="LSU"
        )
        print(json_data)
        time.sleep(5)

        # Get 2021 Cincinnati Bearcats Football games
        # where the Bearcats were the home team.
        print(
            "Get 2021 Cincinnati Bearcats Football games " +
            "where the Bearcats were the home team."
        )
        json_data = get_cfbd_games(
            api_key=cfbd_key,
            season=2021,
            home_team="Cincinnati"
        )
        print(json_data)
        time.sleep(5)

        # Get 2018 Ohio Bobcats Football games
        # where the Bobcats were the away team.
        print(
            "Get 2018 Ohio Bobcats Football games " +
            "where the Bobcats were the away team."
        )
        json_data = get_cfbd_games(
            api_key=cfbd_key,
            season=2019,
            away_team="Ohio"
        )
        print(json_data)
        time.sleep(5)

        # Get 2022 college football games where one or more teams competing
        # was a Football Championship Subdivision team.
        print(
            "Get 2022 college football games where one or more " +
            "teams competing was a Football Championship Subdivision team."
        )
        json_data = get_cfbd_games(
            api_key=cfbd_key,
            season=2018,
            away_team="Ohio"
        )
        print(json_data)
        time.sleep(5)

        # Get game information for the
        # 2021 American Athletic conference (AAC) Championship Game.
        print(
            "Get game information for " +
            "the 2021 American Athletic conference (AAC) Championship Game."
        )
        json_data = get_cfbd_games(
            api_key=cfbd_key,
            season=2018,
            game_id=401331162
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print(
            "You can also tell this function to just return the API call " +
            "as a Dictionary (read: JSON) object."
        )
        json_data = get_cfbd_games(
            season=2020,
            week=10,
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

        # Get CFB games from the 2020 CFB season.
        print("Get CFB games from the 2020 CFB season.")
        json_data = get_cfbd_games(
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get CFB games from week 10 of the 2020 CFB season.
        print("Get CFB games from week 10 of the 2020 CFB season.")
        json_data = get_cfbd_games(
            season=2020,
            week=10
        )
        print(json_data)
        time.sleep(5)

        # Get CFB games from the 2019 CFB season
        # that involved the 2019 LSU Tigers.
        print(
            "Get CFB games from the 2019 CFB season " +
            "that involved the 2019 LSU Tigers."
        )
        json_data = get_cfbd_games(
            season=2019,
            team="LSU"
        )
        print(json_data)
        time.sleep(5)

        # Get 2021 Cincinnati Bearcats Football games
        # where the Bearcats were the home team.
        print(
            "Get 2021 Cincinnati Bearcats Football games " +
            "where the Bearcats were the home team."
        )
        json_data = get_cfbd_games(
            season=2021,
            home_team="Cincinnati"
        )
        print(json_data)
        time.sleep(5)

        # Get 2018 Ohio Bobcats Football games
        # where the Bobcats were the away team.
        print(
            "Get 2018 Ohio Bobcats Football games " +
            "where the Bobcats were the away team."
        )
        json_data = get_cfbd_games(
            season=2019,
            away_team="Ohio"
        )
        print(json_data)
        time.sleep(5)

        # Get 2018 Ohio Bobcats Football games
        # where the Bobcats were the away team.
        print(
            "Get 2018 Ohio Bobcats Football games " +
            "where the Bobcats were the away team."
        )
        json_data = get_cfbd_games(
            season=2018,
            away_team="Ohio"
        )
        print(json_data)
        time.sleep(5)

        # Get 2022 college football games where one or more teams competing
        # was a Football Championship Subdivision team.
        print(
            "Get 2022 college football games where one or more " +
            "teams competing was a Football Championship Subdivision team."
        )
        json_data = get_cfbd_games(
            season=2018,
            away_team="Ohio"
        )
        print(json_data)
        time.sleep(5)

        # Get game information for the
        # 2021 American Athletic conference (AAC) Championship Game.
        print(
            "Get game information for " +
            "the 2021 American Athletic conference (AAC) Championship Game."
        )
        json_data = get_cfbd_games(
            season=2018,
            game_id=401331162
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print(
            "You can also tell this function to just return the API call " +
            "as a Dictionary (read: JSON) object."
        )
        json_data = get_cfbd_games(
            season=2020,
            week=10,
            return_as_dict=True
        )
        print(json_data)

    ```
    Returns
    ----------
    A pandas `DataFrame` object with college football game information,
    or (if `return_as_dict` is set to `True`)
    a dictionary object with college football game information.
    """

    now = datetime.now()
    cfb_games_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/games"

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
            "`season_type` must be set to either "
            + '"regular" or "postseason" for this function to work.'
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
            + f"\n\nYou entered: \n{ncaa_division}"
        )

    # URL builder
    ##########################################################################

    # Required by API
    url += f"?seasonType={season_type}"

    if game_id is not None:
        url += f"&year={season}"
        url += f"&id={game_id}"

        if (
            team is not None
            or home_team is not None
            or away_team is not None
            or conference is not None
            or week is not None
        ):
            logging.warning(
                "When calling `cfbd_json_py.games.get_cfbd_games()`, "
                + "and setting `game_id` to a non-null value, "
                + "only `season` and `game_id` are considered "
                + "when calling the CFBD API."
            )

    else:
        url += f"&year={season}"

        # Optional for the API
        if week is not None:
            url += f"&week={week}"

        if team is not None:
            url += f"&team={team}"

        if home_team is not None:
            url += f"&home={home_team}"

        if away_team is not None:
            url += f"&away={away_team}"

        if conference is not None:
            url += f"&conference={conference}"

        if ncaa_division is not None:
            url += f"&division={ncaa_division}"

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

    cfb_games_df = pd.json_normalize(json_data)
    # print(cfb_games_df.columns)
    if len(cfb_games_df) == 0:
        logging.error(
            "The CFBD API accepted your inputs, "
            + "but found no data within your specified input parameters."
            + " Please double check your input parameters."
        )

    return cfb_games_df


def get_cfbd_team_records(
    api_key: str = None,
    api_key_dir: str = None,
    season: int = None,
    team: str = None,  # Must specify either a year or team
    conference: str = None,
    return_as_dict: bool = False,
):
    """
    Get a team, or multiple team's record (wins, losses, ties)
    for home games, away games,
    conference games, and the team's record for that season.

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
        Specifies the season you want CFB team records data from.
        You MUST set `season` or `team` to a non-null value for
        this function to work. If you don't, a `ValueError()`
        will be raised.

    `team` (str, optional):
        Semi-optional argument.
        If you only want CFB team records data for a specific team,
        set `team` to the name of the team you want CFB drive data from.
        You MUST set `season` or `team` to a non-null value for
        this function to work. If you don't, a `ValueError()`
        will be raised.

    `conference` (str, optional):
        Optional argument.
        If you only want CFB team records data from games
        involving teams from a specific conference,
        set `conference` to the abbreviation
        of the conference you want CFB team records data from.
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

    from cfbd_json_py.games import get_cfbd_team_records


    cfbd_key = "tigersAreAwesome"  # placeholder for your CFBD API Key.

    if cfbd_key is not "tigersAreAwesome":
        print(
            "Using the user's API key declared in this script " +
            "for this example."
        )

        # Get CFB team records from the 2020 CFB season.
        print("Get CFB team records from the 2020 CFB season.")
        json_data = get_cfbd_team_records(
            api_key=cfbd_key,
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get team records from football teams
        # fielded by the University of Cincinnati.
        print(
            "Get team records from football teams fielded " +
            "by the University of Cincinnati."
        )
        json_data = get_cfbd_team_records(
            api_key=cfbd_key,
            team="Cincinnati"
        )
        print(json_data)
        time.sleep(5)

        # Get team records from football teams that played
        # in the Big 10 (B1G) conference in the 2017 CFB season
        print(
            "Get team records from football teams that played " +
            "in the Big 10 (B1G) conference in the 2017 CFB season"
        )
        json_data = get_cfbd_team_records(
            api_key=cfbd_key,
            season=2017,
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
        json_data = get_cfbd_team_records(
            season=2020,
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

        # Get CFB team records from the 2020 CFB season.
        print("Get CFB team records from the 2020 CFB season.")
        json_data = get_cfbd_team_records(
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get team records from football teams
        # fielded by the University of Cincinnati.
        print(
            "Get team records from football teams " +
            "fielded by the University of Cincinnati."
        )
        json_data = get_cfbd_team_records(
            team="Cincinnati"
        )
        print(json_data)
        time.sleep(5)

        # Get team records from football teams that played
        # in the Big 10 (B1G) conference in the 2017 CFB season
        print(
            "Get team records from football teams that played " +
            "in the Big 10 (B1G) conference in the 2017 CFB season"
        )
        json_data = get_cfbd_team_records(
            season=2017,
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
        json_data = get_cfbd_team_records(
            season=2020,
            return_as_dict=True
        )
        print(json_data)

    ```

    Returns
    ----------
    A pandas `DataFrame` object with CFB team records data,
    or (if `return_as_dict` is set to `True`)
    a dictionary object with CFB team records data.

    """

    now = datetime.now()
    cfb_records_df = pd.DataFrame()
    # row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/records"

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

    if season is not None and season > now.year:
        raise ValueError(f"`season` cannot be greater than {season}.")
    elif season is not None and season < 1869:
        raise ValueError("`season` cannot be less than 1869.")

    if season is None and team is None:
        raise ValueError(
            "If you call `cfbd_json_py.games.get_cfbd_team_records()`, "
            + "you must specify at least a team or CFB season."
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

    if team is not None and url_elements == 0:
        url += f"?team={team}"
        url_elements += 1
    elif team is not None:
        url += f"&team={team}"
        url_elements += 1

    if conference is not None and url_elements == 0:
        url += f"?conference={conference}"
        url_elements += 1
    elif conference is not None:
        url += f"&conference={conference}"
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

    cfb_records_df = pd.json_normalize(json_data)
    # print(cfb_records_df.columns)
    cfb_records_df.rename(
        columns={
            "year": "season",
            "teamId": "team_id",
            "team": "team_name",
            "conference": "conference_name",
            "division": "division_name",
            "expectedWins": "expected_wins",
            "total.games": "games",
            "total.wins": "wins",
            "total.losses": "losses",
            "total.ties": "ties",
            "conferenceGames.games": "conf_games",
            "conferenceGames.wins": "conf_wins",
            "conferenceGames.losses": "conf_losses",
            "conferenceGames.ties": "conf_ties",
            "homeGames.games": "home_games",
            "homeGames.wins": "home_wins",
            "homeGames.losses": "home_losses",
            "homeGames.ties": "home_ties",
            "awayGames.games": "away_games",
            "awayGames.wins": "away_wins",
            "awayGames.losses": "away_losses",
            "awayGames.ties": "away_ties",
        },
        inplace=True,
    )
    return cfb_records_df


def get_cfbd_season_weeks(
    season: int,
    api_key: str = None,
    api_key_dir: str = None,
    return_as_dict: bool = False,
):
    """
    Retrieves a list of weeks that occurred in a given CFB season.

    Parameters
    ----------
    `season` (int, mandatory):
        Required argument.
        Specifies the season you want a list of weeks that occurred
        in a given CFB season information from.
        This must be specified, otherwise this package, and by extension
        the CFBD API, will not accept the request
        to get a list of weeks that occurred in a given CFB season information.

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

    from cfbd_json_py.games import get_cfbd_season_weeks


    cfbd_key = "tigersAreAwesome"  # placeholder for your CFBD API Key.

    if cfbd_key is not "tigersAreAwesome":
        print(
            "Using the user's API key declared in this script " +
            "for this example."
        )

        # Get a list of weeks in the 2020 CFB season.
        print("Get a list of weeks in the 2020 CFB season.")
        json_data = get_cfbd_season_weeks(
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
        json_data = get_cfbd_season_weeks(
            season=2020,
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

        # Get a list of weeks in the 2020 CFB season.
        print("Get a list of weeks in the 2020 CFB season.")
        json_data = get_cfbd_season_weeks(
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
        json_data = get_cfbd_season_weeks(
            season=2020,
            return_as_dict=True
        )
        print(json_data)
    ```
    Returns
    ----------
    A pandas `DataFrame` object
    with a list of valid weeks in a given CFB season,
    or (if `return_as_dict` is set to `True`)
    a dictionary object with a list of valid weeks in a given CFB season.
    """

    now = datetime.now()
    cfb_weeks_df = pd.DataFrame()
    # row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/calendar"

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

    # URL builder
    ##########################################################################

    # Required by API
    url += f"?year={season}"

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

    cfb_weeks_df = pd.json_normalize(json_data)
    # print(cfb_weeks_df.columns)
    cfb_weeks_df.rename(
        columns={
            "firstGameStart": "first_game_start",
            "lastGameStart": "last_game_start",
        }
    )
    return cfb_weeks_df


def get_cfbd_game_media_info(
    season: int,
    api_key: str = None,
    api_key_dir: str = None,
    season_type: str = "regular",  # "regular", "postseason", or "both"
    week: int = None,
    team: str = None,
    conference: str = None,
    media_type: str = "all",  # "tv", "radio", "web", "ppv", or "mobile"
    ncaa_division: str = "fbs",
    return_as_dict: bool = False,
):
    """
    Gets known media information for CFB games in a given CFB season.

    Parameters
    ----------
    `season` (int, mandatory):
        Required argument.
        Specifies the season you want CFB media information from.
        This must be specified, otherwise this package, and by extension
        the CFBD API, will not accept the request to get CFB media information.

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

    `season_type` (str, semi-optional):
        Semi-optional argument.
        By default, this will be set to "regular", for the CFB regular season.
        If you want CFB media information for non-regular season games,
        set `season_type` to "postseason".
        If you want both "regular" and "postseason" games returned,
        set `season_type` to "both"
        If `season_type` is set to anything but "regular" or "postseason",
        a `ValueError()` will be raised.

    `week` (int, optional):
        Optional argument.
        If `week` is set to an integer, this function will attempt
        to load CFB media information from games in that season,
        and in that week.

    `team` (str, optional):
        Optional argument.
        If you only want CFB media information for a team,
        regardless if they are the home/away team,
        set `team` to the name of the team you want CFB media information from.

    `conference` (str, optional):
        Optional argument.
        If you only want media information from games
        involving teams a specific conference,
        set `conference` to the abbreviation
        of the conference you want game information from.

    `media_type` (str, semi-optional):
        Semi-optional argument.
        If you only want game broadcast information
        for a specific type of broadcast,
        set this to the type of broadcast.

        Valid inputs are:
        - `all` (default): Returns all games,
            and all known broadcasters for those games.
        - `tv`: Returns all known TV broadcasters for CFB games
            in the requested time frame.
        - `radio`: Returns all known radio broadcasters
            for CFB games in the requested time frame.
        - `web`: Returns all known web broadcasts (like ESPN+)
            for CFB games in the requested time frame.
        - `ppv`: Returns all known Pay Per View (PPV) broadcasts
            for CFB games in the requested time frame.
        - `mobile`: Returns all known broadcasters that only broadcasted
            games on mobile devices (?)

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

    from cfbd_json_py.games import get_cfbd_game_media_info


    cfbd_key = "tigersAreAwesome"  # placeholder for your CFBD API Key.

    if cfbd_key is not "tigersAreAwesome":
        print(
            "Using the user's API key declared in this script " +
            "for this example."
        )

        # Get a media information for the 2020 CFB season.
        print("Get a media information for the 2020 CFB season.")
        json_data = get_cfbd_game_media_info(
            api_key=cfbd_key,
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get a media information for postseason games in the 2020 CFB season.
        print("Get a media information for the 2020 CFB season.")
        json_data = get_cfbd_game_media_info(
            api_key=cfbd_key,
            season=2020,
            season_type="postseason"
        )
        print(json_data)
        time.sleep(5)

        # Get a media information for week 10 games in the 2020 CFB season.
        print(
            "Get a media information for week 10 games in the 2020 CFB season."
        )
        json_data = get_cfbd_game_media_info(
            api_key=cfbd_key,
            season=2020,
            week=10
        )
        print(json_data)
        time.sleep(5)

        # Get all known broadcasters for games played by
        # the Ohio State Football Program in the the 2019 CFB season.
        print(
            "Get all known broadcasters for games played by " +
            "the Ohio State Football Program in the the 2019 CFB season."
        )
        json_data = get_cfbd_game_media_info(
            api_key=cfbd_key,
            season=2020,
            team="Ohio State"
        )
        print(json_data)
        time.sleep(5)

        # Get all known radio broadcasters for games played by teams
        # within the American Athletic conference (AAC)
        # in the the 2021 CFB season.
        print(
            "Get all known radio broadcasters for games played " +
            "by teams within the American Athletic conference (AAC) " +
            "in the the 2021 CFB season."
        )
        json_data = get_cfbd_game_media_info(
            api_key=cfbd_key,
            season=2020,
            conference="AAC"
        )
        print(json_data)
        time.sleep(5)

        # Get all known radio broadcasters
        # for games in the the 2020 CFB season.
        print(
            "Get all known radio broadcasters " +
            "for games in the the 2020 CFB season."
        )
        json_data = get_cfbd_game_media_info(
            api_key=cfbd_key,
            season=2020,
            media_type="radio"
        )
        print(json_data)
        time.sleep(5)

        # Get all known broadcasters for
        # the Football Championship Subdivision (FCS) games
        # in the 2020 CFB season.
        print(
            "Get all known broadcasters for " +
            "the Football Championship Subdivision (FCS) games " +
            "in the 2020 CFB season."
        )
        json_data = get_cfbd_game_media_info(
            api_key=cfbd_key,
            season=2020,
            ncaa_division="fcs"
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print(
            "You can also tell this function to just return the API call " +
            "as a Dictionary (read: JSON) object."
        )
        json_data = get_cfbd_game_media_info(
            season=2020,
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

        # Get a media information for the 2020 CFB season.
        print("Get a media information for the 2020 CFB season.")
        json_data = get_cfbd_game_media_info(
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get a media information for postseason games in the 2020 CFB season.
        print("Get a media information for the 2020 CFB season.")
        json_data = get_cfbd_game_media_info(
            season=2020,
            season_type="postseason"
        )
        print(json_data)
        time.sleep(5)

        # Get a media information for week 10 games in the 2020 CFB season.
        print(
            "Get a media information for week 10 games in the 2020 CFB season."
        )
        json_data = get_cfbd_game_media_info(
            season=2020,
            week=10
        )
        print(json_data)
        time.sleep(5)

        # Get all known broadcasters for games played by
        # the Ohio State Football Program in the the 2019 CFB season.
        print(
            "Get all known broadcasters for games played by " +
            "the Ohio State Football Program in the the 2019 CFB season."
        )
        json_data = get_cfbd_game_media_info(
            season=2020,
            team="Ohio State"
        )
        print(json_data)
        time.sleep(5)

        # Get all known radio broadcasters for games played by teams
        # within the American Athletic conference (AAC)
        # in the the 2021 CFB season.
        print(
            "Get all known radio broadcasters for games played " +
            "by teams within the American Athletic conference (AAC) " +
            "in the the 2021 CFB season."
        )
        json_data = get_cfbd_game_media_info(
            season=2020,
            conference="AAC"
        )
        print(json_data)
        time.sleep(5)

        # Get all known radio broadcasters
        # for games in the the 2020 CFB season.
        print(
            "Get all known radio broadcasters " +
            "for games in the the 2020 CFB season."
        )
        json_data = get_cfbd_game_media_info(
            season=2020,
            media_type="radio"
        )
        print(json_data)
        time.sleep(5)

        # Get all known broadcasters for
        # the Football Championship Subdivision (FCS) games
        # in the 2020 CFB season.
        print(
            "Get all known broadcasters for " +
            "the Football Championship Subdivision (FCS) games " +
            "in the 2020 CFB season."
        )
        json_data = get_cfbd_game_media_info(
            season=2020,
            ncaa_division="fcs"
        )
        print(json_data)
        time.sleep(5)


        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print(
            "You can also tell this function to just return the API call " +
            "as a Dictionary (read: JSON) object."
        )
        json_data = get_cfbd_game_media_info(
            season=2020,
            return_as_dict=True
        )
        print(json_data)

    ```
    Returns
    ----------
    A pandas `DataFrame` object with college football media information,
    or (if `return_as_dict` is set to `True`)
    a dictionary object with college football media information.

    """

    now = datetime.now()
    cfb_games_df = pd.DataFrame()
    # row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/games/media"

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

    if (
        season_type != "both"
        and season_type != "regular"
        and season_type != "postseason"
    ):
        raise ValueError(
            "`season_type` must be set to "
            + '"both", "regular", or "postseason" for this function to work.'
        )

    if (
        media_type != "all"
        and media_type != "tv"
        and media_type != "radio"
        and media_type != "web"
        and media_type != "ppv"
        and media_type != "mobile"
    ):
        raise ValueError(
            "`media_type` must be set "
            + "to one of the following values for this function to work:"
            + "\n\t- `all`"
            + "\n\t- `tv`"
            + "\n\t- `radio`"
            + "\n\t- `web`"
            + "\n\t- `ppv`"
            + "\n\t- `mobile`"
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
            + f"\n\nYou entered: \n{ncaa_division}"
        )

    # URL builder
    ##########################################################################

    # Required by API
    url += f"?year={season}"

    if week is not None:
        url += f"&week={week}"

    if team is not None:
        url += f"&team={team}"

    if conference is not None:
        url += f"&conference={conference}"

    if season_type is not None:
        url += f"&seasonType={season_type}"

    if media_type == "all":
        # If we don't care about what media type we want back,
        # we don't need to add anything to the URL.
        pass
    elif media_type is not None:
        url += f"&mediaType={media_type}"

    if ncaa_division is not None:
        url += f"&classification={ncaa_division}"

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

    # for game in tqdm(json_data):
    #     row_df = pd.DataFrame({"season": season}, index=[0])
    #     row_df["week"] = game["week"]
    #     row_df["game_id"] = game["id"]
    #     row_df["season_type"] = game["seasonType"]
    #     row_df["game_start_time"] = game["startTime"]
    #     row_df["is_start_time_tbd"] = game["isStartTimeTBD"]
    #     row_df["home_team"] = game["homeTeam"]
    #     row_df["home_conference"] = game["homeConference"]
    #     row_df["away_team"] = game["awayTeam"]
    #     row_df["away_conference"] = game["awayConference"]
    #     row_df["media_type"] = game["mediaType"]
    #     row_df["outlet"] = game["outlet"]

    #     cfb_games_df = pd.concat([cfb_games_df, row_df], ignore_index=True)
    #     del row_df

    cfb_games_df = pd.json_normalize(json_data)
    # print(cfb_games_df.columns)
    cfb_games_df.rename(
        columns={
            "seasonType": "season_type",
            "startTime": "start_time",
            "isStartTimeTBD": "is_start_time_tbd",
            "homeTeam": "home_team_name",
            "homeConference": "home_conference_name",
            "awayTeam": "away_team_name",
            "awayConference": "away_conference_name",
            "mediaType": "media_type",
        },
        inplace=True,
    )
    return cfb_games_df


def get_cfbd_player_game_stats(
    season: int,
    api_key: str = None,
    api_key_dir: str = None,
    season_type: str = "regular",  # "regular" or "postseason"
    week: int = None,
    team: str = None,
    conference: str = None,
    # `week`, `team`, and/or `conference`
    # must be not null for this function to work.
    stat_category: str = None,
    game_id: int = None,
    return_as_dict: bool = False,
):
    """
    Retrieves player game stats for a given time frame.

    Parameters
    ----------
    `season` (int, mandatory):
        Required argument.
        Specifies the season you want CFB player game stats from.
        This must be specified, otherwise this package, and by extension
        the CFBD API, will not accept the request to get CFB player game stats.

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

    `season_type` (str, semi-optional):
        Semi-optional argument.
        By default, this will be set to "regular", for the CFB regular season.
        If you want CFB player game stats for non-regular season games,
        set `season_type` to "postseason".
        If `season_type` is set to anything but "regular" or "postseason",
        a `ValueError()` will be raised.

    **For the following three variables,
    at least one must be set to
    a non-null variable when calling this function.**

    `week` (int, optional):
        Optional argument.
        If `week` is set to an integer, this function will attempt
        to load CFB player game stats from games in that season,
        and in that week.

    `team` (str, optional):
        Optional argument.
        If you only want CFB player game stats for a team,
        regardless if they are the home/away team,
        set `team` to the name of the team you want CFB player game stats from.

    `conference` (str, optional):
        Optional argument.
        If you only want player game stats from games
        involving teams a specific conference,
        set `conference` to the abbreviation
        of the conference you want stats from.

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

    `game_id` (int, optional):
        Optional argument.
        If `game_id` is set to a game ID, `get_cfbd_player_game_stats()`
        will try to get player game stats just for that game ID.

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

    from cfbd_json_py.games import get_cfbd_player_game_stats


    cfbd_key = "tigersAreAwesome"  # placeholder for your CFBD API Key.

    if cfbd_key is not "tigersAreAwesome":
        print(
            "Using the user's API key declared in this script " +
            "for this example."
        )

        # Get player game stats for week 10 of the 2020 CFB season.
        print("Get player game stats for week 10 of the 2020 CFB season.")
        json_data = get_cfbd_player_game_stats(
            api_key=cfbd_key,
            season=2020,
            week=10
        )
        print(json_data)
        time.sleep(5)

        # Get postseason player game stats for the 2020 CFB season.
        print("Get postseason player game stats for the 2020 CFB season.")
        json_data = get_cfbd_player_game_stats(
            api_key=cfbd_key,
            season=2020,
            season_type="postseason",
            week=1
        )
        print(json_data)
        time.sleep(5)

        # Get player game stats for
        # the Alabama Crimson Tide Football Team for the 2018 CFB season.
        print(
            "Get player game stats for " +
            "the Alabama Crimson Tide Football Team for the 2018 CFB season."
        )
        json_data = get_cfbd_player_game_stats(
            api_key=cfbd_key,
            season=2018,
            team="Alabama"
        )
        print(json_data)
        time.sleep(5)

        # Get player game stats for players of teams in
        # the Atlantic Coast Conference (ACC) in the 2020 CFB season.
        print(
            "Get player game stats for players of teams in " +
            "the Atlantic Coast Conference (ACC) in the 2020 CFB season."
        )
        json_data = get_cfbd_player_game_stats(
            api_key=cfbd_key,
            season=2020,
            conference="ACC"
        )
        print(json_data)
        time.sleep(5)

        # Get get passing stats from players who played
        # in week 7 of the 2017 CFB season.
        print(
            "Get get passing stats from players who played " +
            "in week 7 of the 2017 CFB season."
        )
        json_data = get_cfbd_player_game_stats(
            api_key=cfbd_key,
            season=2017,
            week=7,
            stat_category="passing"
        )
        print(json_data)
        time.sleep(5)

        # Get player game stats from the 2021 Virbo Citrus Bowl,
        # a bowl game that happened in the 2020 CFB season.
        print(
            "Get player game stats from the 2021 Virbo Citrus Bowl, " +
            "a bowl game that happened in the 2020 CFB season."
        )
        json_data = get_cfbd_player_game_stats(
            api_key=cfbd_key,
            season=2020,
            game_id=401256199
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print(
            "You can also tell this function to just return the API call " +
            "as a Dictionary (read: JSON) object."
        )
        json_data = get_cfbd_player_game_stats(
            season=2020,
            week=10,
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

        # Get player game stats for week 10 of the 2020 CFB season.
        print("Get player game stats for week 10 of the 2020 CFB season.")
        json_data = get_cfbd_player_game_stats(
            season=2020,
            week=10
        )
        print(json_data)
        time.sleep(5)

        # Get postseason player game stats for the 2020 CFB season.
        print("Get postseason player game stats for the 2020 CFB season.")
        json_data = get_cfbd_player_game_stats(
            season=2020,
            season_type="postseason",
            week=1
        )
        print(json_data)
        time.sleep(5)

        # Get player game stats for
        # the Alabama Crimson Tide Football Team for the 2018 CFB season.
        print(
            "Get player game stats for " +
            "the Alabama Crimson Tide Football Team for the 2018 CFB season."
        )
        json_data = get_cfbd_player_game_stats(
            season=2018,
            team="Alabama"
        )
        print(json_data)
        time.sleep(5)

        # Get player game stats for players of teams in
        # the Atlantic Coast Conference (ACC) in the 2020 CFB season.
        print(
            "Get player game stats for players of teams in " +
            "the Atlantic Coast Conference (ACC) in the 2020 CFB season."
        )
        json_data = get_cfbd_player_game_stats(
            season=2020,
            conference="ACC"
        )
        print(json_data)
        time.sleep(5)

        # Get get passing stats from players who played
        # in week 7 of the 2017 CFB season.
        print(
            "Get get passing stats from players who played " +
            "in week 7 of the 2017 CFB season."
        )
        json_data = get_cfbd_player_game_stats(
            season=2017,
            week=7,
            stat_category="passing"
        )
        print(json_data)
        time.sleep(5)

        # Get player game stats from the 2021 Virbo Citrus Bowl,
        # a bowl game that happened in the 2020 CFB season,
        # between the Aubrun Tigers, and the Northwestern Wildcats.
        print("Get player game stats from the 2021 Virbo Citrus Bowl, "+
            "a bowl game that happened in the 2020 CFB season " +
            "between the Aubrun Tigers, and the Northwestern Wildcats."
        )
        json_data = get_cfbd_player_game_stats(
            season=2020,
            game_id=401256199
        )
        print(json_data)
        time.sleep(5)


        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print(
            "You can also tell this function to just return the API call " +
            "as a Dictionary (read: JSON) object."
        )
        json_data = get_cfbd_player_game_stats(
            season=2020,
            week=10,
            return_as_dict=True
        )
        print(json_data)

    ```
    Returns
    ----------
    A pandas `DataFrame` object with player game stats data,
    or (if `return_as_dict` is set to `True`)
    a dictionary object with player game stats data.

    """

    now = datetime.now()

    rebuilt_json = {}
    rebuilt_json_list = []

    cfb_games_df = pd.DataFrame()
    # row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/games/players"
    stat_columns = [
        "season",
        "game_id",
        "team_name",
        "team_conference",
        "player_id",
        "player_name",
        "home_away",
        # PASS
        "passing_C/ATT",
        "passing_COMP",
        "passing_ATT",
        "passing_YDS",
        "passing_AVG",
        "passing_TD",
        "passing_INT",
        "passing_QBR",
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
        "kicking_FG",
        "kicking_FGM",
        "kicking_FGA",
        "kicking_PCT",
        "kicking_LONG",
        "kicking_XP",
        "kicking_XPM",
        "kicking_XPA",
        "kicking_PTS",
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
            '`season_type` must be set to either "regular" or '
            + '"postseason" for this function to work.'
        )

    # `week`, `team`, and/or `conference`
    # must be not null for this function to work.

    if (
        week is None and
        team is None and
        conference is None and
        game_id is None
    ):
        raise ValueError(
            "To use `get_cfbd_player_game_stats()`,"
            + " `week`, `team`, and/or `conference` "
            + "need to be set to a non-null value."
        )

    filter_by_stat_category = False

    if stat_category is None:
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

    # URL builder
    ##########################################################################

    # Required by the API
    url += f"?year={season}"

    if game_id is not None:
        url += f"&gameId={game_id}"

        if stat_category is not None:
            url += f"&category={stat_category}"

        if week is not None or team is not None or conference is not None:
            logging.warning(
                "When calling "
                + "`cfbd_json_py.games.get_cfbd_player_game_stats()`"
                + ", and setting `game_id` to a non-null value, "
                + "only `season`, `stat_category`, "
                + "and `game_id` are considered "
                + "when calling the CFBD API."
            )
    else:
        if season_type is not None:
            url += f"&seasonType={season_type}"

        if week is not None:
            url += f"&week={week}"

        if team is not None:
            url += f"&team={team}"

        if conference is not None:
            url += f"&conference={conference}"

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

    for game in tqdm(json_data):
        game_id = game["id"]

        for team in game["teams"]:
            team_name = team["school"]
            team_conference = team["conference"]
            home_away = team["homeAway"]

            for stat_category in team["categories"]:
                stat_category = stat_category["name"]
                for s_type in stat_category["types"]:
                    stat_name = s_type["name"]
                    for player in s_type["athletes"]:
                        p_id = player["id"]
                        p_name = player["name"]
                        full_stat_name = f"{stat_category}_{stat_name}"
                        stat_value = player["stat"]

                        if rebuilt_json.get(p_id) is None:
                            rebuilt_json[p_id] = {}
                        rebuilt_json[p_id]["player_id"] = p_id
                        rebuilt_json[p_id]["game_id"] = game_id
                        rebuilt_json[p_id]["team_name"] = team_name
                        rebuilt_json[p_id]["team_conference"] = team_conference
                        rebuilt_json[p_id]["home_away"] = home_away
                        rebuilt_json[p_id]["player_name"] = p_name
                        rebuilt_json[p_id][full_stat_name] = stat_value

    for _, value in rebuilt_json.items():
        rebuilt_json_list.append(value)
    cfb_games_df = pd.DataFrame(rebuilt_json_list)
    cfb_games_df["season"] = season

    cfb_games_df[["passing_COMP", "passing_ATT"]] = cfb_games_df[
        "passing_C/ATT"
    ].str.split("/", expand=True)

    cfb_games_df[["kicking_FGM", "kicking_FGA"]] = cfb_games_df[
        "kicking_FG"
    ].str.split(
        "/", expand=True
    )

    cfb_games_df[["kicking_XP", "kicking_XPM"]] = cfb_games_df[
        "kicking_XP"
    ].str.split(
        "/", expand=True
    )

    cfb_games_df = cfb_games_df.reindex(
        columns=stat_columns
    )

    cfb_games_df = cfb_games_df.replace(np.nan, 0)
    cfb_games_df = cfb_games_df.astype(
        {
            "season": "uint16",
            "game_id": "int64",
            "team_name": "str",
            "team_conference": "str",
            "player_id": "int64",
            "player_name": "str",
            "home_away": "str",

            "passing_COMP": "uint16",
            "passing_ATT": "uint16",
            "passing_YDS": "int16",
            "passing_TD": "uint16",
            "passing_INT": "uint16",
            "passing_AVG": "float16",

            "rushing_CAR": "uint16",
            "rushing_YDS": "int16",
            "rushing_AVG": "float16",
            "rushing_TD": "uint16",
            "rushing_LONG": "int16",

            "receiving_REC": "uint16",
            "receiving_YDS": "int16",
            "receiving_AVG": "float16",
            "receiving_TD": "uint16",
            "receiving_LONG": "int16",

            "fumbles_FUM": "uint8",
            "fumbles_LOST": "uint8",
            "fumbles_REC": "uint8",

            "defensive_TOT": "uint16",
            "defensive_SOLO": "uint16",
            "defensive_TFL": "float16",
            "defensive_QB HUR": "uint16",
            "defensive_SACKS": "float16",
            "defensive_PD": "uint16",
            "defensive_TD": "uint8",

            "interceptions_INT": "uint8",
            "interceptions_YDS": "int16",
            "interceptions_TD": "uint8",

            "punting_NO": "uint16",
            "punting_YDS": "int16",
            "punting_AVG": "float16",
            "punting_TB": "uint8",
            "punting_In 20": "uint8",
            "punting_LONG": "int8",

            "kicking_FGM": "uint16",
            "kicking_FGA": "uint16",
            "kicking_PCT": "float16",
            "kicking_LONG": "uint8",
            "kicking_XPM": "uint16",
            "kicking_XPA": "uint16",
            "kicking_PTS": "uint16",

            "kickReturns_NO": "uint16",
            "kickReturns_YDS": "int16",
            "kickReturns_AVG": "float16",
            "kickReturns_TD": "uint8",
            "kickReturns_LONG": "int8",

            "puntReturns_NO": "uint16",
            "puntReturns_YDS": "int16",
            "puntReturns_AVG": "float16",
            "puntReturns_TD": "uint8",
            "puntReturns_LONG": "int8",
        }
    )

    if filter_by_stat_category is True and stat_category == "passing":
        cfb_games_df = cfb_games_df[[
            "season",
            "game_id",
            "team_name",
            "team_conference",
            "player_id",
            "player_name",
            "home_away",
            # PASS
            "passing_C/ATT",
            "passing_COMP",
            "passing_ATT",
            "passing_YDS",
            "passing_AVG",
            "passing_TD",
            "passing_INT",
            "passing_QBR",
        ]]
    elif filter_by_stat_category is True and stat_category == "rushing":
        cfb_games_df = cfb_games_df[[
            "season",
            "game_id",
            "team_name",
            "team_conference",
            "player_id",
            "player_name",
            "home_away",
            # RUSH
            "rushing_CAR",
            "rushing_YDS",
            "rushing_AVG",
            "rushing_TD",
            "rushing_LONG",
        ]]
    elif filter_by_stat_category is True and stat_category == "receiving":
        cfb_games_df = cfb_games_df[[
            "season",
            "game_id",
            "team_name",
            "team_conference",
            "player_id",
            "player_name",
            "home_away",
            # REC
            "receiving_REC",
            "receiving_YDS",
            "receiving_AVG",
            "receiving_TD",
            "receiving_LONG",
        ]]
    elif filter_by_stat_category is True and stat_category == "fumbles":
        cfb_games_df = cfb_games_df[[
            "season",
            "game_id",
            "team_name",
            "team_conference",
            "player_id",
            "player_name",
            "home_away",
            # FUM
            "fumbles_FUM",
            "fumbles_LOST",
            "fumbles_REC",
        ]]
    elif filter_by_stat_category is True and stat_category == "defensive":
        cfb_games_df = cfb_games_df[[
            "season",
            "game_id",
            "team_name",
            "team_conference",
            "player_id",
            "player_name",
            "home_away",
            # DEFENSE
            "defensive_TOT",
            "defensive_SOLO",
            "defensive_TFL",
            "defensive_QB HUR",
            "defensive_SACKS",
            "defensive_PD",
            "defensive_TD",
        ]]
    elif filter_by_stat_category is True and stat_category == "interceptions":
        cfb_games_df = cfb_games_df[[
            "season",
            "game_id",
            "team_name",
            "team_conference",
            "player_id",
            "player_name",
            "home_away",
            # INT
            "interceptions_INT",
            "interceptions_YDS",
            "interceptions_TD",
        ]]
    elif filter_by_stat_category is True and stat_category == "punting":
        cfb_games_df = cfb_games_df[[
            "season",
            "game_id",
            "team_name",
            "team_conference",
            "player_id",
            "player_name",
            "home_away",
            # PUNT
            "punting_NO",
            "punting_YDS",
            "punting_AVG",
            "punting_TB",
            "punting_In 20",
            "punting_LONG",
        ]]
    elif filter_by_stat_category is True and stat_category == "kicking":
        cfb_games_df = cfb_games_df[[
            "season",
            "game_id",
            "team_name",
            "team_conference",
            "player_id",
            "player_name",
            "home_away",
            # KICK
            "kicking_FG",
            "kicking_FGM",
            "kicking_FGA",
            "kicking_PCT",
            "kicking_LONG",
            "kicking_XP",
            "kicking_XPM",
            "kicking_XPA",
            "kicking_PTS",
        ]]
    elif filter_by_stat_category is True and stat_category == "kickReturns":
        cfb_games_df = cfb_games_df[[
            "season",
            "game_id",
            "team_name",
            "team_conference",
            "player_id",
            "player_name",
            "home_away",
            # KR
            "kickReturns_NO",
            "kickReturns_YDS",
            "kickReturns_AVG",
            "kickReturns_TD",
            "kickReturns_LONG",
        ]]
    elif filter_by_stat_category is True and stat_category == "puntReturns":
        cfb_games_df = cfb_games_df[[
            "season",
            "game_id",
            "team_name",
            "team_conference",
            "player_id",
            "player_name",
            "home_away",
            # KR
            "puntReturns_NO",
            "puntReturns_YDS",
            "puntReturns_AVG",
            "puntReturns_TD",
            "puntReturns_LONG",
        ]]

    return cfb_games_df


def get_cfbd_player_advanced_game_stats(
    game_id: int,
    api_key: str = None,
    api_key_dir: str = None,
    return_as_dict: bool = False,
):
    """
    Retrieves advanced game stats from the CFBD API.

    Parameters
    ----------
    `game_id` (int, mandatory):
        Mandatory requirement.
        Specifies the game you want advanced game stats from.

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

    from cfbd_json_py.games import get_cfbd_player_advanced_game_stats


    cfbd_key = "tigersAreAwesome"  # placeholder for your CFBD API Key.

    if cfbd_key is not "tigersAreAwesome":
        print(
            "Using the user's API key declared in this script " +
            "for this example."
        )

        # Get advanced player stats for a 2019 CFB game
        # between the LSU Tigers Football Program,
        # and the Oklahoma Sooners Football Program.
        print(
            "Get advanced player stats for a 2019 CFB game between " +
            "the LSU Tigers Football Program, " +
            "and the Oklahoma Sooners Football Program."
        )
        json_data = get_cfbd_player_advanced_game_stats(
            api_key=cfbd_key,
            game_id=401135278
        )
        print(json_data)
        time.sleep(5)


        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print(
            "You can also tell this function to just return the API call " +
            "as a Dictionary (read: JSON) object."
        )
        json_data = get_cfbd_player_advanced_game_stats(
            api_key=cfbd_key,
            game_id=401135278,
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

        # Get advanced player stats for a 2019 CFB game
        # between the LSU Tigers Football Program,
        # and the Oklahoma Sooners Football Program.
        print(
            "Get advanced player stats for a 2019 CFB game " +
            "between the LSU Tigers Football Program, " +
            "and the Oklahoma Sooners Football Program."
        )
        json_data = get_cfbd_player_advanced_game_stats(
            game_id=401135278
        )
        print(json_data)
        time.sleep(5)


        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print(
            "You can also tell this function to just return the API call " +
            "as a Dictionary (read: JSON) object."
        )
        json_data = get_cfbd_player_advanced_game_stats(
            game_id=401135278,
            return_as_dict=True
        )
        print(json_data)

    ```
    Returns
    ----------
    A pandas `DataFrame` object with college football game information,
    or (if `return_as_dict` is set to `True`)
    a dictionary object with college football game information.
    """

    # now = datetime.now()
    usage_df = pd.DataFrame()
    ppa_df = pd.DataFrame()
    adv_stats_df = pd.DataFrame()
    row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/game/box/advanced"

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

    # URL builder
    ##########################################################################

    # Required by API
    url += f"?gameId={game_id}"

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

    home_team_name = json_data["gameInfo"]["homeTeam"]
    home_points = json_data["gameInfo"]["homePoints"]
    home_win_prob = json_data["gameInfo"]["homeWinProb"]
    away_team_name = json_data["gameInfo"]["awayTeam"]
    away_points = json_data["gameInfo"]["awayPoints"]
    away_win_prob = json_data["gameInfo"]["awayWinProb"]
    home_winner = json_data["gameInfo"]["homeWinner"]
    game_excitement_score = json_data["gameInfo"]["excitement"]

    # Parsing Usage
    logging.info("Parsing player usage data.")
    for player in json_data["players"]["usage"]:
        row_df = pd.DataFrame({"game_id": game_id}, index=[0])
        row_df["player_name"] = player["player"]
        row_df["team"] = player["team"]
        row_df["position"] = player["position"]

        row_df["total_usage"] = player["total"]
        row_df["q1_usage"] = player["quarter1"]
        row_df["q2_usage"] = player["quarter2"]
        row_df["q3_usage"] = player["quarter3"]
        row_df["q4_usage"] = player["quarter4"]
        row_df["rushing_usage"] = player["rushing"]
        row_df["passing_usage"] = player["passing"]

        usage_df = pd.concat([usage_df, row_df], ignore_index=True)
        del row_df

    # Parsing PPA
    logging.info("Parsing player PPA data.")
    for player in json_data["players"]["ppa"]:
        row_df = pd.DataFrame({"game_id": game_id}, index=[0])
        row_df["player_name"] = player["player"]
        row_df["team"] = player["team"]
        row_df["position"] = player["position"]

        row_df["average_ppa_total"] = player["average"]["total"]
        row_df["average_ppa_q1"] = player["average"]["quarter1"]
        row_df["average_ppa_q2"] = player["average"]["quarter2"]
        row_df["average_ppa_q3"] = player["average"]["quarter3"]
        row_df["average_ppa_q4"] = player["average"]["quarter4"]
        row_df["average_ppa_rushing"] = player["average"]["rushing"]
        row_df["average_ppa_passing"] = player["average"]["passing"]

        row_df["cumulative_ppa_total"] = player["cumulative"]["total"]
        row_df["cumulative_ppa_q1"] = player["cumulative"]["quarter1"]
        row_df["cumulative_ppa_q2"] = player["cumulative"]["quarter2"]
        row_df["cumulative_ppa_q3"] = player["cumulative"]["quarter3"]
        row_df["cumulative_ppa_q4"] = player["cumulative"]["quarter4"]
        row_df["cumulative_ppa_rushing"] = player["cumulative"]["rushing"]
        row_df["cumulative_ppa_passing"] = player["cumulative"]["passing"]

        ppa_df = pd.concat([ppa_df, row_df], ignore_index=True)

    # Join `usage_df` and `ppa_df` together
    adv_stats_df = pd.merge(
        left=usage_df,
        right=ppa_df,
        how="outer",
        on=["game_id", "player_name", "team", "position"],
    )

    # Add in these columns for completeness.

    adv_stats_df.loc[
        adv_stats_df["team"] == home_team_name, "home_away"
    ] = "home"
    adv_stats_df.loc[adv_stats_df["team"] == home_team_name, "opponent"] = (
        away_team_name
    )

    adv_stats_df.loc[
        adv_stats_df["team"] == away_team_name, "home_away"
    ] = "away"
    adv_stats_df.loc[adv_stats_df["team"] == away_team_name, "opponent"] = (
        home_team_name
    )

    adv_stats_df["home_team"] = home_team_name
    adv_stats_df["away_team"] = away_team_name

    adv_stats_df["home_win_prob"] = home_win_prob
    adv_stats_df["away_win_prob"] = away_win_prob

    adv_stats_df["home_points"] = home_points
    adv_stats_df["away_points"] = away_points

    adv_stats_df["home_winner"] = home_winner
    adv_stats_df["game_excitement_score"] = game_excitement_score

    return adv_stats_df


###############################################################################
# Patreon Only Functions.
#   No caching, because the entire point of these functions are to get people
#   data ASAP, and right before kickoff.
###############################################################################


def get_cfbd_live_scoreboard(
    ncaa_division: str = "fbs",
    conference: str = None,
    api_key: str = None,
    api_key_dir: str = None,
    return_as_dict: bool = False,
):
    """
    YOU MUST BE SUBSCRIBED TO THE CFBD PATREON FOR THIS FUNCTION TO WORK!
    To view the CFBD Patreon, visit https://www.patreon.com/collegefootballdata

    Retrieves live scoreboard data from the CFBD API,
    assuming the API key is an API key from a Patreon supporter.

    Parameters
    ----------
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

    `conference` (str, optional):
        Optional argument.
        If you only want live scoreboard data from games
        involving teams a specific conference,
        set `conference` to the abbreviation
        of the conference you want live scoreboard data from.

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

    from cfbd_json_py.games import get_cfbd_live_scoreboard


    cfbd_key = "tigersAreAwesome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwesome":
        print(
            "Using the user's API key declared " +
            "in this script for this example."
        )

        # Get live scoreboard data from the CFBD API.
        print(
            "Get live scoreboard data from the CFBD API."
        )
        json_data = get_cfbd_live_scoreboard(
            api_key=cfbd_key
        )
        print(json_data)
        time.sleep(5)

        # Get live scoreboard data from the CFBD API,
        # but only from the FCS ranks.
        print(
            "Get live scoreboard data from the CFBD API, " +
            "but only from the FCS ranks."
        )
        json_data = get_cfbd_live_scoreboard(
            ncaa_division="fcs",
            api_key=cfbd_key
        )
        print(json_data)
        time.sleep(5)

        # Get live scoreboard data from the CFBD API,
        # but only from the Atlantic Coast Conference.
        print(
            "Get live scoreboard data from the CFBD API, " +
            "but only from the Atlantic Coast Conference."
        )
        json_data = get_cfbd_live_scoreboard(
            conference="ACC",
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
        json_data = get_cfbd_live_scoreboard(
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

        # Get live scoreboard data from the CFBD API.
        print(
            "Get live scoreboard data from the CFBD API."
        )
        json_data = get_cfbd_live_scoreboard()
        print(json_data)
        time.sleep(5)

        # Get live scoreboard data from the CFBD API,
        # but only from the FCS ranks.
        print(
            "Get live scoreboard data from the CFBD API, " +
            "but only from the FCS ranks."
        )
        json_data = get_cfbd_live_scoreboard(
            ncaa_division="fcs",
        )
        print(json_data)
        time.sleep(5)

        # Get live scoreboard data from the CFBD API,
        # but only from the Atlantic Coast Conference.
        print(
            "Get live scoreboard data from the CFBD API, " +
            "but only from the Atlantic Coast Conference."
        )
        json_data = get_cfbd_live_scoreboard(
            conference="ACC",
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print(
            "You can also tell this function to just return the API call " +
            "as a Dictionary (read: JSON) object."
        )
        json_data = get_cfbd_live_scoreboard(
            return_as_dict=True
        )
        print(json_data)

    ```

    Returns
    ----------
    A pandas `DataFrame` object with live scoreboard data,
    or (if `return_as_dict` is set to `True`)
    a dictionary object with live scoreboard data.

    """
    # real_api_key = ""
    scoreboard_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/scoreboard"

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

    url += f"?classification={ncaa_division}"

    if conference is not None and len(conference) > 0:
        url += f"&conference={conference}"

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

    scoreboard_df = pd.json_normalize(json_data)

    if len(scoreboard_df) > 0:
        scoreboard_df.rename(
            columns={
                "id": "game_id",
                "startDate": "start_datetime",
                "startTimeTBD": "is_start_time_tbd",
                "tv": "tv_network",
                "neutralSite": "is_neutral_site_game",
                "conferenceGame": "is_conference_game",
                "venue.name": "stadium_name",
                "venue.city": "stadium_city",
                "venue.state": "stadium_state",
                "homeTeam.id": "home_team_id",
                "homeTeam.name": "home_team_name",
                "homeTeam.conference": "home_team_conference",
                "awayTeam.id": "away_team_id",
                "awayTeam.name": "away_team_name",
                "awayTeam.conference": "away_team_conference",
                "weather.temperature": "weather_temperature",
                "weather.description": "weather_description",
                "weather.windSpeed": "weather_wind_speed",
                "weather.windDirection": "weather_wind_direction",
                "betting.spread": "betting_spread",
                "betting.overUnder": "betting_over_under",
                "betting.homeMoneyline": "betting_home_moneyline",
                "betting.awayMoneyline": "betting_away_moneyline",
            },
            inplace=True,
        )

    return scoreboard_df


def get_cfbd_weather_info(
    # game_id: int = None,
    season: int = None,
    # `game_id` and/or `season` must be not null for this function to work.
    week: int = None,
    season_type: str = "both",  # "regular", "postseason", or "both"
    conference: str = None,
    team_name: str = None,
    ncaa_division: str = "fbs",
    api_key: str = None,
    api_key_dir: str = None,
    return_as_dict: bool = False,
):
    """
    YOU MUST BE SUBSCRIBED TO THE CFBD PATREON FOR THIS FUNCTION TO WORK!
    To view the CFBD Patreon, visit https://www.patreon.com/collegefootballdata

    Parameters
    ----------
    Retrieves live scoreboard data from the CFBD API,
    assuming the API key is an API key from a Patreon supporter.

    Parameters
    ----------

    `game_id` (int, mandatory):
        DEPRECATED FROM V1.
        Specifies the game you want weather data from.
        This or `season` must be set to a valid non-null value.

    `season` (int, mandatory):
        Mandatory requirement.
        Specifies the season you want weather data from.
        This or `season` must be set to a valid non-null value.

    `week` (int, optional):
        Optional argument.
        If `week` is set to an integer, this function will attempt
        to load weather data from games in that season, and in that week.

    `season_type` (str, semi-optional):
        Semi-optional argument.
        By default, this will be set to "both", for the CFB regular season.
        If you want postseason betting data, set `season_type` to "postseason".
        If `season_type` is set to anything but "regular" or "postseason",
        a `ValueError()` will be raised.

    `conference` (str, optional):
        Optional argument.
        If you only want weather data from games
        involving teams a specific conference,
        set `conference` to the abbreviation
        of the conference you want weather data from.

    `team_name` (str, optional):
        Optional argument.
        If you only want weather data for a team,
        regardless if they are the home/away team,
        set `team` to the name of the team
        you want weather data from.

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

    from cfbd_json_py.games import get_cfbd_weather_info


    cfbd_key = "tigersAreAwesome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwesome":
        print(
            "Using the user's API key declared " +
            "in this script for this example."
        )

        # Get weather data for the 2024 CFB season
        print(
            "Get weather data for the 2024 CFB season."
        )
        json_data = get_cfbd_weather_info(
            season=2024,
            api_key=cfbd_key
        )
        print(json_data)
        time.sleep(5)

        # Get weather data for the 2024 Rose Bowl (game ID #401551786).
        print(
            "Get weather data for the 2024 Rose Bowl (game ID #401551786)."
        )
        json_data = get_cfbd_weather_info(
            game_id=401551786,
            api_key=cfbd_key
        )
        print(json_data)
        time.sleep(5)

        # Get weather data for week 1 of the 2024 CFB season
        print(
            "Get weather data for week 1 of the 2024 CFB season."
        )
        json_data = get_cfbd_weather_info(
            season=2024,
            week=1,
            api_key=cfbd_key
        )
        print(json_data)
        time.sleep(5)

        # Get weather data for postseason games of the 2023 CFB season.
        print(
            "Get weather data for postseason games of the 2023 CFB season."
        )
        json_data = get_cfbd_weather_info(
            season=2023,
            season_type="postseason",
            api_key=cfbd_key
        )
        print(json_data)
        time.sleep(5)

        # Get weather data for postseason games of the 2023 CFB season.
        print(
            "Get weather data for postseason games of the 2023 CFB season."
        )
        json_data = get_cfbd_weather_info(
            season=2023,
            season_type="postseason",
            api_key=cfbd_key
        )
        print(json_data)
        time.sleep(5)

        # Get weather data for Big 10 (B1G) games of the 2024 CFB season.
        print(
            "Get weather data for Big 10 (B1G) games of the 2024 CFB season."
        )
        json_data = get_cfbd_weather_info(
            season=2024,
            conference="B1G",
            api_key=cfbd_key
        )
        print(json_data)
        time.sleep(5)

        # Get weather data for FCS games of the 2024 CFB season.
        print(
            "Get weather data for FCS games of the 2024 CFB season."
        )
        json_data = get_cfbd_weather_info(
            season=2024,
            ncaa_division="fcs",
            api_key=cfbd_key
        )
        print(json_data)
        time.sleep(5)

        # Get weather data for University of Cincinnati games
        # of the 2024 CFB season.
        print(
            "Get weather data for Big 10 (B1G) games of the 2024 CFB season."
        )
        json_data = get_cfbd_weather_info(
            season=2024,
            team_name="Cincinnati",
            api_key=cfbd_key
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call
        # as a Dictionary (read: JSON) object.
        print(
            "You can also tell this function to just return the API call " +
            "as a Dictionary (read: JSON) object."
        )
        json_data = get_cfbd_weather_info(
            api_key=cfbd_key,
            season=2023,
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

        # Get weather data for the 2024 CFB season
        print(
            "Get weather data for the 2024 CFB season."
        )
        json_data = get_cfbd_weather_info(
            season=2024
        )
        print(json_data)
        time.sleep(5)

        # Get weather data for the 2024 Rose Bowl (game ID #401551786).
        print(
            "Get weather data for the 2024 Rose Bowl (game ID #401551786)."
        )
        json_data = get_cfbd_weather_info(
            game_id=401551786
        )
        print(json_data)
        time.sleep(5)

        # Get weather data for week 1 of the 2024 CFB season
        print(
            "Get weather data for week 1 of the 2024 CFB season."
        )
        json_data = get_cfbd_weather_info(
            season=2024,
            week=1
        )
        print(json_data)
        time.sleep(5)

        # Get weather data for postseason games of the 2023 CFB season.
        print(
            "Get weather data for postseason games of the 2023 CFB season."
        )
        json_data = get_cfbd_weather_info(
            season=2023,
            season_type="postseason"
        )
        print(json_data)
        time.sleep(5)

        # Get weather data for postseason games of the 2023 CFB season.
        print(
            "Get weather data for postseason games of the 2023 CFB season."
        )
        json_data = get_cfbd_weather_info(
            season=2023,
            season_type="postseason"
        )
        print(json_data)
        time.sleep(5)

        # Get weather data for Big 10 (B1G) games of the 2024 CFB season.
        print(
            "Get weather data for Big 10 (B1G) games of the 2024 CFB season."
        )
        json_data = get_cfbd_weather_info(
            season=2024,
            conference="B1G"
        )
        print(json_data)
        time.sleep(5)

        # Get weather data for FCS games of the 2024 CFB season.
        print(
            "Get weather data for FCS games of the 2024 CFB season."
        )
        json_data = get_cfbd_weather_info(
            season=2024,
            ncaa_division="fcs"
        )
        print(json_data)
        time.sleep(5)

        # Get weather data for University of Cincinnati games
        # of the 2024 CFB season.
        print(
            "Get weather data for Big 10 (B1G) games of the 2024 CFB season."
        )
        json_data = get_cfbd_weather_info(
            season=2024,
            team_name="Cincinnati"
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call
        # as a Dictionary (read: JSON) object.
        print(
            "You can also tell this function to just return the API call " +
            "as a Dictionary (read: JSON) object."
        )
        json_data = get_cfbd_weather_info(
            season=2023,
            return_as_dict=True
        )
        print(json_data)

    ```
    Returns
    ----------
    A pandas `DataFrame` object with live weather data,
    or (if `return_as_dict` is set to `True`)
    a dictionary object with live weather data.

    """

    weather_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/games/weather"

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

    # if (game_id is None) and (season is None):
    #     raise ValueError(
    #         "`game_id` and/or `season` must be set to " +
    #         "valid, non-null values."
    #     )
    # elif (game_id is not None) and (season is not None):
    #     url += f"?gameId={game_id}&year={season}"
    # elif game_id is not None:
    #     url += f"?gameId={game_id}"
    # elif season is not None:
    #     url += f"?year={season}"
    if season is None:
        raise ValueError(
            "`season` must be set to a valid, non-null value."
        )
    elif season is not None:
        url += f"?year={season}"

    if (ncaa_division is not None) and (
        ncaa_division.lower() == "fbs"
        or ncaa_division.lower() == "fcs"
        or ncaa_division.lower() == "ii"
        or ncaa_division.lower() == "iii"
    ):
        ncaa_division = ncaa_division.lower()
        url += f"&classification={ncaa_division}"
    else:
        raise ValueError(
            "An invalid NCAA Division was inputted when calling this function."
            + '\nValid inputs are:\n-"fbs"\n-"fcs"\n-"ii"\n-"iii"'
            + f"\n\nYou entered:\n{ncaa_division}"
        )

    if week is not None:
        url += f"&week={week}"

    if (
        season_type == "regular" or
        season_type == "postseason" or
        season_type == "both"
    ):
        url += f"&seasonType={season_type}"
    elif season_type is not None:
        raise ValueError(
            '`season_type` must be set to either "regular", '
            + '"postseason", or "both" if you want to specify '
            + "a part of the season."
        )

    if team_name is not None:
        url += f"&team={team_name}"

    if conference is not None:
        url += f"&conference={conference}"

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

    weather_df = pd.json_normalize(json_data)
    # print(weather_df.columns)

    [
        "weatherConditionCode",
        "weatherCondition",
    ]
    if len(weather_df) > 0:
        weather_df.rename(
            columns={
                "id": "game_id",
                "startTime": "start_datetime",
                "seasonType": "season_type",
                "gameIndoors": "is_game_indoors",
                "homeTeam": "home_team_name",
                "homeConference": "home_team_conference",
                "awayTeam": "away_team_name",
                "awayConference": "away_team_conference",
                "venueId": "venue_id",
                "venue": "venue_name",
                "windDirection": "wind_direction",
                "windSpeed": "wind_speed",
                "weatherConditionCode": "weather_condition_code",
                "weatherCondition": "weather_condition",
            },
            inplace=True,
        )

    return weather_df
