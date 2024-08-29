# Creation Date: 08/30/2023 01:13 EDT
# Last Updated Date: 08/13/2024 02:10 PM EDT
# Author: Joseph Armstrong (armstrongjoseph08@gmail.com)
# File Name: betting.py
# Purpose: Houses functions pertaining to betting data within the CFBD API.
###############################################################################

# import warnings

import pandas as pd
import requests
from tqdm import tqdm

from cfbd_json_py.utls import get_cfbd_api_token


def get_cfbd_betting_lines(
    season: int = None,
    api_key: str = None,
    api_key_dir: str = None,
    # game_id: int = None,
    week: int = None,
    season_type: str = "regular",  # "regular" or "postseason"
    team: str = None,
    home_team: str = None,
    away_team: str = None,
    conference: str = None,
    year: int = None,
    home: str = None,
    away: str = None,
    # cache_data: bool = False,
    # cache_dir: str = None,
    return_as_dict: bool = False,
):
    """
    Retrieves betting information from the CFBD API for a given season,
    or you could only get betting information for a single game.

    Parameters
    ----------

    `season` (int, mandatory):
        The season you want to retrieve betting information from.

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

    `game_id` (int, optional):
        DEPRECATED FROM V1.
        If `game_id` is set to a game ID,
        `get_cfb_betting_lines()` will try to get
        all betting information for that game ID.

    `week` (int, optional):
        Optional argument.
        If `week` is set to an integer, this function will attempt
        to load betting data from games in that season, and that week.

    `season_type` (str, semi-optional):
        Semi-optional argument.
        By default, this will be set to "regular", for the CFB regular season.
        If you want postseason betting data, set `season_type` to "postseason".
        If `season_type` is set to anything but "regular" or "postseason",
        a `ValueError()` will be raised.

    `team` (str, optional):
        Optional argument.
        If you only want betting information for a team,
        regardless if they are the home/away team,
        set `team` to the name of the team
        you want game-level betting data from.

    `home_team` (str, optional):
        Optional argument.
        If you only want betting information for a team,
        where that team was the home team in this season,
        set `home_team` to the name of the team
        you want game-level betting data from.


    `away_team` (str, optional):
        Optional argument.
        If you only want betting information for a team,
        where that team was the away team in this season,
        set `away_team` to the name of the team
        you want game-level betting data from.

    `conference` (str, optional):
        Optional argument.
        If you only want betting information from games
        involving teams a specific conference,
        set `conference` to the abbreviation
        of the conference you want betting information from.

    `year` (int):
        Alternative keyword for `season`

    `home` (str):
        Alternative keyword for `home_team`

    `away` (str):
        Alternative keyword for `away_team`

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

    from cfbd_json_py.betting import get_cfbd_betting_lines

    cfbd_key = "tigersAreAwesome"  # placeholder for your CFBD API Key.

    if cfbd_key is not "tigersAreAwesome":
        print(
            "Using the user's API key declared " +
            "in this script for this example."
        )


        # Get all available betting info for the 2020 CFB season, in week 2.
        print(
            "Get all available betting info for the 2020 CFB season, "+
            "in week 2."
        )
        json_data = get_cfbd_betting_lines(
            api_key=cfbd_key,
            season=2020,
            week=2
        )
        print(json_data)
        time.sleep(5)

        # Get all betting info for the 2020 CFB season,
        # in the postseason (bowls, playoffs, etc.).
        print(
            "Get all betting info for the 2020 CFB season, " +
            "in the postseason (bowls, playoffs, etc.)."
        )
        json_data = get_cfbd_betting_lines(
            api_key=cfbd_key,
            season=2020,
            season_type="postseason"
        )
        print(json_data)
        time.sleep(5)

        # Get all betting info for the University of Cincinnati Bearcats
        # Football games the 2020 CFB season.
        print(
            "Get all betting info for the University of Cincinnati " +
            "Bearcats Football games the 2020 CFB season."
        )
        json_data = get_cfbd_betting_lines(
            api_key=cfbd_key,
            season=2020,
            team="Cincinnati"
        )
        print(json_data)
        time.sleep(5)

        # Get all betting info for Ohio Bobcats home games the 2020 CFB season.
        print(
            "Get all betting info for Ohio Bobcats " +
            "home games the 2020 CFB season."
        )
        json_data = get_cfbd_betting_lines(
            api_key=cfbd_key,
            season=2020,
            home_team="Ohio"
        )
        print(json_data)
        time.sleep(5)

        # Get all betting info for Ohio State Buckeyes
        # away games the 2020 CFB season.
        print(
            "Get all betting info for Ohio State Buckeyes " +
            "away games the 2020 CFB season."
        )
        json_data = get_cfbd_betting_lines(
            api_key=cfbd_key,
            season=2020,
            away_team="Ohio State"
        )
        print(json_data)
        time.sleep(5)

        # Get all betting info for Atlantic Coast Conference (ACC)
        # games the 2020 CFB season.
        print(
            "Get all betting info for Atlantic Coast Conference (ACC) " +
            "games the 2020 CFB season."
        )
        json_data = get_cfbd_betting_lines(
            api_key=cfbd_key,
            season=2020,
            conference="ACC"
        )
        print(json_data)
        time.sleep(5)

        # Get all available betting info for the 2020 CFB season.
        print("Get all available betting info for the 2020 CFB season.")
        json_data = get_cfbd_betting_lines(
            api_key=cfbd_key,
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call
        # as a Dictionary (read: JSON) object.
        print(
            "You can also tell this function to just return the API call " +
            "as a Dictionary (read: JSON) object."
        )
        json_data = get_cfbd_betting_lines(
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

        # Get all available betting info for the 2020 CFB season, in week 2.
        print(
            "Get all available betting info for the 2020 CFB season, " +
            "in week 2."
        )
        json_data = get_cfbd_betting_lines(
            season=2020,
            week=2
        )
        print(json_data)
        time.sleep(5)
        # Get all betting info for the 2020 CFB season,
        # in the postseason (bowls, playoffs, etc.).
        print(
            "Get all betting info for the 2020 CFB season, " +
            "in the postseason (bowls, playoffs, etc.)."
        )
        json_data = get_cfbd_betting_lines(
            season=2020,
            season_type="postseason"
        )
        print(json_data)
        time.sleep(5)

        # Get all betting info for University of Cincinnati
        # Bearcats Football games the 2020 CFB season.
        print(
            "Get all betting info for University of Cincinnati " +
            "Bearcats Football games the 2020 CFB season."
        )
        json_data = get_cfbd_betting_lines(
            season=2020,
            team="Cincinnati"
        )
        print(json_data)
        time.sleep(5)

        # Get all betting info for Ohio Bobcats home games the 2020 CFB season.
        print(
            "Get all betting info for Ohio Bobcats " +
            "home games the 2020 CFB season."
        )
        json_data = get_cfbd_betting_lines(
            season=2020,
            home_team="Ohio"
        )
        print(json_data)
        time.sleep(5)

        # Get all betting info for Ohio State Buckeyes
        # away games the 2020 CFB season.
        print(
            "Get all betting info for Ohio State Buckeyes " +
            "away games the 2020 CFB season."
        )
        json_data = get_cfbd_betting_lines(

            season=2020,
            away_team="Ohio State"
        )
        print(json_data)
        time.sleep(5)

        # Get all betting info for Atlantic Coast Conference (ACC)
        # games the 2020 CFB season.
        print(
            "Get all betting info for Atlantic Coast Conference (ACC) " +
            "games the 2020 CFB season."
        )
        json_data = get_cfbd_betting_lines(
            season=2020,
            conference="ACC"
        )
        print(json_data)
        time.sleep(5)

        # Get all available betting info for the 2020 CFB season.
        print("Get all available betting info for the 2020 CFB season.")
        json_data = get_cfbd_betting_lines(
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call
        # as a Dictionary (read: JSON) object.
        print(
            "You can also tell this function to just return the API call " +
            "as a Dictionary (read: JSON) object."
        )
        json_data = get_cfbd_betting_lines(
            season=2020,
            team="Cincinnati",
            return_as_dict=True
        )
        print(json_data)

    ```
    Returns
    ----------
    A pandas `DataFrame` object with college football betting data,
    or (if `return_as_dict` is set to `True`)
    a dictionary object with college football betting data.
    """

    # now = datetime.now()
    betting_df = pd.DataFrame()
    row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/lines?"

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

    # `home` to `home_team`
    if home is not None and home_team is not None and (home is not home_team):
        raise ValueError(
            "Inconsistent inputs for `home` and `home_team`."
            + "\nPlease use either `home` OR `home_team` "
            + "when calling this function"
        )
    elif home is not None:
        home_team = home

    # `away` to `away_team`
    if away is not None and away_team is not None and (away is not away_team):
        raise ValueError(
            "Inconsistent inputs for `away` and `away_team`."
            + "\nPlease use either `away` OR `away_team` "
            + "when calling this function"
        )
    elif away is not None:
        away_team = away

    del year, home, away

    # if game_id is not None and season is not None:
    #     warnings.warn(
    #         "If you are getting betting information for a single game, "
    #         + "only set `game_id` to the game ID, " +
    #         "and leave `season` as `NULL`."
    #     )

    if season_type == "regular" or season_type == "postseason":
        url += f"seasonType={season_type}"
    else:
        raise ValueError(
            '`season_type` must be set to either "regular" or "postseason".'
        )

    # if (game_id is None) and (season is None) and (week is not None):
    #     raise ValueError(
    #         "When setting a value for `week`, `season` cannot be null."
    #     )

    if (season is None) and (week is not None):
        raise ValueError(
            "When setting a value for `week`, `season` cannot be null."
        )

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

    # if game_id is not None:
    #     url += f"&gameId={game_id}"

    if season is not None:
        url += f"&year={season}"

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

    headers = {
        "Authorization": f"{real_api_key}", "accept": "application/json"
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

    for game in tqdm(json_data):
        gameId = game["id"]
        season = game["id"]
        seasonType = game["seasonType"]
        startDate = game["startDate"]
        homeTeam = game["homeTeam"]
        homeConference = game["homeConference"]
        homeScore = game["homeScore"]
        awayTeam = game["awayTeam"]
        awayConference = game["awayConference"]
        awayScore = game["awayScore"]

        for line in game["lines"]:
            row_df = pd.DataFrame(
                {
                    "game_id": gameId,
                    "season": season,
                    "season_type": seasonType,
                    "start_date": startDate,
                    "home_team_name": homeTeam,
                    "home_conference_name": homeConference,
                    "home_score": homeScore,
                    "away_team_name": awayTeam,
                    "away_conference_name": awayConference,
                    "away_score": awayScore,
                },
                index=[0],
            )

            row_df["line_provider"] = line["provider"]
            row_df["spread"] = line["spread"]
            row_df["formatted_spread"] = line["formattedSpread"]
            row_df["spread_open"] = line["spreadOpen"]
            row_df["over_under"] = line["overUnder"]
            row_df["over_under_open"] = line["overUnderOpen"]
            row_df["home_moneyline"] = line["homeMoneyline"]
            row_df["away_moneyline"] = line["awayMoneyline"]

            betting_df = pd.concat([betting_df, row_df], ignore_index=True)
            del row_df

        del (
            gameId,
            seasonType,
            startDate,
            homeTeam,
            homeConference,
            homeScore,
            awayTeam,
            awayConference,
            awayScore,
        )

    return betting_df
