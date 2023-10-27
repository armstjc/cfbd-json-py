# Creation Date: 08/30/2023 01:13 EDT
# Last Updated Date: 10/23/2023 04:09 PM EDT
# Author: Joseph Armstrong (armstrongjoseph08@gmail.com)
# File Name: betting.py
# Purpose: Houses functions pertaining to betting data within the CFBD API.
####################################################################################################

import warnings

import pandas as pd
import requests
from tqdm import tqdm

from cfbd_json_py.utls import get_cfbd_api_token


def get_cfbd_betting_lines(
        season: int,
        api_key: str = None,
        api_key_dir: str = None,
        game_id: int = None,
        week: int = None,
        season_type: str = "regular",  # "regular" or "postseason"
        team: str = None,
        home_team: str = None,
        away_team: str = None,
        conference_abv: str = None,
        # cache_data: bool = False,
        # cache_dir: str = None,
        return_as_dict: bool = False):
    """
    Retrives betting information from the CFBD API for a given season, 
    or you could only get betting information for a single game.

    Parameters
    ----------

    `season` (int, mandatory):
        The season you want to retrive betting information from.

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

    `game_id` (int, optional):
        Optional argument. 
        If `game_id` is set to a game ID, `get_cfb_betting_lines()` will try to get 
        all betting informaiton for that game ID.

    `week` (int, optional):
        Optional argument.
        If `week` is set to an integer, this function will attempt 
        to load betting data from games in that season, and that week.

    `season_type` (str, semi-optional):
        Semi-optional argument.
        By defualt, this will be set to "regular", for the CFB regular season.
        If you want postseason betting data, set `season_type` to "postseason".
        If `season_type` is set to anything but "regular" or "postseason", 
        a `ValueError()` will be raised.

    `team` (str, optional):
        Optional argument.
        If you only want betting information for a team, 
        regardless if they are the home/away team,
        set `team` to the name of the team you want game-level betting data from.

    `home_team` (str, optional):
        Optional argument.
        If you only want betting information for a team, 
        where that team was the home team in this season,
        set `home_team` to the name of the team you want game-level betting data from.

    `away_team` (str, optional):
        Optional argument.
        If you only want betting information for a team, 
        where that team was the away team in this season,
        set `away_team` to the name of the team you want game-level betting data from.

    `conference_abv` (str, optional):
        Optional argument.
        If you only want betting information from games 
        involving teams a specific confrence, 
        set `conference_abv` to the abbreviation 
        of the conference you want betting informaiton from.

    `return_as_dict` (bool, semi-optional):
        Semi-optional argument.
        If you want this function to return the data as a dictionary (read: JSON object), 
        instead of a pandas `DataFrame` object,
        set `return_as_dict` to `True`.

    Usage
    ---------- 
    ```
    import time

    from cfbd_json_py.betting import get_cfbd_betting_lines

    cfbd_key = "tigersAreAwsome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwsome":
        print("Using the user's API key declared in this script for this example.")

        # Gets all available betting info for the 2020 CFB season.
        print("Gets all available betting info for the 2020 CFB season.")
        json_data = get_cfbd_betting_lines(
            api_key=cfbd_key,
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Gets all available betting info for the 2020 CFB season, in week 2.
        print("Gets all available betting info for the 2020 CFB season, in week 2.")
        json_data = get_cfbd_betting_lines(
            api_key=cfbd_key,
            season=2020,
            week=2
        )
        print(json_data)
        time.sleep(5)
        # Gets all betting info for the 2020 CFB season, in the postseason (bowls, playoffs, etc.).
        print("Gets all betting info for the 2020 CFB season, in the postseason (bowls, playoffs, etc.).")
        json_data = get_cfbd_betting_lines(
            api_key=cfbd_key,
            season=2020,
            season_type="postseason"
        )
        print(json_data)
        time.sleep(5)
        # Gets all betting info for Cincinnati Bearcats Football games the 2020 CFB season.
        print("Gets all betting info for Cincinnati Bearcats Football games the 2020 CFB season.")
        json_data = get_cfbd_betting_lines(
            api_key=cfbd_key,
            season=2020,
            team="Cincinnati"
        )
        print(json_data)
        time.sleep(5)
        # Gets all betting info for Ohio Bobcats home games the 2020 CFB season.
        print("Gets all betting info for Ohio Bobcats home games the 2020 CFB season.")
        json_data = get_cfbd_betting_lines(
            api_key=cfbd_key,
            season=2020,
            home_team="Ohio"
        )
        print(json_data)
        time.sleep(5)
        # Gets all betting info for Ohio State Buckeyes away games the 2020 CFB season.
        print("Gets all betting info for Ohio State Buckeyes away games the 2020 CFB season.")
        json_data = get_cfbd_betting_lines(
            api_key=cfbd_key,
            season=2020,
            away_team="Ohio State"
        )

        # Gets all betting info for Atlantic Coast Conference (ACC) games the 2020 CFB season.
        print("Gets all betting info for Atlantic Coast Conference (ACC) games the 2020 CFB season.")
        json_data = get_cfbd_betting_lines(
            api_key=cfbd_key,
            season=2020,
            conference_abv="ACC"
        )
        print(json_data)
        time.sleep(5)
        # You can also tell this function to just return the API call as a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_betting_lines(
            api_key=cfbd_key,
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

        # Gets all available betting info for the 2020 CFB season.
        print("Gets all available betting info for the 2020 CFB season.")
        json_data = get_cfbd_betting_lines(
            season=2020
        )
        print(json_data)
        time.sleep(5)
        # Gets all available betting info for the 2020 CFB season, in week 2.
        print("Gets all available betting info for the 2020 CFB season, in week 2.")
        json_data = get_cfbd_betting_lines(
            season=2020,
            week=2
        )
        print(json_data)
        time.sleep(5)
        # Gets all betting info for the 2020 CFB season, in the postseason (bowls, playoffs, etc.).
        print("Gets all betting info for the 2020 CFB season, in the postseason (bowls, playoffs, etc.).")
        json_data = get_cfbd_betting_lines(
            season=2020,
            season_type="postseason"
        )
        print(json_data)
        time.sleep(5)
        # Gets all betting info for Cincinnati Bearcats Football games the 2020 CFB season.
        print("Gets all betting info for Cincinnati Bearcats Football games the 2020 CFB season.")
        json_data = get_cfbd_betting_lines(
            season=2020,
            team="Cincinnati"
        )
        print(json_data)
        time.sleep(5)
        # Gets all betting info for Ohio Bobcats home games the 2020 CFB season.
        print("Gets all betting info for Ohio Bobcats home games the 2020 CFB season.")
        json_data = get_cfbd_betting_lines(
            season=2020,
            home_team="Ohio"
        )
        print(json_data)
        time.sleep(5)
        # Gets all betting info for Ohio State Buckeyes away games the 2020 CFB season.
        print("Gets all betting info for Ohio State Buckeyes away games the 2020 CFB season.")
        json_data = get_cfbd_betting_lines(

            season=2020,
            away_team="Ohio State"
        )

        # Gets all betting info for Atlantic Coast Conference (ACC) games the 2020 CFB season.
        print("Gets all betting info for Atlantic Coast Conference (ACC) games the 2020 CFB season.")
        json_data = get_cfbd_betting_lines(
            season=2020,
            conference_abv="ACC"
        )
        print(json_data)
        time.sleep(5)
        # You can also tell this function to just return the API call as a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_betting_lines(
            season=2020,
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
    ########################################################################################################################################################################################################
    if game_id != None and season != None:
        warnings.warn(
            "If you are getting betting information for a single game, only set `game_id` to the game ID, and leave `season` as `NULL`.")

    if season_type == "regular" or season_type == "postseason":
        url += f"seasonType={season_type}"
    else:
        raise ValueError(
            "`season_type` must be set to either \"regular\" or \"postseason\".")

    if (game_id == None) and (season == None) and (week != None):
        raise ValueError(
            "When setting a value for `week`, `season` cannot be null.")

    # if cache_data == True and ((team != None) or (home_team != None) or (away_team != None) or (conference_abv != None)):
    #     logging.warning(
    #         "When caching data is enabled for this function, the following inputs are ignored when making the API call:\n-`team`\n-`home_team`\n-`away_team`\n-`conference_abv`")

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

    if game_id != None:
        url += f"&gameId={game_id}"

    if season != None:
        url += f"&year={season}"

    if week != None:
        url += f"&week={week}"

    if team != None:
        url += f"&team={team}"

    if home_team != None:
        url += f"&home={home_team}"

    if away_team != None:
        url += f"&away={away_team}"

    if conference_abv != None:
        url += f"&conference={conference_abv}"

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

    for game in tqdm(json_data):
        gameId = game['id']
        season = game['id']
        seasonType = game['seasonType']
        startDate = game['startDate']
        homeTeam = game['homeTeam']
        homeConference = game['homeConference']
        homeScore = game['homeScore']
        awayTeam = game['awayTeam']
        awayConference = game['awayConference']
        awayScore = game['awayScore']

        for line in game['lines']:
            row_df = pd.DataFrame(
                {
                    "game_id": gameId,
                    "season": season,
                    "season_type": seasonType,
                    "start_date": startDate,
                    "home_team": homeTeam,
                    "home_conference": homeConference,
                    "home_score": homeScore,
                    "away_team": awayTeam,
                    "away_conference": awayConference,
                    "away_score": awayScore
                },
                index=[0]
            )

            row_df["line_provider"] = line['provider']
            row_df["spread"] = line['spread']
            row_df["formatted_spread"] = line['formattedSpread']
            row_df["spread_open"] = line['spreadOpen']
            row_df["over_under"] = line['overUnder']
            row_df["over_under_open"] = line['overUnderOpen']
            row_df["home_moneyline"] = line['homeMoneyline']
            row_df["away_moneyline"] = line['awayMoneyline']

            betting_df = pd.concat([betting_df, row_df], ignore_index=True)
            del row_df

        del gameId, seasonType, startDate, homeTeam, \
            homeConference, homeScore, awayTeam, \
            awayConference, awayScore

    return betting_df
