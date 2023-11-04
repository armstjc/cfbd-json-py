# Creation Date: 08/30/2023 01:13 EDT
# Last Updated Date: 11/04/2023 02:55 PM EDT
# Author: Joseph Armstrong (armstrongjoseph08@gmail.com)
# File Name: metrics.py
# Purpose: Houses functions pertaining to various CFB stats within the CFBD API.
####################################################################################################

from datetime import datetime
import logging
import pandas as pd
import requests
from tqdm import tqdm

from cfbd_json_py.utls import get_cfbd_api_token


def get_cfbd_predicted_ppa_from_down_distance(
        down: int,
        distance: int,
        api_key: str = None,
        api_key_dir: str = None,
        return_as_dict: bool = False):
    """
    Given a down and distance, 
    this function will attempt to get the predicted
    PPA value for that down and distance, 
    at every yard line possible for that down and distance.

    PPA is the CFBD API's equivalent metric to Expected Points Added (EPA).

    For this endpoint, 
    [`yardLine`] is the number of yards from 1 (offense has the ball on their side, 
    at their 1 yard line), to 99 
    (offense with the ball with a X and goal situation on the opponent's 1 yard line.

    Parameters
    ----------
    `down` (int, mandatory):
        Mandatory argument.
        This is the down (a number between 1 and 4 in normal situations)
        for this play you want PPA for.

    `distance` (int, mandatory):
        Mandatory argument.
        This variable should be set to the number of yards between 
        the line of scrimage (LOS), and the first down line on the field.

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

    from cfbd_json_py.metrics import get_cfbd_predicted_ppa_from_down_distance


    cfbd_key = "tigersAreAwsome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwsome":
        print("Using the user's API key declared in this script for this example.")

        # Get the predicted PPA for a 1st and 10 play, 
        # in every possible situation.
        print("Get the predicted PPA for a 1st and 10 play, in every possible situation.")
        json_data = get_cfbd_predicted_ppa_from_down_distance(
            down=1,
            distance=10,
            api_key=cfbd_key
        )
        print(json_data)
        time.sleep(5)


        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_predicted_ppa_from_down_distance(
            down=1,
            distance=10,
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


        # Get the predicted PPA for a 1st and 10 play, 
        # in every possible situation.
        print("Get the predicted PPA for a 1st and 10 play, in every possible situation.")
        json_data = get_cfbd_predicted_ppa_from_down_distance(
            down=1,
            distance=10
        )
        print(json_data)
        time.sleep(5)


        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_predicted_ppa_from_down_distance(
            down=1,
            distance=10,
            return_as_dict=True
        )
        print(json_data)

    ```
    Returns
    ----------
    A pandas `DataFrame` object with a calculated PPA from a dwon and distance, 
    or (if `return_as_dict` is set to `True`) 
    a dictionary object with a calculated PPA from a dwon and distance.


    """

    # now = datetime.now()
    ppa_df = pd.DataFrame()
    row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/ppa/predicted"

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

    if down >= 1 and down <= 4:
        # This is normal, so pass.
        pass
    elif down == 5:
        # Due to a Missouri-Colorado game in the 90s
        # being won by Colorado on a mythical "5th down",
        # we cannot reject this down outright,
        # but we have to convey to the person calling this
        # function that setting `down = 5`
        # is not something they should be doing.
        logging.warn(
            "There is a very limited number of \"5th down\" situations " +
            "in American Football history. " +
            "Do not expect anything back when calling this function, " +
            "and setting`down` to `5`."
        )
    else:
        raise ValueError(
            "Invalid `down` inputted! Valid inputs are:\n" +
            "\n\t- `1`" +
            "\n\t- `2`" +
            "\n\t- `3`" +
            "\n\t- `4`" +
            f"\nYou entered: \t`{down}`"


        )

    if distance == 0:
        raise ValueError(
            "If you want \"X and inches\" predicted PPA data, " +
            "set `down` to `1` when calling this function."
        )
    elif distance >= 100 and distance <= 110:
        raise ValueError(
            "The CFBD API cannot calculate predicted PPA for " +
            "U-Sports (Canada) football."
        )
    elif distance >= 1 and distance <= 99:
        # While numbers beyond 30 are rare,
        # there are some situations IRL that caused the distance
        # in "down and distance" to exceed 90
        # (most famously a 2017 game between
        # Mississippi State and Louisiana Tech).
        pass

    # URL builder
    ########################################################################################################################################################################################################

    # Required by API
    url += f"?down={down}&distance={distance}"

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

    for dnd in json_data:
        row_df = pd.DataFrame(
            {
                "down": down,
                "distance": distance,

            },
            index=[0]
        )
        row_df['predicted_points'] = dnd['predictedPoints']
        row_df['yard_line'] = dnd['yardLine']
        ppa_df = pd.concat([ppa_df, row_df], ignore_index=True)

    return ppa_df


def get_cfbd_team_season_ppa_data(
        api_key: str = None,
        api_key_dir: str = None,
        season: int = None,
        team: str = None,
        # `year` and/or `team` must be not null for this function to work.
        conference_abv: str = None,
        exclude_garbage_time: bool = False,
        return_as_dict: bool = False):
    """
    Allows you to get team PPA data, 
    over an entire season,
    with or without garbage time plays, 
    for a specificed team and/or time period.

    PPA is the CFBD API's equivalent metric to Expected Points Added (EPA).    

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

    `conference_abv` (str, optional):
        Optional argument.
        If you only want team PPA data from games 
        involving teams from a specific confrence, 
        set `conference_abv` to the abbreviation 
        of the conference you want team PPA data from.
        For a list of confrences, 
        use the `cfbd_json_py.conferences.get_cfbd_conference_info()`
        function.

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

    from cfbd_json_py.metrics import get_cfbd_team_ppa_data


    cfbd_key = "tigersAreAwsome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwsome":
        print("Using the user's API key declared in this script for this example.")

        # Get team season PPA data for the 2020 CFB season.
        print("Get team PPA data for the 2020 CFB season.")
        json_data = get_cfbd_team_ppa_data(
            api_key=cfbd_key,
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get team season PPA data for the 2020 Ohio State Buckeyes.
        print("Get team season PPA data for the 2020 Ohio State Buckeyes.")
        json_data = get_cfbd_team_ppa_data(
            api_key=cfbd_key,
            season=2020,
            team="Ohio State"
        )
        print(json_data)
        time.sleep(5)

        # Get team season PPA data for the 2020 Ohio State Buckeyes, 
        # but exclude garbage time plays when making the PPA calculations.
        print("Get team season PPA data for the 2020 Ohio State Buckeyes, but exclude garbage time plays when making the PPA calculations.")
        json_data = get_cfbd_team_ppa_data(
            api_key=cfbd_key,
            season=2020,
            team="Ohio State",
            exclude_garbage_time=True
        )
        print(json_data)
        time.sleep(5)

        # Get team season PPA data for teams in the Big 10 (B1G) Conference in the 2020 CFB Season.
        print("Get team season PPA data for teams in the Big 10 (B1G) Conference in the 2020 CFB Season.")
        json_data = get_cfbd_team_ppa_data(
            api_key=cfbd_key,
            season=2020,
            conference_abv="B1G"
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_team_ppa_data(
            api_key=cfbd_key,
            season=2020,
            conference_abv="B1G",
            return_as_dict=True
        )
        print(json_data)

    else:
        # Alternatively, if the CFBD API key exists in this python environment,
        # or it's been set by cfbd_json_py.utls.set_cfbd_api_token(),
        # you could just call these functions directly, without setting the API key
        # in the script.
        print("Using the user's API key suposedly loaded into this python environment for this example.")

        # Get team season PPA data for the 2020 CFB season.
        print("Get team PPA data for the 2020 CFB season.")
        json_data = get_cfbd_team_ppa_data(
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get team season PPA data for the 2020 Ohio State Buckeyes.
        print("Get team season PPA data for the 2020 Ohio State Buckeyes.")
        json_data = get_cfbd_team_ppa_data(
            season=2020,
            team="Ohio State"
        )
        print(json_data)
        time.sleep(5)

        # Get team season PPA data for the 2020 Ohio State Buckeyes, 
        # but exclude garbage time plays when making the PPA calculations.
        print("Get team season PPA data for the 2020 Ohio State Buckeyes, but exclude garbage time plays when making the PPA calculations.")
        json_data = get_cfbd_team_ppa_data(
            season=2020,
            team="Ohio State",
            exclude_garbage_time=True
        )
        print(json_data)
        time.sleep(5)

        # Get team season PPA data for teams in the Big 10 (B1G) Conference in the 2020 CFB Season.
        print("Get team season PPA data for teams in the Big 10 (B1G) Conference in the 2020 CFB Season.")
        json_data = get_cfbd_team_ppa_data(
            season=2020,
            conference_abv="B1G"
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_team_ppa_data(
            season=2020,
            conference_abv="B1G",
            return_as_dict=True
        )
        print(json_data)

    ```
    Returns
    ----------
    A pandas `DataFrame` object with team season PPA data, 
    or (if `return_as_dict` is set to `True`) 
    a dictionary object with a team season PPA data.

    """

    now = datetime.now()
    ppa_df = pd.DataFrame()
    row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/ppa/teams"

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

    if season == None and team == None:
        raise ValueError(
            "To use this function, `season` and/or `team` must be set to a " +
            "non-null variable."
        )

    if season == None:
        # Rare, but in this endpoint,
        # you don't need to input the season.
        pass
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

    if exclude_garbage_time != None and url_elements == 0:
        url += f"?excludeGarbageTime={gt_str}"
        url_elements += 1
    elif exclude_garbage_time != None:
        url += f"&excludeGarbageTime={gt_str}"
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

    for team in tqdm(json_data):
        t_season = team['season']
        t_conference = team['conference']
        t_name = team['team']

        row_df = pd.DataFrame(
            {
                "season": t_season,
                "team_name": t_name,
                "team_conference": t_conference
            },
            index=[0]
        )

        # Team offense
        row_df['offensive_ppa_overall'] = team['offense']['overall']
        row_df['offensive_ppa_passing'] = team['offense']['passing']
        row_df['offensive_ppa_rushing'] = team['offense']['rushing']
        row_df['offensive_ppa_first_down'] = team['offense']['firstDown']
        row_df['offensive_ppa_second_down'] = team['offense']['secondDown']
        row_df['offensive_ppa_third_down'] = team['offense']['thirdDown']
        row_df['offensive_ppa_cumulative'] = team['offense']['cumulative']['total']
        row_df['offensive_ppa_cumulative_passing'] = team['offense']['cumulative']['passing']
        row_df['offensive_ppa_cumulative_rushing'] = team['offense']['cumulative']['rushing']

        # Team defense
        row_df['defensive_ppa_overall'] = team['defense']['overall']
        row_df['defensive_ppa_passing'] = team['defense']['passing']
        row_df['defensive_ppa_rushing'] = team['defense']['rushing']
        row_df['defensive_ppa_first_down'] = team['defense']['firstDown']
        row_df['defensive_ppa_second_down'] = team['defense']['secondDown']
        row_df['defensive_ppa_third_down'] = team['defense']['thirdDown']
        row_df['defensive_ppa_cumulative'] = team['defense']['cumulative']['total']
        row_df['defensive_ppa_cumulative_passing'] = team['defense']['cumulative']['passing']
        row_df['defensive_ppa_cumulative_rushing'] = team['defense']['cumulative']['rushing']

        ppa_df = pd.concat([ppa_df, row_df], ignore_index=True)

        del t_season, t_conference, t_name
        del row_df

    return ppa_df


def get_cfbd_team_game_ppa_data(
        season: int,
        api_key: str = None,
        api_key_dir: str = None,
        week: int = None,
        team: str = None,
        conference_abv: str = None,
        exclude_garbage_time: bool = False,
        season_type: str = "regular",  # "regular" or "postseason"
        return_as_dict: bool = False):
    """
    Allows you to get team PPA data, 
    at a game level,
    with or without garbage time plays, 
    for a specificed team and/or time period.

    PPA is the CFBD API's equivalent metric to Expected Points Added (EPA).    

    Parameters
    ----------
    `season` (int, mandatory):
        Required argument.
        Specifies the season you want team game PPA data information from.
        This must be specified, otherwise this package, and by extension
        the CFBD API, will not accept the request to get team game PPA data information.

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

    `week` (int, optional):
        Optional argument.
        If `week` is set to an integer, this function will attempt 
        to load team game PPA data from games in that season, and in that week.

    `team` (str, optional):
        Optional argument.
        If you only want team game PPA data for a team, 
        regardless if they are the home/away team,
        set `team` to the name of the team you want team game PPA data from.

    `conference_abv` (str, optional):
        Optional argument.
        If you only want team game PPA data from games 
        involving teams a specific confrence, 
        set `conference_abv` to the abbreviation 
        of the conference you want team game PPA data from.

    `exclude_garbage_time` (bool, optional):
        Optional argument.
        If you want to filter out plays where the result of the game is largely decided,
        set `exclude_garbage_time = True`.
        Default behavior is that this variable is set to 
        `False` when this function is called.

    `season_type` (str, semi-optional):
        Semi-optional argument.
        By defualt, this will be set to "regular", for the CFB regular season.
        If you want team game PPA data for non-regular season games, 
        set `season_type` to "postseason".
        If `season_type` is set to anything but "regular" or "postseason", 
        a `ValueError()` will be raised.

    `return_as_dict` (bool, semi-optional):
        Semi-optional argument.
        If you want this function to return the data as a dictionary (read: JSON object), 
        instead of a pandas `DataFrame` object,
        set `return_as_dict` to `True`.

    Usage
    ----------
    ```
    import time

    from cfbd_json_py.metrics import get_cfbd_team_game_ppa_data


    cfbd_key = "tigersAreAwsome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwsome":
        print("Using the user's API key declared in this script for this example.")

        # Get team PPA data for individual games within the 2020 CFB season.
        print("Get team PPA data for individual games within the 2020 CFB season.")
        json_data = get_cfbd_team_game_ppa_data(
            api_key=cfbd_key,
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get team PPA data for week 10 games within the 2020 CFB season.
        print("Get team PPA data for week 10 games within the 2020 CFB season.")
        json_data = get_cfbd_team_game_ppa_data(
            api_key=cfbd_key,
            season=2020,
            week=10
        )
        print(json_data)
        time.sleep(5)

        # Get team PPA data for 
        # University of Cincinnati football games within the 2020 CFB season.
        print("Get team PPA data for University of Cincinnati football games within the 2020 CFB season.")
        json_data = get_cfbd_team_game_ppa_data(
            api_key=cfbd_key,
            season=2020,
            team="Cincinnati"
        )
        print(json_data)
        time.sleep(5)

        # Get team PPA data for Southeastern Conference (SEC) 
        # games within the 2020 CFB season.
        print("Get team PPA data for Southeastern Conference (SEC) games within the 2020 CFB season.")
        json_data = get_cfbd_team_game_ppa_data(
            api_key=cfbd_key,
            season=2020,
            conference_abv="SEC"
        )
        print(json_data)
        time.sleep(5)

        # Get team PPA data for Southeastern Conference (SEC) 
        # games within the 2020 CFB season, but exclude plays that occur in garbage time.
        print("Get team PPA data for Southeastern Conference (SEC) games within the 2020 CFB season, but exclude plays that occur in garbage time.")
        json_data = get_cfbd_team_game_ppa_data(
            api_key=cfbd_key,
            season=2020,
            conference_abv="SEC",
            exclude_garbage_time=True
        )
        print(json_data)
        time.sleep(5)

        # Get team PPA data for postseason games in the 2020 CFB season.
        print("Get team PPA data for postseason games in the 2020 CFB season.")
        json_data = get_cfbd_team_game_ppa_data(
            api_key=cfbd_key,
            season=2020,
            season_type="postseason"
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_team_game_ppa_data(
            api_key=cfbd_key,
            season=2020,
            team="Cincinnati",
            return_as_dict=True
        )
        print(json_data)

    else:
        # Alternatively, if the CFBD API key exists in this python environment,
        # or it's been set by cfbd_json_py.utls.set_cfbd_api_token(),
        # you could just call these functions directly, without setting the API key
        # in the script.
        print("Using the user's API key suposedly loaded into this python environment for this example.")

        # Get team PPA data for individual games within the 2020 CFB season.
        print("Get team PPA data for individual games within the 2020 CFB season.")
        json_data = get_cfbd_team_game_ppa_data(
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get team PPA data for week 10 games within the 2020 CFB season.
        print("Get team PPA data for week 10 games within the 2020 CFB season.")
        json_data = get_cfbd_team_game_ppa_data(
            season=2020,
            week=10
        )
        print(json_data)
        time.sleep(5)

        # Get team PPA data for 
        # University of Cincinnati football games within the 2020 CFB season.
        print("Get team PPA data for University of Cincinnati football games within the 2020 CFB season.")
        json_data = get_cfbd_team_game_ppa_data(
            season=2020,
            team="Cincinnati"
        )
        print(json_data)
        time.sleep(5)

        # Get team PPA data for Southeastern Conference (SEC) 
        # games within the 2020 CFB season.
        print("Get team PPA data for Southeastern Conference (SEC) games within the 2020 CFB season.")
        json_data = get_cfbd_team_game_ppa_data(
            season=2020,
            conference_abv="SEC"
        )
        print(json_data)
        time.sleep(5)

        # Get team PPA data for Southeastern Conference (SEC) 
        # games within the 2020 CFB season, but exclude plays that occur in garbage time.
        print("Get team PPA data for Southeastern Conference (SEC) games within the 2020 CFB season, but exclude plays that occur in garbage time.")
        json_data = get_cfbd_team_game_ppa_data(
            season=2020,
            conference_abv="SEC",
            exclude_garbage_time=True
        )
        print(json_data)
        time.sleep(5)

        # Get team PPA data for postseason games in the 2020 CFB season.
        print("Get team PPA data for postseason games in the 2020 CFB season.")
        json_data = get_cfbd_team_game_ppa_data(
            season=2020,
            season_type="postseason"
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_team_game_ppa_data(
            season=2020,
            team="Cincinnati",
            return_as_dict=True
        )
        print(json_data)

    ```
    Returns
    ----------
    A pandas `DataFrame` object with team PPA data, 
    or (if `return_as_dict` is set to `True`) 
    a dictionary object with team PPA data.

    """

    now = datetime.now()
    cfb_games_df = pd.DataFrame()
    row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/ppa/games"

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

    if week != None and week < 0:
        raise ValueError(
            "`week` must be a positive number."
        )

    if season_type != "regular" and season_type != "postseason":
        raise ValueError(
            "`season_type` must be set to either \"regular\" or \"postseason\" for this function to work.")

    gt_str = ""
    if exclude_garbage_time == True:
        gt_str = "true"
    elif exclude_garbage_time == False:
        gt_str = "false"

    # URL builder
    ########################################################################################################################################################################################################

    # Required by API
    url += f"?seasonType={season_type}"
    url += f"&year={season}"

    if week != None:
        url += f"&week={week}"

    if team != None:
        url += f"&team={team}"

    if conference_abv != None:
        url += f"&conference={conference_abv}"

    if exclude_garbage_time != None:
        url += f"&excludeGarbageTime={gt_str}"

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
        g_season = game['season']
        g_gid = game['gameId']
        g_week = game['week']
        g_tm = game['team']
        g_conf = game['conference']
        g_opp = game['opponent']

        row_df = pd.DataFrame(
            {
                "season": g_season,
                "game_id": g_gid,
                "week": g_week,
                "team": g_tm,
                "conference": g_conf,
                "opponent": g_opp
            },
            index=[0]
        )

        # Team Offense
        row_df['ppa_offense_overall'] = game['offense']['overall']
        row_df['ppa_offense_passing'] = game['offense']['passing']
        row_df['ppa_offense_rushing'] = game['offense']['rushing']
        row_df['ppa_offense_first_down'] = game['offense']['firstDown']
        row_df['ppa_offense_second_down'] = game['offense']['secondDown']
        row_df['ppa_offense_third_down'] = game['offense']['thirdDown']

        # Team Defense
        row_df['ppa_defense_overall'] = game['defense']['overall']
        row_df['ppa_defense_passing'] = game['defense']['passing']
        row_df['ppa_defense_rushing'] = game['defense']['rushing']
        row_df['ppa_defense_first_down'] = game['defense']['firstDown']
        row_df['ppa_defense_second_down'] = game['defense']['secondDown']
        row_df['ppa_defense_third_down'] = game['defense']['thirdDown']

        cfb_games_df = pd.concat([cfb_games_df, row_df], ignore_index=True)

        del row_df
        del g_gid, g_season, g_week,\
            g_conf, g_tm, g_opp

    return cfb_games_df


def get_cfbd_player_game_ppa_data(
        api_key: str = None,
        api_key_dir: str = None,
        season: int = None,
        week: int = None,
        team: str = None,
        # A week or team must be specified
        position: str = None,
        player_id: int = None,
        play_threshold: int = None,
        exclude_garbage_time: bool = False,
        season_type: str = "regular",  # "regular" or "postseason"
        return_as_dict: bool = False):
    """
    Allows you to get player PPA data, 
    at a game level,
    with or without garbage time plays, 
    for a specificed time period and/or team.

    PPA is the CFBD API's equivalent metric to Expected Points Added (EPA).    

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

    `season` (int, semi-optional):
        Semi-Optional argument.
        Specifies the season you want player game PPA data information from.
        This must be specified, otherwise this package, and by extension
        the CFBD API, will not accept the request to get player game PPA data information.

    `week` (int, semi-optional):
        Semi-Optional argument.
        If `week` is set to an integer, this function will attempt 
        to load player game PPA data from games in that season, and in that week.
        `week` and/or `team` must be set to a non-null value for this function 
        to work.

    `team` (str, semi-optional):
        Semi-Optional argument.
        If you only want player game PPA data for players of a specific team, 
        regardless if they are the home/away team,
        set `team` to the name of the team you want player game PPA data from.
        `week` and/or `team` must be set to a non-null value for this function 
        to work.

    `position` (str, optional):
        Optional argument.
        If you only want player game PPA data for players of a specific position, 
        set `position` to the position you want player game PPA data from.

    `player_id` (int, optional):
        Optional argument.
        If you only want PPA data for a specific player ID, 
        set this variable to the player ID of the player you want PPA data from. 

    `play_threshold`
        Optional argument.
        If you only want PPA data for players 
        who touched the ball for *X* number of plays in a game,
        set `play_threshold = x`, where `x` is 
        your specified minimum number of plays.

    `exclude_garbage_time` (bool, optional):
        Optional argument.
        If you want to filter out plays where the result of the game is largely decided,
        set `exclude_garbage_time = True`.
        Default behavior is that this variable is set to 
        `False` when this function is called.

    `season_type` (str, semi-optional):
        Semi-optional argument.
        By defualt, this will be set to "regular", for the CFB regular season.
        If you want player game PPA data for non-regular season games, 
        set `season_type` to "postseason".
        If `season_type` is set to anything but "regular" or "postseason", 
        a `ValueError()` will be raised.

    `return_as_dict` (bool, semi-optional):
        Semi-optional argument.
        If you want this function to return the data as a dictionary (read: JSON object), 
        instead of a pandas `DataFrame` object,
        set `return_as_dict` to `True`.

    Usage
    ----------
    ```
    import time

    from cfbd_json_py.metrics import get_cfbd_player_game_ppa_data


    cfbd_key = "tigersAreAwsome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwsome":
        print("Using the user's API key declared in this script for this example.")

        # Get player game PPA data for week 10 of the 2020 CFB season.
        print("Get player game PPA data for week 10 of the 2020 CFB season.")
        json_data = get_cfbd_player_game_ppa_data(
            api_key=cfbd_key,
            season=2020,
            week=10
        )
        print(json_data)
        time.sleep(5)

        # Get player game PPA data for players of the 
        # 2020 University of Cincinnati Football team.
        print("Get player game PPA data for players of the 2020 University of Cincinnati Football team.")
        json_data = get_cfbd_player_game_ppa_data(
            api_key=cfbd_key,
            season=2020,
            team="Cincinnati"
        )
        print(json_data)
        time.sleep(5)

        # Get player game PPA data for QBs who played in week 10 of the 2020 CFB season.
        print("Get player game PPA data for week 10 of the 2020 CFB season.")
        json_data = get_cfbd_player_game_ppa_data(
            api_key=cfbd_key,
            season=2020,
            week=10,
            position="QB"
        )
        print(json_data)
        time.sleep(5)

        # Get player game PPA data for QBs who played in week 10 of the 2020 CFB season, 
        # but exclude plays in garbage time.
        print("Get player game PPA data for week 10 of the 2020 CFB season, but exclude plays in garbage time.")
        json_data = get_cfbd_player_game_ppa_data(
            api_key=cfbd_key,
            season=2020,
            week=10,
            position="QB",
            exclude_garbage_time=True
        )
        print(json_data)
        time.sleep(5)

        # Get player game PPA data for week 10 of the 2020 CFB season,
        # where a player touched the ball for at least 25 plays.
        print("Get player game PPA data for week 10 of the 2020 CFB season, where a player touched the ball for at least 25 plays.")
        json_data = get_cfbd_player_game_ppa_data(
            api_key=cfbd_key,
            season=2020,
            week=10,
            play_threshold=25
        )
        print(json_data)
        time.sleep(5)

        # Get player game PPA data the 2020 Alabama Crimson Tide Football team, 
        # during their postseason.
        print("Get player game PPA data the 2020 Alabama Crimson Tide Football team, during their postseason.")
        json_data = get_cfbd_player_game_ppa_data(
            api_key=cfbd_key,
            season=2020,
            team="Alabama",
            season_type="postseason"
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_player_game_ppa_data(
            api_key=cfbd_key,
            season=2020,
            week=10,
            return_as_dict=True
        )
        print(json_data)

    else:
        # Alternatively, if the CFBD API key exists in this python environment,
        # or it's been set by cfbd_json_py.utls.set_cfbd_api_token(),
        # you could just call these functions directly, without setting the API key
        # in the script.
        print("Using the user's API key suposedly loaded into this python environment for this example.")

        # Get player game PPA data for week 10 of the 2020 CFB season.
        print("Get player game PPA data for week 10 of the 2020 CFB season.")
        json_data = get_cfbd_player_game_ppa_data(
            season=2020,
            week=10
        )
        print(json_data)
        time.sleep(5)

        # Get player game PPA data for players of the 
        # 2020 University of Cincinnati Football team.
        print("Get player game PPA data for players of the 2020 University of Cincinnati Football team.")
        json_data = get_cfbd_player_game_ppa_data(
            season=2020,
            team="Cincinnati"
        )
        print(json_data)
        time.sleep(5)

        # Get player game PPA data for QBs who played in week 10 of the 2020 CFB season.
        print("Get player game PPA data for week 10 of the 2020 CFB season.")
        json_data = get_cfbd_player_game_ppa_data(
            season=2020,
            week=10,
            position="QB"
        )
        print(json_data)
        time.sleep(5)

        # Get player game PPA data for QBs who played in week 10 of the 2020 CFB season, 
        # but exclude plays in garbage time.
        print("Get player game PPA data for week 10 of the 2020 CFB season, but exclude plays in garbage time.")
        json_data = get_cfbd_player_game_ppa_data(
            season=2020,
            week=10,
            position="QB",
            exclude_garbage_time=True
        )
        print(json_data)
        time.sleep(5)

        # Get player game PPA data for week 10 of the 2020 CFB season,
        # where a player touched the ball for at least 25 plays.
        print("Get player game PPA data for week 10 of the 2020 CFB season, where a player touched the ball for at least 25 plays.")
        json_data = get_cfbd_player_game_ppa_data(
            season=2020,
            week=10,
            play_threshold=25
        )
        print(json_data)
        time.sleep(5)

        # Get player game PPA data the 2020 Alabama Crimson Tide Football team, 
        # during their postseason.
        print("Get player game PPA data the 2020 Alabama Crimson Tide Football team, during their postseason.")
        json_data = get_cfbd_player_game_ppa_data(
            season=2020,
            team="Alabama",
            season_type="postseason"
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_player_game_ppa_data(
            season=2020,
            week=10,
            return_as_dict=True
        )
        print(json_data)

    ```
    Returns
    ----------
    A pandas `DataFrame` object with player PPA data, 
    or (if `return_as_dict` is set to `True`) 
    a dictionary object with player PPA data.

    """

    now = datetime.now()
    cfb_games_df = pd.DataFrame()
    row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/ppa/players/games"

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

    if week == None and team == None:
        raise ValueError(
            "To call this function, you must set `week` and/or `team` " +
            "to a non-null value."
        )

    if season_type != "regular" and season_type != "postseason":
        raise ValueError(
            "`season_type` must be set to either \"regular\" or \"postseason\" for this function to work.")

    if week != None and week < 0:
        raise ValueError(
            "`week` must be a positive number."
        )

    if season_type != "regular" and season_type != "postseason":
        raise ValueError(
            "`season_type` must be set to either \"regular\" or \"postseason\" for this function to work.")

    if play_threshold != None and play_threshold < 0:
        raise ValueError(
            "`play_threshold` must be an integer at or greater than 0."
        )

    gt_str = ""
    if exclude_garbage_time == True:
        gt_str = "true"
    elif exclude_garbage_time == False:
        gt_str = "false"

    # URL builder
    ########################################################################################################################################################################################################
    url_elements = 0

    if season != None and url_elements == 0:
        url += f"?year={season}"
        url_elements += 1
    elif season != None:
        url += f"&year={season}"
        url_elements += 1

    if week != None and url_elements == 0:
        url += f"?week={week}"
        url_elements += 1
    elif week != None:
        url += f"&week={week}"
        url_elements += 1

    if team != None and url_elements == 0:
        url += f"?team={team}"
        url_elements += 1
    elif team != None:
        url += f"&team={team}"
        url_elements += 1

    if position != None and url_elements == 0:
        url += f"?position={position}"
        url_elements += 1
    elif position != None:
        url += f"&position={position}"
        url_elements += 1

    if player_id != None and url_elements == 0:
        url += f"?playerId={player_id}"
        url_elements += 1
    elif player_id != None:
        url += f"&playerId={player_id}"
        url_elements += 1

    if play_threshold != None and url_elements == 0:
        url += f"?threshold={play_threshold}"
        url_elements += 1
    elif play_threshold != None:
        url += f"&threshold={play_threshold}"
        url_elements += 1

    if exclude_garbage_time != None and url_elements == 0:
        url += f"?excludeGarbageTime={gt_str}"
        url_elements += 1
    elif exclude_garbage_time != None:
        url += f"&excludeGarbageTime={gt_str}"
        url_elements += 1

    if season_type != None and url_elements == 0:
        url += f"?seasonType={season_type}"
        url_elements += 1
    elif season_type != None:
        url += f"&seasonType={season_type}"
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

    for player in tqdm(json_data):
        p_season = player['season']
        row_df = pd.DataFrame(
            {
                "season": p_season
            },
            index=[0]
        )

        row_df['week'] = player['week']
        row_df['player_name'] = player['name']
        row_df['player_position'] = player['position']
        row_df['team'] = player['team']
        row_df['opponent'] = player['opponent']

        row_df['avg_ppa_all'] = player['averagePPA']['all']
        row_df['avg_ppa_pass'] = player['averagePPA']['pass']
        row_df['avg_ppa_rush'] = player['averagePPA']['rush']

        # Have to do this because of a FutureWarning that is raised
        # starting in pandas 2.1.1, when using pd.concat(),
        # and a column datatype mismatch is found.
        row_df = row_df.astype(
            {
                "avg_ppa_all": "float",
                "avg_ppa_pass": "float",
                "avg_ppa_rush": "float",
            }
        )

        cfb_games_df = pd.concat([cfb_games_df, row_df], ignore_index=True)

        del row_df
        del p_season

    return cfb_games_df


def get_cfbd_player_season_ppa_data(
        api_key: str = None,
        api_key_dir: str = None,
        season: int = None,
        team: str = None,
        conference_abv: str = None,
        position: str = None,
        player_id: int = None,
        play_threshold: int = None,
        exclude_garbage_time: bool = False,
        return_as_dict: bool = False):
    """
    Allows you to get player PPA data, 
    at a season level,
    with or without garbage time plays, 
    for a specificed time period and/or team.

    PPA is the CFBD API's equivalent metric to Expected Points Added (EPA).    

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

    `season` (int, semi-optional):
        Semi-Optional argument.
        Specifies the season you want player season PPA data information from.
        This must be specified, otherwise this package, and by extension
        the CFBD API, will not accept the request to get player season PPA data information.


    `team` (str, semi-optional):
        Semi-Optional argument.
        If you only want player season PPA data for players of a specific team, 
        regardless if they are the home/away team,
        set `team` to the name of the team you want player season PPA data from.
        `week` and/or `team` must be set to a non-null value for this function 
        to work.

    `conference_abv` (str, optional):
        Optional argument.
        If you only want player season PPA data from games 
        involving teams from a specific confrence, 
        set `conference_abv` to the abbreviation 
        of the conference you want player season PPA data from.
        For a list of confrences, 
        use the `cfbd_json_py.conferences.get_cfbd_conference_info()`
        function.

    `position` (str, optional):
        Optional argument.
        If you only want player season PPA data for players of a specific position, 
        set `position` to the position you want player season PPA data from.

    `player_id` (int, optional):
        Optional argument.
        If you only want PPA data for a specific player ID, 
        set this variable to the player ID of the player you want PPA data from. 

    `play_threshold`
        Optional argument.
        If you only want PPA data for players 
        who touched the ball for *X* number of plays in a game,
        set `play_threshold = x`, where `x` is 
        your specified minimum number of plays.

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

    from cfbd_json_py.metrics import get_cfbd_player_season_ppa_data


    cfbd_key = "tigersAreAwsome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwsome":
        print("Using the user's API key declared in this script for this example.")

        # Get player season PPA data for the 2020 CFB season.
        print("Get player season PPA data for the 2020 CFB season.")
        json_data = get_cfbd_player_season_ppa_data(
            api_key=cfbd_key,
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get player season PPA data from the 2020 Ohio Bobcats Football Team.
        print("Get player season PPA data for the 2020 Ohio Bobcats Football Team.")
        json_data = get_cfbd_player_season_ppa_data(
            api_key=cfbd_key,
            season=2020,
            team="Ohio"
        )
        print(json_data)
        time.sleep(5)

        # Get player season PPA data for players who played on
        # teams within the Southeastern Conference (SEC) for the
        # 2020 CFB Season.
        print("Get player season PPA data for players who played on teams within the Southeastern Conference (SEC) for the 2020 CFB Season.")
        json_data = get_cfbd_player_season_ppa_data(
            api_key=cfbd_key,
            season=2020,
            conference_abv="SEC"
        )
        print(json_data)
        time.sleep(5)

        # Get player season PPA data from QBs in the 2020 CFB Season.
        print("Get player season PPA data from QBs in the 2020 CFB Season.")
        json_data = get_cfbd_player_season_ppa_data(
            api_key=cfbd_key,
            season=2020,
            position="QB"
        )
        print(json_data)
        time.sleep(5)

        # Get player season PPA data from
        # former Ohio State and LSU QB Joe Burrow (player ID #3915511).
        print("Get player season PPA data from former Ohio State and LSU QB Joe Burrow (player ID #3915511).")
        json_data = get_cfbd_player_season_ppa_data(
            api_key=cfbd_key,
            player_id=3915511
        )
        print(json_data)
        time.sleep(5)

        # Get player season PPA data from
        # former Ohio State and LSU QB Joe Burrow (player ID #3915511),
        # but exclude plays that occured in garbage time.
        print("Get player season PPA data from former Ohio State and LSU QB Joe Burrow (player ID #3915511), but exclude plays that occured in garbage time.")
        json_data = get_cfbd_player_season_ppa_data(
            api_key=cfbd_key,
            player_id=3915511,
            exclude_garbage_time=True
        )
        print(json_data)
        time.sleep(5)

        # Get player season PPA data from the 2020 CFB Season,
        # for players with at least 100 plays/touches.
        print("Get player season PPA data from the 2020 CFB Season, for players with at least 100 plays/touches.")
        json_data = get_cfbd_player_season_ppa_data(
            api_key=cfbd_key,
            season=2020,
            play_threshold=100
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_player_season_ppa_data(
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

        # Get player season PPA data for the 2020 CFB season.
        print("Get player season PPA data for the 2020 CFB season.")
        json_data = get_cfbd_player_season_ppa_data(
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get player season PPA data from the 2020 Ohio Bobcats Football Team.
        print("Get player season PPA data for the 2020 Ohio Bobcats Football Team.")
        json_data = get_cfbd_player_season_ppa_data(
            season=2020,
            team="Ohio"
        )
        print(json_data)
        time.sleep(5)

        # Get player season PPA data for players who played on
        # teams within the Southeastern Conference (SEC) for the
        # 2020 CFB Season.
        print("Get player season PPA data for players who played on teams within the Southeastern Conference (SEC) for the 2020 CFB Season.")
        json_data = get_cfbd_player_season_ppa_data(
            season=2020,
            conference_abv="SEC"
        )
        print(json_data)
        time.sleep(5)

        # Get player season PPA data from QBs in the 2020 CFB Season.
        print("Get player season PPA data from QBs in the 2020 CFB Season.")
        json_data = get_cfbd_player_season_ppa_data(
            season=2020,
            position="QB"
        )
        print(json_data)
        time.sleep(5)

        # Get player season PPA data from
        # former Ohio State and LSU QB Joe Burrow (player ID #3915511).
        print("Get player season PPA data from former Ohio State and LSU QB Joe Burrow (player ID #3915511).")
        json_data = get_cfbd_player_season_ppa_data(
            player_id=3915511
        )
        print(json_data)
        time.sleep(5)

        # Get player season PPA data from
        # former Ohio State and LSU QB Joe Burrow (player ID #3915511),
        # but exclude plays that occured in garbage time.
        print("Get player season PPA data from former Ohio State and LSU QB Joe Burrow (player ID #3915511), but exclude plays that occured in garbage time.")
        json_data = get_cfbd_player_season_ppa_data(
            player_id=3915511,
            exclude_garbage_time=True
        )
        print(json_data)
        time.sleep(5)

        # Get player season PPA data from the 2020 CFB Season,
        # for players with at least 100 plays/touches.
        print("Get player season PPA data from the 2020 CFB Season, for players with at least 100 plays/touches.")
        json_data = get_cfbd_player_season_ppa_data(
            season=2020,
            play_threshold=100
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_player_season_ppa_data(
            season=2020,
            return_as_dict=True
        )
        print(json_data)

    ```
    Returns
    ----------
    A pandas `DataFrame` object with player PPA data, 
    or (if `return_as_dict` is set to `True`) 
    a dictionary object with player PPA data.

    """
    now = datetime.now()
    cfb_games_df = pd.DataFrame()
    row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/ppa/players/season"

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
        pass
    elif season > (now.year + 1):
        raise ValueError(f"`season` cannot be greater than {season}.")
    elif season < 1869:
        raise ValueError(f"`season` cannot be less than 1869.")

    if play_threshold != None and play_threshold < 0:
        raise ValueError(
            "`play_threshold` must be an integer at or greater than 0."
        )

    gt_str = ""
    if exclude_garbage_time == True:
        gt_str = "true"
    elif exclude_garbage_time == False:
        gt_str = "false"

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

    if position != None and url_elements == 0:
        url += f"?position={position}"
        url_elements += 1
    elif position != None:
        url += f"&position={position}"
        url_elements += 1

    if player_id != None and url_elements == 0:
        url += f"?playerId={player_id}"
        url_elements += 1
    elif player_id != None:
        url += f"&playerId={player_id}"
        url_elements += 1

    if play_threshold != None and url_elements == 0:
        url += f"?threshold={play_threshold}"
        url_elements += 1
    elif play_threshold != None:
        url += f"&threshold={play_threshold}"
        url_elements += 1

    if exclude_garbage_time != None and url_elements == 0:
        url += f"?excludeGarbageTime={gt_str}"
        url_elements += 1
    elif exclude_garbage_time != None:
        url += f"&excludeGarbageTime={gt_str}"
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

    for player in tqdm(json_data):
        p_season = player['season']
        row_df = pd.DataFrame(
            {"season": p_season},
            index=[0]
        )
        row_df['player_id'] = player['id']
        row_df['player_name'] = player['name']
        row_df['player_position'] = player['position']
        row_df['team'] = player['team']
        row_df['conference'] = player['conference']
        row_df['countable_plays'] = player['countablePlays']

        # Average PPA
        row_df['average_ppa_all'] = player['averagePPA']['all']
        row_df['average_ppa_pass'] = player['averagePPA']['pass']
        row_df['average_ppa_rush'] = player['averagePPA']['rush']
        row_df['average_ppa_first_down'] = player['averagePPA']['firstDown']
        row_df['average_ppa_second_down'] = player['averagePPA']['secondDown']
        row_df['average_ppa_third_down'] = player['averagePPA']['thirdDown']
        row_df['average_ppa_standard_downs'] = player['averagePPA']['standardDowns']
        row_df['average_ppa_passing_downs'] = player['averagePPA']['passingDowns']

        # Total PPA
        row_df['total_ppa_all'] = player['totalPPA']['all']
        row_df['total_ppa_pass'] = player['totalPPA']['pass']
        row_df['total_ppa_rush'] = player['totalPPA']['rush']
        row_df['total_ppa_first_down'] = player['totalPPA']['firstDown']
        row_df['total_ppa_second_down'] = player['totalPPA']['secondDown']
        row_df['total_ppa_third_down'] = player['totalPPA']['thirdDown']
        row_df['total_ppa_standard_downs'] = player['totalPPA']['standardDowns']
        row_df['total_ppa_passing_downs'] = player['totalPPA']['passingDowns']

        # Have to do this because of a FutureWarning that is raised
        # starting in pandas 2.1.1, when using pd.concat(),
        # and a column datatype mismatch is found.
        row_df = row_df.astype(
            {
                "average_ppa_all": "float",
                "average_ppa_pass": "float",
                "average_ppa_rush": "float",
                "average_ppa_first_down": "float",
                "average_ppa_second_down": "float",
                "average_ppa_third_down": "float",
                "average_ppa_standard_downs": "float",
                "average_ppa_passing_downs": "float",

                "total_ppa_all": "float",
                "total_ppa_pass": "float",
                "total_ppa_rush": "float",
                "total_ppa_first_down": "float",
                "total_ppa_second_down": "float",
                "total_ppa_third_down": "float",
                "total_ppa_standard_downs": "float",
                "total_ppa_passing_downs": "float"
            }
        )

        cfb_games_df = pd.concat([cfb_games_df, row_df], ignore_index=True)
        del row_df
        del p_season

    return cfb_games_df


def get_cfbd_game_win_probability_data(
        game_id: int,
        api_key: str = None,
        api_key_dir: str = None,
        return_as_dict: bool = False):
    """
    Allows one to get win probabliity data for a given game ID.

    Parameters
    ----------

    `game_id` (int, mandatory):
        Mandatory argument.
        This is the game ID for the game you want win probability data from,
        at the play-by-play level.

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

    from cfbd_json_py.metrics import get_cfbd_game_win_probability_data


    cfbd_key = "tigersAreAwsome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwsome":
        print("Using the user's API key declared in this script for this example.")

        # Get the win probablility data for a 2017 game between 
        # the University of Cincinnati and UConn (game ID #400941851).
        print("Get the win probablility data for a 2017 game between the University of Cincinnati and UConn (game ID #400941851).")
        json_data = get_cfbd_game_win_probability_data(
            api_key=cfbd_key,
            game_id=400941851
        )
        print(json_data)
        time.sleep(5)

        # Get the win probablility data for a 2023 game between 
        # the University of Duke and the University of Louisville (game ID #401525535).
        print("Get the win probablility data for a 2023 game between the University of Duke and the University of Louisville (game ID #401525535).")
        json_data = get_cfbd_game_win_probability_data(
            api_key=cfbd_key,
            game_id=401525535
        )
        print(json_data)
        time.sleep(5)


        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_game_win_probability_data(
            api_key=cfbd_key,
            game_id=400941851,
            return_as_dict=True
        )
        print(json_data)

    else:
        # Alternatively, if the CFBD API key exists in this python environment,
        # or it's been set by cfbd_json_py.utls.set_cfbd_api_token(),
        # you could just call these functions directly, without setting the API key
        # in the script.
        print("Using the user's API key suposedly loaded into this python environment for this example.")

        # Get win probablility data for a 2017 game between 
        # the University of Cincinnati and UConn (game ID #400941851).
        print("Get the win probablility data for a 2017 game between the University of Cincinnati and UConn (game ID #400941851).")
        json_data = get_cfbd_game_win_probability_data(
            game_id=400941851
        )
        print(json_data)
        time.sleep(5)

        # Get win probablility data for a 2023 game between 
        # the University of Duke and the University of Louisville (game ID #401525535).
        print("Get the win probablility data for a 2023 game between the University of Duke and the University of Louisville (game ID #401525535).")
        json_data = get_cfbd_game_win_probability_data(
            game_id=401525535
        )
        print(json_data)
        time.sleep(5)


        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_game_win_probability_data(
            game_id=400941851,
            return_as_dict=True
        )
        print(json_data)

    ```
    Returns
    ----------
    A pandas `DataFrame` object with win probability data at the play-by-play level,
    or (if `return_as_dict` is set to `True`) 
    a dictionary object with win probability data at the play-by-play level.

    """

    wp_df = pd.DataFrame()
    row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/metrics/wp"

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

    for play in tqdm(json_data):
        row_df = pd.DataFrame(
            {"game_id": game_id},
            index=[0]
        )
        row_df['play_id'] = play['playId']
        row_df['play_text'] = play['playText']
        row_df['home_id'] = play['homeId']
        row_df['home_team_name'] = play['home']
        row_df['away_id'] = play['awayId']
        row_df['away_team_name'] = play['away']
        row_df['spread'] = play['spread']
        row_df['home_team_has_ball'] = play['homeBall']
        row_df['home_score'] = play['homeScore']
        row_df['away_score'] = play['awayScore']
        row_df['down'] = play['down']
        row_df['distance'] = play['distance']
        row_df['home_win_probability'] = play['homeWinProb']
        row_df['play_number'] = play['playNumber']

        wp_df = pd.concat([wp_df, row_df], ignore_index=True)

    if len(wp_df) == 0:
        logging.error(
            "The CFBD API accepted your inputs, " +
            "but found no data within your specified input paramaters." +
            " Please double check your input paramaters."
        )
    else:
        wp_df = wp_df.astype(
            {"home_win_probability": "float"}
        )
        wp_df['away_win_probability'] = 1 - wp_df['home_win_probability']

    return wp_df


def get_cfbd_pregame_win_probability_data(
        season: int,
        api_key: str = None,
        api_key_dir: str = None,
        week: int = None,
        team: str = None,
        season_type: str = "regular",  # "regular" or "postseason"
        return_as_dict: bool = False):
    """
    Allows you to get pregame win probability data for games within a timeframe.

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
        Specifies the season you want pregame win probability data.

    `week` (int, optional):
        Optional argument.
        If `week` is set to an integer, this function will attempt 
        to load CFB game data from games in that season, and in that week.

    `team` (str, optional):
        Semi-ptional argument.
        If you only want pregame win probability data for a specific team,
        set `team` to the name of the team you want pregame win probability data from.

    `season_type` (str, semi-optional):
        Semi-optional argument.
        By defualt, this will be set to "regular", for the CFB regular season.
        If you want CFB game information for non-regular season games, 
        set `season_type` to "postseason".
        If `season_type` is set to anything but "regular" or "postseason", 
        a `ValueError()` will be raised.

    `return_as_dict` (bool, semi-optional):
        Semi-optional argument.
        If you want this function to return the data as a dictionary (read: JSON object), 
        instead of a pandas `DataFrame` object,
        set `return_as_dict` to `True`.

    Usage
    ----------
    ```
    import time

    from cfbd_json_py.metrics import get_cfbd_pregame_win_probability_data


    cfbd_key = "tigersAreAwsome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwsome":
        print("Using the user's API key declared in this script for this example.")

        # Get pregame win probabilities for games in the 2023 CFB season.
        print("Get pregame win probabilities for games in the 2023 CFB season.")
        json_data = get_cfbd_pregame_win_probability_data(
            api_key=cfbd_key,
            season=2023
        )
        print(json_data)
        time.sleep(5)


        # Get pregame win probabilities for games in week 10 of the 2021 CFB season.
        print("Get pregame win probabilities for games in week 10 of the 2021 CFB season.")
        json_data = get_cfbd_pregame_win_probability_data(
            api_key=cfbd_key,
            season=2021,
            week=10
        )
        print(json_data)
        time.sleep(5)


        # Get pregame win probabilities for games involving the 2021 Cincinnati Bearcats Football Team.
        print("Get pregame win probabilities for games involving the 2021 Cincinnati Bearcats Football Team.")
        json_data = get_cfbd_pregame_win_probability_data(
            api_key=cfbd_key,
            season=2021,
            week=10
        )
        print(json_data)
        time.sleep(5)


        # Get pregame win probabilities for postseason games in the 2020 CFB season.
        print("Get pregame win probabilities for postseason games in the 2020 CFB season.")
        json_data = get_cfbd_pregame_win_probability_data(
            api_key=cfbd_key,
            season=2020,
            season_type="postseason"
        )
        print(json_data)
        time.sleep(5)


        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_pregame_win_probability_data(
            api_key=cfbd_key,
            season=2023,
            week=10,
            return_as_dict=True
        )
        print(json_data)

    else:
        # Alternatively, if the CFBD API key exists in this python environment,
        # or it's been set by cfbd_json_py.utls.set_cfbd_api_token(),
        # you could just call these functions directly, without setting the API key
        # in the script.
        print("Using the user's API key suposedly loaded into this python environment for this example.")

    # Get pregame win probabilities for games in the 2023 CFB season.
        print("Get pregame win probabilities for games in the 2023 CFB season.")
        json_data = get_cfbd_pregame_win_probability_data(
            season=2023
        )
        print(json_data)
        time.sleep(5)


        # Get pregame win probabilities for games in week 10 of the 2021 CFB season.
        print("Get pregame win probabilities for games in week 10 of the 2021 CFB season.")
        json_data = get_cfbd_pregame_win_probability_data(
            season=2021,
            week=10
        )
        print(json_data)
        time.sleep(5)


        # Get pregame win probabilities for games involving the 2021 Cincinnati Bearcats Football Team.
        print("Get pregame win probabilities for games involving the 2021 Cincinnati Bearcats Football Team.")
        json_data = get_cfbd_pregame_win_probability_data(
            season=2021,
            week=10
        )
        print(json_data)
        time.sleep(5)


        # Get pregame win probabilities for postseason games in the 2020 CFB season.
        print("Get pregame win probabilities for postseason games in the 2020 CFB season.")
        json_data = get_cfbd_pregame_win_probability_data(
            season=2020,
            season_type="postseason"
        )
        print(json_data)
        time.sleep(5)


        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_pregame_win_probability_data(
            season=2023,
            week=10,
            return_as_dict=True
        )
        print(json_data)
        
    ```
    Returns
    ----------
    A pandas `DataFrame` object with pregame win probability data, 
    or (if `return_as_dict` is set to `True`) 
    a dictionary object with a pregame win probability data.

    """
    now = datetime.now()
    wp_df = pd.DataFrame()
    row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/metrics/wp/pregame"

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
        pass
    elif season > (now.year + 1):
        raise ValueError(f"`season` cannot be greater than {season}.")
    elif season < 1869:
        raise ValueError(f"`season` cannot be less than 1869.")

    if week != None and week < 0:
        raise ValueError(
            "`week` must be an integer greater than 0."
        )

    if season_type != "regular" and season_type != "postseason":
        raise ValueError(
            "`season_type` must be set to either \"regular\" or \"postseason\" for this function to work.")



    # URL builder
    ########################################################################################################################################################################################################
    url_elements = 0

    if season != None and url_elements == 0:
        url += f"?year={season}"
        url_elements += 1
    elif season != None:
        url += f"&year={season}"
        url_elements += 1

    if week != None and url_elements == 0:
        url += f"?week={week}"
        url_elements += 1
    elif week != None:
        url += f"&week={week}"
        url_elements += 1

    if team != None and url_elements == 0:
        url += f"?team={team}"
        url_elements += 1
    elif team != None:
        url += f"&team={team}"
        url_elements += 1

    if season_type != None and url_elements == 0:
        url += f"?seasonType={season_type}"
        url_elements += 1
    elif season_type != None:
        url += f"&seasonType={season_type}"
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

    for game in tqdm(json_data):
        g_season = game['season']
        row_df = pd.DataFrame(
            {"season":g_season},
            index=[0]
        )
        row_df['week'] = game['week']
        row_df['season_type'] = game['seasonType']
        row_df['game_id'] = game['gameId']
        row_df['home_team_name'] = game['homeTeam']
        row_df['away_team_name'] = game['awayTeam']
        row_df['spread'] = game['spread']
        row_df['home_win_probability'] = game['homeWinProb']
        
        wp_df = pd.concat([wp_df,row_df],ignore_index=True)
        del row_df
        del g_season

    if len(wp_df) == 0:
        logging.error(
            "The CFBD API accepted your inputs, " +
            "but found no data within your specified input paramaters." +
            " Please double check your input paramaters."
        )
    else:
        wp_df = wp_df.astype(
            {"home_win_probability": "float"}
        )
        wp_df['away_win_probability'] = 1 - wp_df['home_win_probability']

    return wp_df