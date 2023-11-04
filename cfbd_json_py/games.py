# Creation Date: 08/30/2023 01:13 EDT
# Last Updated Date: 11/04/2023 02:55 PM EDT
# Author: Joseph Armstrong (armstrongjoseph08@gmail.com)
# File Name: games.py
# Purpose: Houses functions pertaining to CFB game data within the CFBD API.
####################################################################################################

from datetime import datetime
import logging

import pandas as pd
import requests
from tqdm import tqdm

from cfbd_json_py.utls import get_cfbd_api_token


def get_cfbd_games(
        season: int,
        api_key: str = None,
        api_key_dir: str = None,
        season_type: str = "regular",
        week: int = None,
        team: str = None,
        home_team: str = None,
        away_team: str = None,
        conference_abv: str = None,
        ncaa_division: str = "fbs",
        game_id: int = None,
        return_as_dict: bool = False):
    """
    Retrives game schedule data from the CFBD API.

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

    `season_type` (str, semi-optional):
        Semi-optional argument.
        By defualt, this will be set to "regular", for the CFB regular season.
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

    `conference_abv` (str, optional):
        Optional argument.
        If you only want game information from games 
        involving teams a specific confrence, 
        set `conference_abv` to the abbreviation 
        of the conference you want game information from.

    `ncaa_division` (str, semi-optional):
        Semi-optional argument.
        By default, `ncaa_division` will be set to "fbs", 
        short for the Football Bowl Subdivision (FBS), 
        formerly known as D1-A (read as "division one single A"),
        the highest level in the NCAA football pyramid,
        where teams can scolarship up to 85 players 
        on their football team soley for athletic ability, 
        and often have the largest athletics budgets
        within the NCAA.

        Other valid inputs are:
        - "fcs": Football Championship Subdivision (FCS), 
            formerly known as D1-AA (read as "division one double A").
            An FCS school is still in the 1st division of the NCAA,
            making them elligable for the March Madness tournament,
            but may not have the resources to compete at the FBS level
            at this time. FCS schools are limited to 63 athletic scolarships
            for football.
        - "ii": NCAA Division II. Schools in this and D3 are not
            elligable for the March Madness tournament, 
            and are limited to 36 athletic scolarships for their football team.
        - "iii": NCAA Division III. The largest single division within the 
            NCAA football pyramid. 
            D3 schools have the distinction of being part of 
            the only NCAA division that cannot give out scolarships soley 
            for athletic ability.

    `game_id` (int, optional):
        Optional argument. 
        If `game_id` is set to a game ID, `get_cfb_betting_lines()` will try to get 
        game information just for that game ID.

    `return_as_dict` (bool, semi-optional):
        Semi-optional argument.
        If you want this function to return the data as a dictionary (read: JSON object), 
        instead of a pandas `DataFrame` object,
        set `return_as_dict` to `True`.

    Usage
    ----------
    ```
    import time

    from cfbd_json_py.games import get_cfbd_games


    cfbd_key = "tigersAreAwsome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwsome":
        print("Using the user's API key declared in this script for this example.")

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

        # Get CFB games from the 2019 CFB season that involved the 2019 LSU Tigers.
        print("Get CFB games from the 2019 CFB season that involved the 2019 LSU Tigers.")
        json_data = get_cfbd_games(
            api_key=cfbd_key,
            season=2019,
            team="LSU"
        )
        print(json_data)
        time.sleep(5)

        # Get 2021 Cincinnati Bearcats Football games where the Bearcats were the home team.
        print("Get 2021 Cincinnati Bearcats Football games where the Bearcats were the home team.")
        json_data = get_cfbd_games(
            api_key=cfbd_key,
            season=2021,
            home_team="Cincinnati"
        )
        print(json_data)
        time.sleep(5)

        # Get 2018 Ohio Bobcats Football games where the Bobcats were the away team.
        print("Get 2018 Ohio Bobcats Football games where the Bobcats were the away team.")
        json_data = get_cfbd_games(
            api_key=cfbd_key,
            season=2019,
            away_team="Ohio"
        )
        print(json_data)
        time.sleep(5)

        # Get 2018 Ohio Bobcats Football games where the Bobcats were the away team.
        print("Get 2018 Ohio Bobcats Football games where the Bobcats were the away team.")
        json_data = get_cfbd_games(
            api_key=cfbd_key,
            season=2018,
            away_team="Ohio"
        )
        print(json_data)
        time.sleep(5)

        # Get 2022 college football games where one or more teams competing
        # was a Football Championship Subdivision team.
        print("Get 2022 college football games where one or more teams competing was a Football Championship Subdivision team.")
        json_data = get_cfbd_games(
            api_key=cfbd_key,
            season=2018,
            away_team="Ohio"
        )
        print(json_data)
        time.sleep(5)

        # Get game information for the
        # 2021 American Athletic Confrence (AAC) Championship Game.
        print("Get game information for the 2021 American Athletic Confrence (AAC) Championship Game.")
        json_data = get_cfbd_games(
            api_key=cfbd_key,
            season=2018,
            game_id=401331162
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
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
        # you could just call these functions directly, without setting the API key
        # in the script.
        print("Using the user's API key suposedly loaded into this python environment for this example.")

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

        # Get CFB games from the 2019 CFB season that involved the 2019 LSU Tigers.
        print("Get CFB games from the 2019 CFB season that involved the 2019 LSU Tigers.")
        json_data = get_cfbd_games(
            season=2019,
            team="LSU"
        )
        print(json_data)
        time.sleep(5)

        # Get 2021 Cincinnati Bearcats Football games where the Bearcats were the home team.
        print("Get 2021 Cincinnati Bearcats Football games where the Bearcats were the home team.")
        json_data = get_cfbd_games(
            season=2021,
            home_team="Cincinnati"
        )
        print(json_data)
        time.sleep(5)

        # Get 2018 Ohio Bobcats Football games where the Bobcats were the away team.
        print("Get 2018 Ohio Bobcats Football games where the Bobcats were the away team.")
        json_data = get_cfbd_games(
            season=2019,
            away_team="Ohio"
        )
        print(json_data)
        time.sleep(5)

        # Get 2018 Ohio Bobcats Football games where the Bobcats were the away team.
        print("Get 2018 Ohio Bobcats Football games where the Bobcats were the away team.")
        json_data = get_cfbd_games(
            season=2018,
            away_team="Ohio"
        )
        print(json_data)
        time.sleep(5)

        # Get 2022 college football games where one or more teams competing
        # was a Football Championship Subdivision team.
        print("Get 2022 college football games where one or more teams competing was a Football Championship Subdivision team.")
        json_data = get_cfbd_games(
            season=2018,
            away_team="Ohio"
        )
        print(json_data)
        time.sleep(5)

        # Get game information for the
        # 2021 American Athletic Confrence (AAC) Championship Game.
        print("Get game information for the 2021 American Athletic Confrence (AAC) Championship Game.")
        json_data = get_cfbd_games(
            season=2018,
            game_id=401331162
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
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
    row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/games"

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

    if season == None:
        # This should never happen without user tampering, but if it does,
        # we need to raise an error, because the CFBD API will refuse this call without a valid season.
        raise SystemError(
            "I don't know how, I don't know why, but you managed to call this function while `season` was `None` (NULL)," +
            " and the function got to this point in the code." +
            "\nIf you have a GitHub account, please raise an issue on this python package's GitHub page:\n" +
            "https://github.com/armstjc/cfbd-json-py/issues"
        )
    elif season > (now.year + 1):
        raise ValueError(f"`season` cannot be greater than {season}.")
    elif season < 1869:
        raise ValueError(f"`season` cannot be less than 1869.")

    if season_type != "regular" and season_type != "postseason":
        raise ValueError(
            "`season_type` must be set to either \"regular\" or \"postseason\" for this function to work.")

    if ncaa_division.lower() == "fbs" or ncaa_division.lower() == "fcs" \
            or ncaa_division.lower() == "ii" or ncaa_division.lower() == "iii":
        pass
    else:
        raise ValueError(
            "An invalid NCAA Division was inputted when calling this function." +
            "\nValid inputs are:\n-\"fbs\"\n-\"fcs\"\n-\"ii\"\n-\"iii\"" +
            f"\n\nYou entered: \n{ncaa_division}"
        )

    # URL builder
    ########################################################################################################################################################################################################

    # Required by API
    url += f"?seasonType={season_type}"

    if game_id != None:
        url += f"&year={season}"
        url += f"&id={game_id}"

        if team != None or home_team != None \
                or away_team != None or conference_abv != None \
                or week != None:
            logging.warning(
                "When calling `cfbd_json_py.games.get_cfbd_games()`, " +
                "and setting `game_id` to a non-null value, " +
                "only `season` and `game_id` are considered " +
                "when calling the CFBD API."
            )

    else:
        url += f"&year={season}"

        # Optional for the API
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

        if ncaa_division != None:
            url += f"&division={ncaa_division}"

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
        g_id = game['id']
        row_df = pd.DataFrame(
            {
                "game_id": g_id
            }, index=[0]
        )
        del g_id

        row_df['season'] = game['season']
        row_df['week'] = game['week']
        row_df['season_type'] = game['season_type']
        row_df['start_date'] = game['start_date']
        row_df['start_time_tbd'] = game['start_time_tbd']
        row_df['is_game_completed'] = game['completed']
        row_df['is_neutral_site'] = game['neutral_site']
        row_df['is_conference_game'] = game['conference_game']
        row_df['game_attendance'] = game['attendance']
        row_df['venue_id'] = game['venue_id']
        row_df['venue_name'] = game['venue']
        row_df['home_id'] = game['home_id']
        row_df['home_team'] = game['home_team']
        row_df['home_conference'] = game['home_conference']
        row_df['home_division'] = game['home_division']
        row_df['home_points'] = game['home_points']
        row_df['home_line_scores'] = str(game['home_line_scores'])
        row_df['home_post_win_prob'] = game['home_post_win_prob']
        row_df['home_pregame_elo'] = game['home_pregame_elo']
        row_df['home_postgame_elo'] = game['home_postgame_elo']
        row_df['away_id'] = game['away_id']
        row_df['away_team'] = game['away_team']
        row_df['away_conference'] = game['away_conference']
        row_df['away_division'] = game['away_division']
        row_df['away_points'] = game['away_points']
        row_df['away_line_scores'] = str(game['away_line_scores'])
        row_df['away_post_win_prob'] = game['away_post_win_prob']
        row_df['away_pregame_elo'] = game['away_pregame_elo']
        row_df['away_postgame_elo'] = game['away_postgame_elo']
        row_df['excitement_index'] = game['excitement_index']
        row_df['highlights'] = game['highlights']
        row_df['notes'] = game['notes']

        cfb_games_df = pd.concat([cfb_games_df, row_df], ignore_index=True)
        del row_df

    if len(cfb_games_df) == 0:
        logging.error(
            "The CFBD API accepted your inputs, " +
            "but found no data within your specified input paramaters." +
            " Please double check your input paramaters."
        )

    return cfb_games_df


def get_cfbd_team_records(
        api_key: str = None,
        api_key_dir: str = None,
        season: int = None,
        team: str = None,  # Must specify either a year or team
        conference_abv: str = None,
        return_as_dict: bool = False):
    """
    Get a team, or multiple team's record (wins, losses, ties) for home games, away games, 
    confrence games, and the team's record for that season.

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
        Specifies the season you want CFB team records data from.
        You MUST set `season` or `team` to a non-null value for 
        this function to work. If you don't, a `ValueError()` 
        will be raised.

    `team` (str, optional):
        Semi-ptional argument.
        If you only want CFB team records data for a specific team,
        set `team` to the name of the team you want CFB drive data from.
        You MUST set `season` or `team` to a non-null value for 
        this function to work. If you don't, a `ValueError()` 
        will be raised.

    `conference_abv` (str, optional):
        Optional argument.
        If you only want CFB team records data from games 
        involving teams from a specific confrence, 
        set `conference_abv` to the abbreviation 
        of the conference you want CFB team records data from.
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

    from cfbd_json_py.games import get_cfbd_team_records


    cfbd_key = "tigersAreAwsome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwsome":
        print("Using the user's API key declared in this script for this example.")

        # Get CFB team records from the 2020 CFB season.
        print("Get CFB team records from the 2020 CFB season.")
        json_data = get_cfbd_team_records(
            api_key=cfbd_key,
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get team records from football teams fielded by the University of Cincinnati.
        print("Get team records from football teams fielded by the University of Cincinnati.")
        json_data = get_cfbd_team_records(
            api_key=cfbd_key,
            team="Cincinnati"
        )
        print(json_data)
        time.sleep(5)

        # Get team records from football teams that played in the Big 10 (B1G) Confrence
        # in the 2017 CFB season
        print("Get team records from football teams that played in the Big 10 (B1G) Confrence in the 2017 CFB season")
        json_data = get_cfbd_team_records(
            api_key=cfbd_key,
            season=2017,
            conference_abv="B1G"
        )
        print(json_data)
        time.sleep(5)


        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_team_records(
            season=2020,
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

        # Get CFB team records from the 2020 CFB season.
        print("Get CFB team records from the 2020 CFB season.")
        json_data = get_cfbd_team_records(
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get team records from football teams fielded by the University of Cincinnati.
        print("Get team records from football teams fielded by the University of Cincinnati.")
        json_data = get_cfbd_team_records(
            team="Cincinnati"
        )
        print(json_data)
        time.sleep(5)

        # Get team records from football teams that played in the Big 10 (B1G) Confrence
        # in the 2017 CFB season
        print("Get team records from football teams that played in the Big 10 (B1G) Confrence in the 2017 CFB season")
        json_data = get_cfbd_team_records(
            season=2017,
            conference_abv="B1G"
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
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
    row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/records"

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

    if season != None and season > now.year:
        raise ValueError(f"`season` cannot be greater than {season}.")
    elif season != None and season < 1869:
        raise ValueError(f"`season` cannot be less than 1869.")

    if season == None and team == None:
        raise ValueError(
            f"If you call `cfbd_json_py.games.get_cfbd_team_records()`, you must specifiy at least a team or CFB season.")

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

    if conference_abv != None and url_elements == 0:
        url += f"?conference={conference_abv}"
        url_elements += 1
    elif conference_abv != None:
        url += f"&conference={conference_abv}"
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

    for team in json_data:
        team_year = team['year']
        row_df = pd.DataFrame(
            {"season": team_year},
            index=[0]
        )
        row_df['team_id'] = team['teamId']
        row_df['team_name'] = team['team']
        row_df['conference_name'] = team['conference']
        if team['division'] == "" or team['division'] == None:
            row_df['conference_division'] = None
        else:
            row_df['conference_division'] = team['division']

        row_df['expected_wins'] = team['expectedWins']
        row_df['total_games'] = team['total']['games']
        row_df['total_wins'] = team['total']['wins']
        row_df['total_losses'] = team['total']['losses']
        row_df['total_ties'] = team['total']['ties']
        row_df['conference_games'] = team['conferenceGames']['games']
        row_df['conference_wins'] = team['conferenceGames']['wins']
        row_df['conference_losses'] = team['conferenceGames']['losses']
        row_df['conference_ties'] = team['conferenceGames']['ties']
        row_df['home_games'] = team['homeGames']['games']
        row_df['home_wins'] = team['homeGames']['wins']
        row_df['home_losses'] = team['homeGames']['losses']
        row_df['home_ties'] = team['homeGames']['ties']
        row_df['away_games'] = team['awayGames']['games']
        row_df['away_wins'] = team['awayGames']['wins']
        row_df['away_losses'] = team['awayGames']['losses']
        row_df['away_ties'] = team['awayGames']['ties']

        cfb_records_df = pd.concat([cfb_records_df, row_df], ignore_index=True)
        del row_df

    return cfb_records_df


def get_cfbd_season_weeks(
        season: int,
        api_key: str = None,
        api_key_dir: str = None,
        return_as_dict: bool = False):
    """
    Retrives a list of weeks that occured in a given CFB season.

    Parameters
    ----------
    `season` (int, mandatory):
        Required argument.
        Specifies the season you want a list of weeks that occured in a given CFB season information from.
        This must be specified, otherwise this package, and by extension
        the CFBD API, will not accept the request to get a list of weeks that occured in a given CFB season information.

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

    from cfbd_json_py.games import get_cfbd_season_weeks


    cfbd_key = "tigersAreAwsome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwsome":
        print("Using the user's API key declared in this script for this example.")

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
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_season_weeks(
            season=2020,
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

        # Get a list of weeks in the 2020 CFB season.
        print("Get a list of weeks in the 2020 CFB season.")
        json_data = get_cfbd_season_weeks(
            season=2020
        )
        print(json_data)
        time.sleep(5)


        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_season_weeks(
            season=2020,
            return_as_dict=True
        )
        print(json_data)

    ```

    Returns
    ----------
    A pandas `DataFrame` object with a list of valid weeks in a given CFB season, 
    or (if `return_as_dict` is set to `True`)
    a dictionary object with a list of valid weeks in a given CFB season.


    """

    now = datetime.now()
    cfb_weeks_df = pd.DataFrame()
    row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/calendar"

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

    if season == None:
        # This should never happen without user tampering, but if it does,
        # we need to raise an error, because the CFBD API will refuse this call without a valid season.
        raise SystemError(
            "I don't know how, I don't know why, but you managed to call this function while `season` was `None` (NULL)," +
            " and the function got to this point in the code." +
            "\nIf you have a GitHub account, please raise an issue on this python package's GitHub page:\n" +
            "https://github.com/armstjc/cfbd-json-py/issues"
        )
    elif season > (now.year + 1):
        raise ValueError(f"`season` cannot be greater than {season}.")
    elif season < 1869:
        raise ValueError(f"`season` cannot be less than 1869.")

    # URL builder
    ########################################################################################################################################################################################################

    # Required by API
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

    for week in json_data:
        row_df = pd.DataFrame(
            {"season": season},
            index=[0]
        )
        row_df['week'] = week['week']
        row_df['season_type'] = week['seasonType']
        row_df['first_game_start'] = week['firstGameStart']
        row_df['last_game_start'] = week['lastGameStart']

        cfb_weeks_df = pd.concat([cfb_weeks_df, row_df], ignore_index=True)
        del row_df

    return cfb_weeks_df


def get_cfbd_game_media_info(
        season: int,
        api_key: str = None,
        api_key_dir: str = None,
        season_type: str = "regular",  # "regular", "postseason", or "both"
        week: int = None,
        team: str = None,
        conference_abv: str = None,
        media_type: str = "all",  # "tv", "radio", "web", "ppv", or "mobile"
        ncaa_division: str = "fbs",
        return_as_dict: bool = False):
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

    `season_type` (str, semi-optional):
        Semi-optional argument.
        By defualt, this will be set to "regular", for the CFB regular season.
        If you want CFB media information for non-regular season games, 
        set `season_type` to "postseason".
        If you want both "regular" and "postseason" games retunred, 
        set `season_type` to "both"
        If `season_type` is set to anything but "regular" or "postseason", 
        a `ValueError()` will be raised.

    `week` (int, optional):
        Optional argument.
        If `week` is set to an integer, this function will attempt 
        to load CFB media information from games in that season, and in that week.

    `team` (str, optional):
        Optional argument.
        If you only want CFB media information for a team, 
        regardless if they are the home/away team,
        set `team` to the name of the team you want CFB media information from.

    `conference_abv` (str, optional):
        Optional argument.
        If you only want media information from games 
        involving teams a specific confrence, 
        set `conference_abv` to the abbreviation 
        of the conference you want game information from.

    `media_type` (str, semi-optional):
        Semi-optional argument.
        If you only want game broadcast information for a specific type of broadcast,
        set this to the type of broadcast.

        Valid inputs are: 
        - `all` (default): Returns all games, and all known broadcasters for those games.
        - `tv`: Returns all known TV broadcasters for CFB games in the requested timeframe.
        - `radio`: Returns all known radio broadcasters 
            for CFB games in the requested timeframe.
        - `web`: Returns all known web broadcasts (like ESPN+) 
            for CFB games in the requested timeframe.
        - `ppv`: Returns all known Pay Per View (PPV) broadcasts 
            for CFB games in the requested timeframe.
        - `mobile`: Returns all known broadcasters that only broadcasted 
            games on mobile devices (?)

    `ncaa_division` (str, semi-optional):
        Semi-optional argument.
        By default, `ncaa_division` will be set to "fbs", 
        short for the Football Bowl Subdivision (FBS), 
        formerly known as D1-A (read as "division one single A"),
        the highest level in the NCAA football pyramid,
        where teams can scolarship up to 85 players 
        on their football team soley for athletic ability, 
        and often have the largest athletics budgets
        within the NCAA.

        Other valid inputs are:
        - "fcs": Football Championship Subdivision (FCS), 
            formerly known as D1-AA (read as "division one double A").
            An FCS school is still in the 1st division of the NCAA,
            making them elligable for the March Madness tournament,
            but may not have the resources to compete at the FBS level
            at this time. FCS schools are limited to 63 athletic scolarships
            for football.
        - "ii": NCAA Division II. Schools in this and D3 are not
            elligable for the March Madness tournament, 
            and are limited to 36 athletic scolarships for their football team.
        - "iii": NCAA Division III. The largest single division within the 
            NCAA football pyramid. 
            D3 schools have the distinction of being part of 
            the only NCAA division that cannot give out scolarships soley 
            for athletic ability.

    `return_as_dict` (bool, semi-optional):
        Semi-optional argument.
        If you want this function to return the data as a dictionary (read: JSON object), 
        instead of a pandas `DataFrame` object,
        set `return_as_dict` to `True`.

    Usage
    ----------
    ```
    import time

    from cfbd_json_py.games import get_cfbd_game_media_info


    cfbd_key = "tigersAreAwsome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwsome":
        print("Using the user's API key declared in this script for this example.")

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
        print("Get a media information for week 10 games in the 2020 CFB season.")
        json_data = get_cfbd_game_media_info(
            api_key=cfbd_key,
            season=2020,
            week=10
        )
        print(json_data)
        time.sleep(5)

        # Get all known broadcasters for games played by the Ohio State Football Program in the the 2019 CFB season.
        print("Get all known broadcasters for games played by the Ohio State Football Program in the the 2019 CFB season.")
        json_data = get_cfbd_game_media_info(
            api_key=cfbd_key,
            season=2020,
            team="Ohio State"
        )
        print(json_data)
        time.sleep(5)

        # Get all known radio broadcasters for games played by teams within the American Athletic Confrence (AAC) in the the 2021 CFB season.
        print("Get all known radio broadcasters for games played by teams within the American Athletic Confrence (AAC) in the the 2021 CFB season.")
        json_data = get_cfbd_game_media_info(
            api_key=cfbd_key,
            season=2020,
            conference_abv="AAC"
        )
        print(json_data)
        time.sleep(5)

        # Get all known radio broadcasters for games in the the 2020 CFB season.
        print("Get all known radio broadcasters for games in the the 2020 CFB season.")
        json_data = get_cfbd_game_media_info(
            api_key=cfbd_key,
            season=2020,
            media_type="radio"
        )
        print(json_data)
        time.sleep(5)

        # Get all known broadcasters for Football Championship Subdivision (FCS) games in the 2020 CFB season.
        print("Get all known broadcasters for Football Championship Subdivision (FCS) games in the 2020 CFB season.")
        json_data = get_cfbd_game_media_info(
            api_key=cfbd_key,
            season=2020,
            ncaa_division="fcs"
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_game_media_info(
            season=2020,
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
        print("Get a media information for week 10 games in the 2020 CFB season.")
        json_data = get_cfbd_game_media_info(
            season=2020,
            week=10
        )
        print(json_data)
        time.sleep(5)

        # Get all known broadcasters for games played by the Ohio State Football Program in the the 2019 CFB season.
        print("Get all known broadcasters for games played by the Ohio State Football Program in the the 2019 CFB season.")
        json_data = get_cfbd_game_media_info(
            season=2020,
            team="Ohio State"
        )
        print(json_data)
        time.sleep(5)

        # Get all known radio broadcasters for games played by teams within the American Athletic Confrence (AAC) in the the 2021 CFB season.
        print("Get all known radio broadcasters for games played by teams within the American Athletic Confrence (AAC) in the the 2021 CFB season.")
        json_data = get_cfbd_game_media_info(
            season=2020,
            conference_abv="AAC"
        )
        print(json_data)
        time.sleep(5)

        # Get all known radio broadcasters for games in the the 2020 CFB season.
        print("Get all known radio broadcasters for games in the the 2020 CFB season.")
        json_data = get_cfbd_game_media_info(
            season=2020,
            media_type="radio"
        )
        print(json_data)
        time.sleep(5)

        # Get all known broadcasters for Football Championship Subdivision (FCS) games in the 2020 CFB season.
        print("Get all known broadcasters for Football Championship Subdivision (FCS) games in the 2020 CFB season.")
        json_data = get_cfbd_game_media_info(
            season=2020,
            ncaa_division="fcs"
        )
        print(json_data)
        time.sleep(5)


        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
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
    row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/games/media"

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

    if season == None:
        # This should never happen without user tampering, but if it does,
        # we need to raise an error, because the CFBD API will refuse this call without a valid season.
        raise SystemError(
            "I don't know how, I don't know why, but you managed to call this function while `season` was `None` (NULL)," +
            " and the function got to this point in the code." +
            "\nIf you have a GitHub account, please raise an issue on this python package's GitHub page:\n" +
            "https://github.com/armstjc/cfbd-json-py/issues"
        )
    elif season > (now.year + 1):
        raise ValueError(f"`season` cannot be greater than {season}.")
    elif season < 1869:
        raise ValueError(f"`season` cannot be less than 1869.")

    if season_type != "both" and season_type != "regular" and season_type != "postseason":
        raise ValueError(
            "`season_type` must be set to \"both\", \"regular\", or \"postseason\" for this function to work.")

    if media_type != "all" and media_type != "tv" and media_type != "radio" and media_type != "web" and media_type != "ppv" and media_type != "mobile":
        raise ValueError(
            "`media_type` must be set to one of the following values for this function to work:" +
            "\n\t- `all`" +
            "\n\t- `tv`" +
            "\n\t- `radio`" +
            "\n\t- `web`" +
            "\n\t- `ppv`" +
            "\n\t- `mobile`"
        )

    if ncaa_division.lower() == "fbs" or ncaa_division.lower() == "fcs" \
            or ncaa_division.lower() == "ii" or ncaa_division.lower() == "iii":
        pass
    else:
        raise ValueError(
            "An invalid NCAA Division was inputted when calling this function." +
            "\nValid inputs are:\n-\"fbs\"\n-\"fcs\"\n-\"ii\"\n-\"iii\"" +
            f"\n\nYou entered: \n{ncaa_division}"
        )

    # URL builder
    ########################################################################################################################################################################################################

    # Required by API
    url += f"?year={season}"

    if week != None:
        url += f"&week={week}"

    if team != None:
        url += f"&team={team}"

    if conference_abv != None:
        url += f"&conference={conference_abv}"

    if season_type != None:
        url += f"&seasonType={season_type}"

    if media_type == "all":
        # If we don't care about what media type we want back,
        # we don't need to add anything to the URL.
        pass
    elif media_type != None:
        url += f"&mediaType={media_type}"

    if ncaa_division != None:
        url += f"&classification={ncaa_division}"

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
        row_df = pd.DataFrame(
            {"season": season},
            index=[0]
        )
        row_df['week'] = game['week']
        row_df['game_id'] = game['id']
        row_df['season_type'] = game['seasonType']
        row_df['game_start_time'] = game['startTime']
        row_df['is_start_time_tbd'] = game['isStartTimeTBD']
        row_df['home_team'] = game['homeTeam']
        row_df['home_conference'] = game['homeConference']
        row_df['away_team'] = game['awayTeam']
        row_df['away_conference'] = game['awayConference']
        row_df['media_type'] = game['mediaType']
        row_df['outlet'] = game['outlet']

        cfb_games_df = pd.concat([cfb_games_df, row_df], ignore_index=True)
        del row_df

    return cfb_games_df


def get_cfbd_player_game_stats(
        season: int,
        api_key: str = None,
        api_key_dir: str = None,
        season_type: str = "regular",  # "regular" or "postseason"
        week: int = None,
        team: str = None,
        conference_abv: str = None,
        # `week`, `team`, and/or `conference`
        # must be not null for this function to work.
        stat_category: str = None,
        game_id: int = None,
        return_as_dict: bool = False):
    """
    Retrives player game stats for a given time frame.

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

    `season_type` (str, semi-optional):
        Semi-optional argument.
        By defualt, this will be set to "regular", for the CFB regular season.
        If you want CFB player game stats for non-regular season games, 
        set `season_type` to "postseason".
        If `season_type` is set to anything but "regular" or "postseason", 
        a `ValueError()` will be raised.

    **For the following three variables, 
    at least one must be set to a non-null variable when calling this function.**

    `week` (int, optional):
        Optional argument.
        If `week` is set to an integer, this function will attempt 
        to load CFB player game stats from games in that season, and in that week.

    `team` (str, optional):
        Optional argument.
        If you only want CFB player game stats for a team, 
        regardless if they are the home/away team,
        set `team` to the name of the team you want CFB player game stats from.

    `conference_abv` (str, optional):
        Optional argument.
        If you only want player game stats from games 
        involving teams a specific confrence, 
        set `conference_abv` to the abbreviation 
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
        If `game_id` is set to a game ID, `get_cfbd_player_game_stats()` will try to get 
        player game stats just for that game ID.

    `return_as_dict` (bool, semi-optional):
        Semi-optional argument.
        If you want this function to return the data as a dictionary (read: JSON object), 
        instead of a pandas `DataFrame` object,
        set `return_as_dict` to `True`.

    Usage
    ----------
    ```
    import time

    from cfbd_json_py.games import get_cfbd_player_game_stats


    cfbd_key = "tigersAreAwsome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwsome":
        print("Using the user's API key declared in this script for this example.")

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

        # Get player game stats for the Alabma Crimson Tide Football Team for the 2018 CFB season.
        print("Get player game stats for the Alabma Crimson Tide Football Team for the 2018 CFB season.")
        json_data = get_cfbd_player_game_stats(
            api_key=cfbd_key,
            season=2018,
            team="Alabama"
        )
        print(json_data)
        time.sleep(5)
        
        # Get player game stats for players of teams in the Atlantic Coast Conference (ACC) in the 2020 CFB season.
        print("Get player game stats for players of teams in the Atlantic Coast Conference (ACC) in the 2020 CFB season.")
        json_data = get_cfbd_player_game_stats(
            api_key=cfbd_key,
            season=2020,
            conference_abv="ACC"
        )
        print(json_data)
        time.sleep(5)

        # Get get passing stats from players who played in week 7 of the 2017 CFB season.
        print("Get get passing stats from players who played in week 7 of the 2017 CFB season.")
        json_data = get_cfbd_player_game_stats(
            api_key=cfbd_key,
            season=2017,
            week=7,
            stat_category="pasing"
        )
        print(json_data)
        time.sleep(5)

        # Get player game stats from the 2021 Virbo Citrus Bowl, 
        # a bowl game that happened in the 2020 CFB season.
        print("Get player game stats from the 2021 Virbo Citrus Bowl, a bowl game that happened in the 2020 CFB season.")
        json_data = get_cfbd_player_game_stats(
            api_key=cfbd_key,
            season=2020,
            game_id=401256199
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
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
        # you could just call these functions directly, without setting the API key
        # in the script.
        print("Using the user's API key suposedly loaded into this python environment for this example.")

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

        # Get player game stats for the Alabma Crimson Tide Football Team for the 2018 CFB season.
        print("Get player game stats for the Alabma Crimson Tide Football Team for the 2018 CFB season.")
        json_data = get_cfbd_player_game_stats(
            season=2018,
            team="Alabama"
        )
        print(json_data)
        time.sleep(5)
        
        # Get player game stats for players of teams in the Atlantic Coast Conference (ACC) in the 2020 CFB season.
        print("Get player game stats for players of teams in the Atlantic Coast Conference (ACC) in the 2020 CFB season.")
        json_data = get_cfbd_player_game_stats(
            season=2020,
            conference_abv="ACC"
        )
        print(json_data)
        time.sleep(5)

        # Get get passing stats from players who played in week 7 of the 2017 CFB season.
        print("Get get passing stats from players who played in week 7 of the 2017 CFB season.")
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
            "a bowl game that happened in the 2020 CFB season between the Aubrun Tigers, and the Northwestern Wildcats.")
        json_data = get_cfbd_player_game_stats(
            season=2020,
            game_id=401256199
        )
        print(json_data)
        time.sleep(5)


        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
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
    
    rebuilt_json = {}
    now = datetime.now()
    cfb_games_df = pd.DataFrame()
    row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/games/players"
    stat_columns = [
        'season',
        'game_id',
        'team_name',
        'team_confrence',
        'player_id',
        'player_name',
        'home_away',
        # PASS
        'passing_C/ATT',
        'passing_COMP',
        'passing_ATT',
        'passing_YDS',
        'passing_AVG',
        'passing_TD',
        'passing_INT',
        'passing_QBR',
        # RUSH
        'rushing_CAR',
        'rushing_YDS',
        'rushing_AVG',
        'rushing_TD',
        'rushing_LONG',
        # REC
        'receiving_REC',
        'receiving_YDS',
        'receiving_AVG',
        'receiving_TD',
        'receiving_LONG',
        # FUM
        'fumbles_FUM',
        'fumbles_LOST',
        'fumbles_REC',
        # DEFENSE
        'defensive_TOT',
        'defensive_SOLO',
        'defensive_TFL',
        'defensive_QB HUR',
        'defensive_SACKS',
        'defensive_PD',
        'defensive_TD',
        # INT
        'interceptions_INT',
        'interceptions_YDS',
        'interceptions_TD',
        # PUNT
        'punting_NO',
        'punting_YDS',
        'punting_AVG',
        'punting_TB',
        'punting_In 20',
        'punting_LONG',
        # KICK
        'kicking_FG',
        'kicking_FGM',
        'kicking_FGA',
        'kicking_PCT',
        'kicking_LONG',
        'kicking_XP',
        'kicking_XPM',
        'kicking_XPA',
        'kicking_PTS',
        # KR
        'kickReturns_NO',
        'kickReturns_YDS',
        'kickReturns_AVG',
        'kickReturns_TD',
        'kickReturns_LONG',
        # PR
        'puntReturns_NO',
        'puntReturns_YDS',
        'puntReturns_AVG',
        'puntReturns_TD',
        'puntReturns_LONG'
    ]

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

    if season == None:
        # This should never happen without user tampering, but if it does,
        # we need to raise an error, because the CFBD API will refuse this call without a valid season.
        raise SystemError(
            "I don't know how, I don't know why, " +
            "but you managed to call this function while `season` was `None` (NULL)," +
            " and the function got to this point in the code." +
            "\nIf you have a GitHub account, " +
            "please raise an issue on this python package's GitHub page:\n" +
            "https://github.com/armstjc/cfbd-json-py/issues"
        )
    elif season > (now.year + 1):
        raise ValueError(f"`season` cannot be greater than {season}.")
    elif season < 1869:
        raise ValueError(f"`season` cannot be less than 1869.")

    if season_type != "regular" and season_type != "postseason":
        raise ValueError(
            "`season_type` must be set to either \"regular\" or " +
            "\"postseason\" for this function to work."
        )

    # `week`, `team`, and/or `conference`
    # must be not null for this function to work.

    if week == None and team == None and conference_abv == None and game_id == None:
        raise ValueError(
            "To use `get_cfbd_player_game_stats()`," +
            " `week`, `team`, and/or `conference_abv` need to be set to a non-null value."
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
            "Invalid input for `stat_category`." +
            "\nValid inputs are:" +
            """
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
    ########################################################################################################################################################################################################

    # Required by the API
    url += f"?year={season}"

    if game_id != None:
        url += f"&gameId={game_id}"

        if stat_category != None:
            url += f"&category={stat_category}"

        if week != None or team != None or conference_abv != None:
            logging.warning(
                "When calling `cfbd_json_py.games.get_cfbd_player_game_stats()`, " +
                "and setting `game_id` to a non-null value, " +
                "only `season`, `stat_category`, and `game_id` are considered " +
                "when calling the CFBD API."
            )
    else:
        if season_type != None:
            url += f"&seasonType={season_type}"

        if week != None:
            url += f"&week={week}"

        if team != None:
            url += f"&team={team}"

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
        game_id = game['id']

        for team in game['teams']:
            team_name = team['school']
            team_confrence = team['conference']
            home_away = team['homeAway']

            for s_category in team['categories']:
                if s_category['name'] == "passing":
                    for stat in s_category['types']:

                        if stat['name'] == "C/ATT":  # passing_C/ATT

                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = i['stat']

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['passing_C/ATT'] = player_stat

                        elif stat['name'] == "YDS":  # passing_YDS

                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = int(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['passing_YDS'] = player_stat

                        elif stat['name'] == "AVG":  # passing_AVG
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = float(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['passing_AVG'] = player_stat

                        elif stat['name'] == "TD":  # passing_TD

                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = int(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['passing_TD'] = player_stat

                        elif stat['name'] == "INT":  # passing_INT

                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = int(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['passing_INT'] = player_stat

                        elif stat['name'] == "QBR":  # passing_QBR
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                try:
                                    player_stat = float(i['stat'])
                                except:
                                    player_stat = None

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['passing_QBR'] = player_stat

                        else:
                            raise IndexError(
                                f"Unhandled stat: \t{stat['name']}")
                    # passing_df = pd.DataFrame(s_category['types'])
                elif s_category['name'] == "rushing":
                    for stat in s_category['types']:
                        if stat['name'] == "CAR":  # rushing_CAR
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = int(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['rushing_CAR'] = player_stat

                        elif stat['name'] == "YDS":  # rushing_YDS
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = int(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['rushing_YDS'] = player_stat

                        elif stat['name'] == "AVG":  # rushing_AVG
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = float(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['rushing_AVG'] = player_stat

                        elif stat['name'] == "TD":  # rushing_TD
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = int(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['rushing_TD'] = player_stat

                        elif stat['name'] == "LONG":  # rushing_LONG
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = int(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['rushing_LONG'] = player_stat

                        else:
                            raise IndexError(
                                f"Unhandled stat: \t{stat['name']}")

                elif s_category['name'] == "receiving":
                    for stat in s_category['types']:
                        if stat['name'] == "REC":  # receiving_REC
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = int(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['receiving_REC'] = player_stat

                        elif stat['name'] == "YDS":  # receiving_YDS
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = int(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['receiving_YDS'] = player_stat

                        elif stat['name'] == "AVG":  # receiving_AVG
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = float(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['receiving_AVG'] = player_stat

                        elif stat['name'] == "TD":  # receiving_TD
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = int(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['receiving_TD'] = player_stat

                        elif stat['name'] == "LONG":  # receiving_LONG
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = int(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['receiving_LONG'] = player_stat

                        else:
                            raise IndexError(
                                f"Unhandled stat: \t{stat['name']}")

                elif s_category['name'] == "fumbles":
                    for stat in s_category['types']:
                        if stat['name'] == "FUM":  # fumbles_FUM
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = int(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['fumbles_FUM'] = player_stat

                        elif stat['name'] == "LOST":  # fumbles_LOST
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = int(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['fumbles_LOST'] = player_stat

                        elif stat['name'] == "REC":  # fumbles_REC
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = int(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['fumbles_REC'] = player_stat

                        else:
                            raise IndexError(
                                f"Unhandled stat: \t{stat['name']}")

                elif s_category['name'] == "defensive":
                    for stat in s_category['types']:
                        if stat['name'] == "TOT":  # defensive_TOT
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = int(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['defensive_TOT'] = player_stat

                        elif stat['name'] == "SOLO":  # defensive_SOLO
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = int(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['defensive_SOLO'] = player_stat

                        elif stat['name'] == "TFL":  # defensive_TFL
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = float(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['defensive_TFL'] = player_stat

                        elif stat['name'] == "QB HUR":  # defensive_QB HUR
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = int(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['defensive_QB HUR'] = player_stat

                        elif stat['name'] == "SACKS":  # defensive_SACKS
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = float(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['defensive_SACKS'] = player_stat

                        elif stat['name'] == "PD":  # defensive_PD
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = int(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['defensive_PD'] = player_stat

                        elif stat['name'] == "TD":  # defensive_TD
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = int(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['defensive_TD'] = player_stat

                        else:
                            raise IndexError(
                                f"Unhandled stat: \t{stat['name']}")

                elif s_category['name'] == "interceptions":
                    for stat in s_category['types']:
                        if stat['name'] == "INT":  # interceptions_INT
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = int(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['interceptions_INT'] = player_stat

                        elif stat['name'] == "YDS":  # interceptions_YDS
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = int(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['interceptions_YDS'] = player_stat

                        elif stat['name'] == "TD":  # interceptions_TD
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = int(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['interceptions_TD'] = player_stat

                        else:
                            raise IndexError(
                                f"Unhandled stat: \t{stat['name']}")

                elif s_category['name'] == "punting":
                    for stat in s_category['types']:
                        if stat['name'] == "NO":  # punting_NO
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = int(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['punting_NO'] = player_stat

                        elif stat['name'] == "YDS":  # punting_YDS
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = int(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['punting_YDS'] = player_stat

                        elif stat['name'] == "AVG":  # punting_AVG
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = float(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['punting_AVG'] = player_stat

                        elif stat['name'] == "TB":  # punting_TB
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = int(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['punting_TB'] = player_stat

                        elif stat['name'] == "In 20":  # punting_In 20
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = int(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['punting_In 20'] = player_stat

                        elif stat['name'] == "LONG":  # punting_LONG
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = int(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['punting_LONG'] = player_stat

                        else:
                            raise IndexError(
                                f"Unhandled stat: \t{stat['name']}")

                elif s_category['name'] == "kicking":
                    for stat in s_category['types']:
                        if stat['name'] == "FG":  # kicking_FG
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = i['stat']

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['kicking_FG'] = player_stat

                        elif stat['name'] == "TOT":  # kicking_FG, special case
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = i['stat']

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['kicking_FG'] = player_stat

                        elif stat['name'] == "PCT":  # kicking_PCT
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = float(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['kicking_PCT'] = player_stat

                        elif stat['name'] == "LONG":  # kicking_LONG
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = int(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['kicking_LONG'] = player_stat

                        elif stat['name'] == "XP":  # kicking_XP
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = i['stat']

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['kicking_XP'] = player_stat

                        elif stat['name'] == "PTS":  # kicking_PTS
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = int(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['kicking_PTS'] = player_stat

                        else:
                            raise IndexError(
                                f"Unhandled stat: \t{stat['name']}")

                elif s_category['name'] == "kickReturns":
                    for stat in s_category['types']:
                        if stat['name'] == "NO":  # kickReturns_NO
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = int(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['kickReturns_NO'] = player_stat

                        elif stat['name'] == "YDS":  # kickReturns_YDS
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = int(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['kickReturns_YDS'] = player_stat

                        elif stat['name'] == "AVG":  # kickReturns_AVG
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = float(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['kickReturns_AVG'] = player_stat

                        elif stat['name'] == "TD":  # kickReturns_TD
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = int(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['kickReturns_TD'] = player_stat

                        elif stat['name'] == "LONG":  # kickReturns_LONG
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = int(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['kickReturns_LONG'] = player_stat

                        else:
                            raise IndexError(
                                f"Unhandled stat: \t{stat['name']}")

                elif s_category['name'] == "puntReturns":
                    for stat in s_category['types']:
                        if stat['name'] == "NO":  # puntReturns_NO
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = int(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['puntReturns_NO'] = player_stat

                        elif stat['name'] == "YDS":  # puntReturns_YDS
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = int(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['puntReturns_YDS'] = player_stat

                        elif stat['name'] == "AVG":  # puntReturns_AVG
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = float(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['puntReturns_AVG'] = player_stat

                        elif stat['name'] == "TD":  # puntReturns_TD
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = int(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['puntReturns_TD'] = player_stat

                        elif stat['name'] == "LONG":  # puntReturns_LONG
                            for i in stat['athletes']:
                                player_id = int(i['id'])
                                player_name = i['name']
                                player_stat = int(i['stat'])

                                if rebuilt_json.get(player_id) == None:
                                    rebuilt_json[player_id] = {}

                                rebuilt_json[player_id]['game_id'] = game_id
                                rebuilt_json[player_id]['team_name'] = team_name
                                rebuilt_json[player_id]['team_confrence'] = team_confrence
                                rebuilt_json[player_id]['player_id'] = player_id
                                rebuilt_json[player_id]['player_name'] = player_name
                                rebuilt_json[player_id]['home_away'] = home_away
                                rebuilt_json[player_id]['puntReturns_LONG'] = player_stat

                        else:
                            raise IndexError(
                                f"Unhandled stat: \t{stat['name']}")

                else:
                    raise IndexError(
                        f"Unhandled stat category: \t{s_category['name']}"
                    )

    for key, value in tqdm(rebuilt_json.items()):
        # print(key)

        # print(value)
        game_id = value['game_id']
        team_name = value['team_name']
        team_confrence = value['team_confrence']
        player_id = value['player_id']
        player_name = value['player_name']
        home_away = value['home_away']

        row_df = pd.DataFrame(
            {
                "game_id": game_id,
                "team_name": team_name,
                "team_confrence": team_confrence,
                "player_id": player_id,
                "player_name": player_name,
                "home_away": home_away
            },
            index=[0]
        )
        # Passing
        if value.get('passing_C/ATT') != None:
            row_df['passing_C/ATT'] = value['passing_C/ATT']

        if value.get('passing_YDS') != None:
            row_df['passing_YDS'] = value['passing_YDS']

        if value.get('passing_AVG') != None:
            row_df['passing_AVG'] = value['passing_AVG']

        if value.get('passing_TD') != None:
            row_df['passing_TD'] = value['passing_TD']

        if value.get('passing_INT') != None:
            row_df['passing_INT'] = value['passing_INT']

        if value.get('passing_QBR') != None:
            row_df['passing_QBR'] = value['passing_QBR']

        # Rushing
        if value.get('rushing_CAR') != None:
            row_df['rushing_CAR'] = value['rushing_CAR']

        if value.get('rushing_YDS') != None:
            row_df['rushing_YDS'] = value['rushing_YDS']

        if value.get('rushing_AVG') != None:
            row_df['rushing_AVG'] = value['rushing_AVG']

        if value.get('rushing_TD') != None:
            row_df['rushing_TD'] = value['rushing_TD']

        if value.get('rushing_LONG') != None:
            row_df['rushing_LONG'] = value['rushing_LONG']

        # Receiving
        if value.get('receiving_REC') != None:
            row_df['receiving_REC'] = value['receiving_REC']

        if value.get('receiving_YDS') != None:
            row_df['receiving_YDS'] = value['receiving_YDS']

        if value.get('receiving_AVG') != None:
            row_df['receiving_AVG'] = value['receiving_AVG']

        if value.get('receiving_TD') != None:
            row_df['receiving_TD'] = value['receiving_TD']

        if value.get('receiving_LONG') != None:
            row_df['receiving_LONG'] = value['receiving_LONG']

        # Fumbles
        if value.get('fumbles_FUM') != None:
            row_df['fumbles_FUM'] = value['fumbles_FUM']

        if value.get('fumbles_LOST') != None:
            row_df['fumbles_LOST'] = value['fumbles_LOST']

        if value.get('fumbles_REC') != None:
            row_df['fumbles_REC'] = value['fumbles_REC']

        # Defense
        if value.get('defensive_TOT') != None:
            row_df['defensive_TOT'] = value['defensive_TOT']

        if value.get('defensive_SOLO') != None:
            row_df['defensive_SOLO'] = value['defensive_SOLO']

        if value.get('defensive_TFL') != None:
            row_df['defensive_TFL'] = value['defensive_TFL']

        if value.get('defensive_QB HUR') != None:
            row_df['defensive_QB HUR'] = value['defensive_QB HUR']

        if value.get('defensive_SACKS') != None:
            row_df['defensive_SACKS'] = value['defensive_SACKS']

        if value.get('defensive_PD') != None:
            row_df['defensive_PD'] = value['defensive_PD']

        if value.get('defensive_TD') != None:
            row_df['defensive_TD'] = value['defensive_TD']

        # interceptions
        if value.get('interceptions_INT') != None:
            row_df['interceptions_INT'] = value['interceptions_INT']

        if value.get('interceptions_YDS') != None:
            row_df['interceptions_YDS'] = value['interceptions_YDS']

        if value.get('interceptions_TD') != None:
            row_df['interceptions_TD'] = value['interceptions_TD']

        # punting
        if value.get('punting_NO') != None:
            row_df['punting_NO'] = value['punting_NO']

        if value.get('punting_YDS') != None:
            row_df['punting_YDS'] = value['punting_YDS']

        if value.get('punting_AVG') != None:
            row_df['punting_AVG'] = value['punting_AVG']

        if value.get('punting_TB') != None:
            row_df['punting_TB'] = value['punting_TB']

        if value.get('punting_In 20') != None:
            row_df['punting_In 20'] = value['punting_In 20']

        if value.get('punting_LONG') != None:
            row_df['punting_LONG'] = value['punting_LONG']

        # kicking
        if value.get('kicking_FG') != None:
            row_df['kicking_FG'] = value['kicking_FG']

        if value.get('kicking_PCT') != None:
            row_df['kicking_PCT'] = value['kicking_PCT']

        if value.get('kicking_LONG') != None:
            row_df['kicking_LONG'] = value['kicking_LONG']

        if value.get('kicking_XP') != None:
            row_df['kicking_XP'] = value['kicking_XP']

        if value.get('kicking_PTS') != None:
            row_df['kicking_PTS'] = value['kicking_PTS']

        # kickReturns
        if value.get('kickReturns_NO') != None:
            row_df['kickReturns_NO'] = value['kickReturns_NO']

        if value.get('kickReturns_YDS') != None:
            row_df['kickReturns_YDS'] = value['kickReturns_YDS']

        if value.get('kickReturns_AVG') != None:
            row_df['kickReturns_AVG'] = value['kickReturns_AVG']

        if value.get('kickReturns_TD') != None:
            row_df['kickReturns_TD'] = value['kickReturns_TD']

        if value.get('kickReturns_LONG') != None:
            row_df['kickReturns_LONG'] = value['kickReturns_LONG']

        # puntReturns
        if value.get('puntReturns_NO') != None:
            row_df['puntReturns_NO'] = value['puntReturns_NO']

        if value.get('puntReturns_YDS') != None:
            row_df['puntReturns_YDS'] = value['puntReturns_YDS']

        if value.get('puntReturns_AVG') != None:
            row_df['puntReturns_AVG'] = value['puntReturns_AVG']

        if value.get('puntReturns_TD') != None:
            row_df['puntReturns_TD'] = value['puntReturns_TD']

        if value.get('puntReturns_LONG') != None:
            row_df['puntReturns_LONG'] = value['puntReturns_LONG']

        cfb_games_df = pd.concat([cfb_games_df, row_df], ignore_index=True)
        del row_df

    cfb_games_df[['passing_COMP', 'passing_ATT']
                 ] = cfb_games_df['passing_C/ATT'].str.split('/', expand=True)

    cfb_games_df[['kicking_FGM', 'kicking_FGA']
                 ] = cfb_games_df['kicking_FG'].str.split('/', expand=True)
    cfb_games_df[['kicking_XPM', 'kicking_XPA']
                 ] = cfb_games_df['kicking_XP'].str.split('/', expand=True)
    
    cfb_games_df = cfb_games_df.fillna(0)

    cfb_games_df = cfb_games_df.astype({
        "passing_COMP": "int",
        "passing_ATT": "int",
        "kicking_FGM": "int",
        "kicking_FGA": "int",
        "kicking_XPM": "int",
        "kicking_XPA": "int"
    })
    # print(cfb_games_df.columns)
    cfb_games_df['season'] = season

    if filter_by_stat_category == False:
        cfb_games_df = cfb_games_df.reindex(columns=stat_columns)

    elif filter_by_stat_category == True and stat_category == "passing":
        cfb_games_df = cfb_games_df[[
            'season',
            'game_id',
            'team_name',
            'team_confrence',
            'player_id',
            'player_name',
            'home_away',
            # PASS
            'passing_C/ATT',
            'passing_COMP',
            'passing_ATT',
            'passing_YDS',
            'passing_AVG',
            'passing_TD',
            'passing_INT',
            'passing_QBR'
        ]]

    elif filter_by_stat_category == True and stat_category == "rushing":
        cfb_games_df = cfb_games_df[[
            'season',
            'game_id',
            'team_name',
            'team_confrence',
            'player_id',
            'player_name',
            'home_away',
            # RUSH
            'rushing_CAR',
            'rushing_YDS',
            'rushing_AVG',
            'rushing_TD',
            'rushing_LONG',
        ]]

    elif filter_by_stat_category == True and stat_category == "receiving":
        cfb_games_df = cfb_games_df[[
            'season',
            'game_id',
            'team_name',
            'team_confrence',
            'player_id',
            'player_name',
            'home_away',
            # REC
            'receiving_REC',
            'receiving_YDS',
            'receiving_AVG',
            'receiving_TD',
            'receiving_LONG'
        ]]

    elif filter_by_stat_category == True and stat_category == "fumbles":
        cfb_games_df = cfb_games_df[[
            'season',
            'game_id',
            'team_name',
            'team_confrence',
            'player_id',
            'player_name',
            'home_away',
            # FUM
            'fumbles_FUM',
            'fumbles_LOST',
            'fumbles_REC'
        ]]

    elif filter_by_stat_category == True and stat_category == "defensive":
        cfb_games_df = cfb_games_df[[
            'season',
            'game_id',
            'team_name',
            'team_confrence',
            'player_id',
            'player_name',
            'home_away',
            # DEFENSE
            'defensive_TOT',
            'defensive_SOLO',
            'defensive_TFL',
            'defensive_QB HUR',
            'defensive_SACKS',
            'defensive_PD',
            'defensive_TD'
        ]]

    elif filter_by_stat_category == True and stat_category == "interceptions":
        cfb_games_df = cfb_games_df[[
            'season',
            'game_id',
            'team_name',
            'team_confrence',
            'player_id',
            'player_name',
            'home_away',
            # INT
            'interceptions_INT',
            'interceptions_YDS',
            'interceptions_TD',
        ]]

    elif filter_by_stat_category == True and stat_category == "punting":
        cfb_games_df = cfb_games_df[[
            'season',
            'game_id',
            'team_name',
            'team_confrence',
            'player_id',
            'player_name',
            'home_away',
            # PUNT
            'punting_NO',
            'punting_YDS',
            'punting_AVG',
            'punting_TB',
            'punting_In 20',
            'punting_LONG'
        ]]

    elif filter_by_stat_category == True and stat_category == "kicking":
        cfb_games_df = cfb_games_df[[
            'season',
            'game_id',
            'team_name',
            'team_confrence',
            'player_id',
            'player_name',
            'home_away',
            # KICK
            'kicking_FG',
            'kicking_FGM',
            'kicking_FGA',
            'kicking_PCT',
            'kicking_LONG',
            'kicking_XP',
            'kicking_XPM',
            'kicking_XPA',
            'kicking_PTS'
        ]]

    elif filter_by_stat_category == True and stat_category == "kickReturns":
        cfb_games_df = cfb_games_df[[
            'season',
            'game_id',
            'team_name',
            'team_confrence',
            'player_id',
            'player_name',
            'home_away',
            # KR
            'kickReturns_NO',
            'kickReturns_YDS',
            'kickReturns_AVG',
            'kickReturns_TD',
            'kickReturns_LONG'
        ]]

    elif filter_by_stat_category == True and stat_category == "puntReturns":
        cfb_games_df = cfb_games_df[[
            'season',
            'game_id',
            'team_name',
            'team_confrence',
            'player_id',
            'player_name',
            'home_away',
            # KR
            'puntReturns_NO',
            'puntReturns_YDS',
            'puntReturns_AVG',
            'puntReturns_TD',
            'puntReturns_LONG'
        ]]

    return cfb_games_df


def get_cfbd_player_advanced_game_stats(
        game_id: int,
        api_key: str = None,
        api_key_dir: str = None,
        return_as_dict: bool = False):
    """
    Retrives advanced game stats from the CFBD API.

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

    from cfbd_json_py.games import get_cfbd_player_advanced_game_stats


    cfbd_key = "tigersAreAwsome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwsome":
        print("Using the user's API key declared in this script for this example.")

        # Get advanced player stats for a 2019 CFB game between the LSU Tigers Football Program, 
        # and the Oklahoma Sooners Football Program.
        print("Get advanced player stats for a 2019 CFB game between the LSU Tigers Football Program, and the Oklahoma Sooners Football Program.")
        json_data = get_cfbd_player_advanced_game_stats(
            api_key=cfbd_key,
            game_id=401135278
        )
        print(json_data)
        time.sleep(5)


        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_player_advanced_game_stats(
            api_key=cfbd_key,
            game_id=401135278,
            return_as_dict=True
        )
        print(json_data)

    else:
        # Alternatively, if the CFBD API key exists in this python environment,
        # or it's been set by cfbd_json_py.utls.set_cfbd_api_token(),
        # you could just call these functions directly, without setting the API key
        # in the script.
        print("Using the user's API key suposedly loaded into this python environment for this example.")

        # Get advanced player stats for a 2019 CFB game between the LSU Tigers Football Program, 
        # and the Oklahoma Sooners Football Program.
        print("Get advanced player stats for a 2019 CFB game between the LSU Tigers Football Program, and the Oklahoma Sooners Football Program.")
        json_data = get_cfbd_player_advanced_game_stats(
            game_id=401135278
        )
        print(json_data)
        time.sleep(5)


        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
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

    #now = datetime.now()
    usage_df = pd.DataFrame()
    ppa_df = pd.DataFrame()
    adv_stats_df = pd.DataFrame()
    row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/game/box/advanced"

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

    # Required by API
    url += f"?gameId={game_id}"

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

    home_team_name = json_data['gameInfo']['homeTeam']
    home_points = json_data['gameInfo']['homePoints']
    home_win_prob = json_data['gameInfo']['homeWinProb']
    away_team_name = json_data['gameInfo']['awayTeam']
    away_points = json_data['gameInfo']['awayPoints']
    away_win_prob = json_data['gameInfo']['awayWinProb']
    home_winner = json_data['gameInfo']['homeWinner']
    game_excitement_score = json_data['gameInfo']['excitement']
    
    
    # Parsing Usage
    print("Parsing player usage data.")
    for player in tqdm(json_data['players']['usage']):
        row_df = pd.DataFrame(
            {
                "game_id":game_id
            },
            index=[0]
        )
        row_df['player_name'] = player['player']
        row_df['team'] = player['team']
        row_df['position'] = player['position']

        row_df['total_usage'] = player['total']
        row_df['q1_usage'] = player['quarter1']
        row_df['q2_usage'] = player['quarter2']
        row_df['q3_usage'] = player['quarter3']
        row_df['q4_usage'] = player['quarter4']
        row_df['rushing_usage'] = player['rushing']
        row_df['passing_usage'] = player['passing']

        usage_df = pd.concat([usage_df,row_df],ignore_index=True)
        del row_df

    # Parsing PPA
    print("Parsing player PPA data.")
    for player in tqdm(json_data['players']['ppa']):
        row_df = pd.DataFrame(
            {
                "game_id":game_id
            },
            index=[0]
        )
        row_df['player_name'] = player['player']
        row_df['team'] = player['team']
        row_df['position'] = player['position']
        
        row_df['average_ppa_total'] = player['average']['total']
        row_df['average_ppa_q1'] = player['average']['quarter1']
        row_df['average_ppa_q2'] = player['average']['quarter2']
        row_df['average_ppa_q3'] = player['average']['quarter3']
        row_df['average_ppa_q4'] = player['average']['quarter4']
        row_df['average_ppa_rushing'] = player['average']['rushing']
        row_df['average_ppa_passing'] = player['average']['passing']
        
        row_df['cumulative_ppa_total'] = player['cumulative']['total']
        row_df['cumulative_ppa_q1'] = player['cumulative']['quarter1']
        row_df['cumulative_ppa_q2'] = player['cumulative']['quarter2']
        row_df['cumulative_ppa_q3'] = player['cumulative']['quarter3']
        row_df['cumulative_ppa_q4'] = player['cumulative']['quarter4']
        row_df['cumulative_ppa_rushing'] = player['cumulative']['rushing']
        row_df['cumulative_ppa_passing'] = player['cumulative']['passing']
        
        ppa_df = pd.concat([ppa_df,row_df],ignore_index=True)

    # Join `usage_df` and `ppa_df` together
    adv_stats_df = pd.merge(
        left=usage_df,
        right=ppa_df,
        how="outer",
        on=["game_id","player_name","team","position"]
    )

    # Add in these columns for completeness.

    adv_stats_df.loc[adv_stats_df["team"]==home_team_name,"home_away"] = "home"
    adv_stats_df.loc[adv_stats_df["team"]==home_team_name,"opponent"] = away_team_name
    
    adv_stats_df.loc[adv_stats_df["team"]==away_team_name,"home_away"] = "away"
    adv_stats_df.loc[adv_stats_df["team"]==away_team_name,"opponent"] = home_team_name
    
    adv_stats_df['home_team'] = home_team_name
    adv_stats_df['away_team'] = away_team_name

    adv_stats_df['home_win_prob'] = home_win_prob
    adv_stats_df['away_win_prob'] = away_win_prob

    adv_stats_df['home_points'] = home_points
    adv_stats_df['away_points'] = away_points

    adv_stats_df['home_winner'] = home_winner
    adv_stats_df['game_excitement_score'] = game_excitement_score

    return adv_stats_df


####################################################################################################
# Patreon Only Functions.
#   No cacheing, because the entire point of these functions are to get people
#   data ASAP, and right before kickoff.
####################################################################################################


def get_cfbd_live_scoreboard(
        api_key: str = None,
        api_key_dir: str = None,
        ncaa_division: str = "fbs",
        conference: str = None):
    """
    YOU MUST BE SUBSCRIBED TO THE CFBD PATREON FOR THIS FUNCTION TO WORK!
    To view the CFBD Patreon, visit https://www.patreon.com/collegefootballdata


    """

    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )


def get_cfbd_weather_info(
        api_key: str = None,
        api_key_dir: str = None,
        ncaa_division: str = "fbs",
        game_id: int = None,
        # `game_id` and/or `year` must be not null for this function to work.
        season: int = None,
        week: int = None,
        season_type: str = "regular",  # "regular", "postseason", or "both"
        conference: str = None):
    """
    YOU MUST BE SUBSCRIBED TO THE CFBD PATREON FOR THIS FUNCTION TO WORK!
    To view the CFBD Patreon, visit https://www.patreon.com/collegefootballdata
    """

    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )
