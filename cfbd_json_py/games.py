# Creation Date: 08/30/2023 01:13 EDT
# Last Updated Date: 10/06/2023 07:53 PM EDT
# Author: Joseph Armstrong (armstrongjoseph08@gmail.com)
# File Name: games.py
# Purpose: Houses functions pertaining to CFB game data within the CFBD API.
####################################################################################################

from datetime import datetime
import logging
import time

import pandas as pd
import requests

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
        If `api_key` is set to a string non-empty string, this variable is ignored.
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
    elif season > now.year:
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
            f"\n\nYou entered:\n{ncaa_division}"
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
                or ncaa_division != None or week != None:
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
            url += f"&year={season}"

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
    time.sleep(0.1)

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

    for game in json_data:
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
        row_df['home_line_scores'] = game['home_line_scores']
        row_df['home_post_win_prob'] = game['home_post_win_prob']
        row_df['home_pregame_elo'] = game['home_pregame_elo']
        row_df['home_postgame_elo'] = game['home_postgame_elo']
        row_df['away_id'] = game['away_id']
        row_df['away_team'] = game['away_team']
        row_df['away_conference'] = game['away_conference']
        row_df['away_division'] = game['away_division']
        row_df['away_points'] = game['away_points']
        row_df['away_line_scores'] = game['away_line_scores']
        row_df['away_post_win_prob'] = game['away_post_win_prob']
        row_df['away_pregame_elo'] = game['away_pregame_elo']
        row_df['away_postgame_elo'] = game['away_postgame_elo']
        row_df['excitement_index'] = game['excitement_index']
        row_df['highlights'] = game['highlights']
        row_df['notes'] = game['notes']

        cfb_games_df = pd.DataFrame([cfb_games_df, row_df], ignore_index=True)
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

    """

    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )


def get_cfbd_season_weeks(
        season: int,
        api_key: str = None,
        api_key_dir: str = None,
        return_as_dict: bool = False):
    """

    """

    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )


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

    """

    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )


def get_cfbd_player_game_stats(
        season: int,
        api_key: str = None,
        api_key_dir: str = None,
        season_type: str = "regular",  # "regular" or "postseason"
        week: int = None,
        team: str = None,
        conference_abv: str = None,
        # `week`, `team`, and/or conference
        # must be not null for this function to work.
        stat_category: str = None,
        game_id: int = None,
        return_as_dict: bool = False):
    """

    """

    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )


def get_cfbd_advanced_game_stats(
        game_id: int,
        api_key: str = None,
        api_key_dir: str = None,
        return_as_dict: bool = False):
    """
    """

    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )

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

    """

    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )
