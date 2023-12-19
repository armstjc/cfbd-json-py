# Creation Date: 08/30/2023 01:13 EDT
# Last Updated Date: 12/19/2023 04:10 PM EDT
# Author: Joseph Armstrong (armstrongjoseph08@gmail.com)
# File Name: ratings.py
# Purpose: Houses functions pertaining to CFB team rating data within the CFBD API.
####################################################################################################

from datetime import datetime
import warnings

import pandas as pd
import requests
from tqdm import tqdm
from cfbd_json_py.utls import get_cfbd_api_token


def get_cfbd_sp_plus_ratings(
    api_key: str = None,
    api_key_dir: str = None,
    season: int = None,
    team: int = None,
    # Either `year` or `team` have to be not null for this function to work.
    return_as_dict: bool = False):
    """
    Allows you to get Success rate and equivalent Points per play (S&P+)
    ratings data from the CFBD API.

    For more information about S&P+, consult the following webpages:
    - https://www.sbnation.com/college-football/2017/10/13/16457830/college-football-advanced-stats-analytics-rankings
    - https://collegefootballdata.com/sp/trends

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

    `season` (int, semi-mandatory):
        Semi-required argument.
        Specifies the season you want S&P+ ratings data from.
        This must be specified, otherwise this package, and by extension
        the CFBD API, will not accept the request to get S&P+ ratings data.
        This or `team` must be set to a valid non-null variable for this to function.

    `team` (str, semi-mandatory):
        Semi-required argument.
        Specifies the season you want S&P+ ratings  data from.
        This must be specified, otherwise this package, and by extension
        the CFBD API, will not accept the request to get S&P+ ratings data.
        This or `season` must be set to a valid non-null variable for this to function.

    `return_as_dict` (bool, semi-optional):
        Semi-optional argument.
        If you want this function to return the data as a dictionary (read: JSON object),
        instead of a pandas `DataFrame` object,
        set `return_as_dict` to `True`.

    Usage
    ----------
    ```
    import time

    from cfbd_json_py.ratings import get_cfbd_sp_plus_ratings


    cfbd_key = "tigersAreAwsome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwsome":
        print("Using the user's API key declared in this script for this example.")

        # Get S&P+ ratings data for the 2020 CFB season.
        print("Get S&P+ ratings data for the 2020 CFB season.")
        json_data = get_cfbd_sp_plus_ratings(
            api_key=cfbd_key,
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get historical S&P+ ratings data for the
        # University of Cincinnati Bearcats Football Team.
        print("Get historical S&P+ ratings data for the University of Cincinnati Bearcats Football Team.")
        json_data = get_cfbd_sp_plus_ratings(
            api_key=cfbd_key,
            team="Cincinnati"
        )
        print(json_data)
        time.sleep(5)

        # Get S&P+ ratings data for the 2019 Ohio State Buckeyes Football Team.
        print("Get S&P+ ratings data for the 2019 Ohio State Buckeyes Football Team.")
        json_data = get_cfbd_sp_plus_ratings(
            api_key=cfbd_key,
            season=2020,
            team="Ohio State"
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_sp_plus_ratings(
            api_key=cfbd_key,
            season=2020,
            team="Ohio State",
            return_as_dict=True
        )
        print(json_data)

    else:
        # Alternatively, if the CFBD API key exists in this python environment,
        # or it's been set by cfbd_json_py.utls.set_cfbd_api_token(),
        # you could just call these functions directly, without setting the API key
        # in the script.
        print("Using the user's API key suposedly loaded into this python environment for this example.")

        # Get S&P+ ratings data for the 2020 CFB season.
        print("Get S&P+ ratings data for the 2020 CFB season.")
        json_data = get_cfbd_sp_plus_ratings(
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get historical S&P+ ratings data for the
        # University of Cincinnati Bearcats Football Team.
        print("Get historical S&P+ ratings data for the University of Cincinnati Bearcats Football Team.")
        json_data = get_cfbd_sp_plus_ratings(
            team="Cincinnati"
        )
        print(json_data)
        time.sleep(5)

        # Get S&P+ ratings data for the 2019 Ohio State Buckeyes Football Team.
        print("Get S&P+ ratings data for the 2019 Ohio State Buckeyes Football Team.")
        json_data = get_cfbd_sp_plus_ratings(
            season=2020,
            team="Ohio State"
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_sp_plus_ratings(
            season=2020,
            team="Ohio State",
            return_as_dict=True
        )
        print(json_data)
    ```
    Returns
    ----------
    A pandas `DataFrame` object with S&P+ ratings data,
    or (if `return_as_dict` is set to `True`)
    a dictionary object with a with S&P+ ratings data.

    """
    warnings.simplefilter(action="ignore", category=FutureWarning)

    now = datetime.now()
    url = "https://api.collegefootballdata.com/ratings/sp"
    row_df = pd.DataFrame()
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

    if season == None and team == None:
        raise ValueError(
            "`season` and/or `team` must be set to a valid, "
            + "non-null value for this function to work."
        )

    if season != None and (season > (now.year + 1)):
        raise ValueError(f"`season` cannot be greater than {season}.")
    elif season != None and season < 1869:
        raise ValueError(f"`season` cannot be less than 1869.")

    # URL builder
    ########################################################################################################################################################################################################
    # Required by the API

    if season != None and team != None:
        url += f"?year={season}&team={team}"
    elif season != None:
        url += f"?year={season}"
    elif team != None:
        url += f"?team={team}"

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

    # final_df = pd.json_normalize(json_data)

    for team in tqdm(json_data):
        t_year = team["year"]
        t_name = team["team"]
        try:
            t_conf = team["conference"]
        except:
            t_conf = None
        t_sp_rating = team["rating"]
        t_sp_ranking = team["ranking"]
        t_2nd_order_wins = team["secondOrderWins"]
        t_sos = team["sos"]

        row_df = pd.DataFrame(
            {
                "season": t_year,
                "team_name": t_name,
                "conference_name": t_conf,
                "S&P+_rating": t_sp_rating,
                "second_order_wins": t_2nd_order_wins,
                "sos": t_sos,
            },
            index=[0],
        )
        row_df["offense_S&P+_ranking"] = team["offense"]["ranking"]
        row_df["offense_S&P+_rating"] = team["offense"]["rating"]
        row_df["offense_S&P+_success"] = team["offense"]["success"]
        row_df["offense_S&P+_explosiveness"] = team["offense"]["explosiveness"]
        row_df["offense_S&P+_rushing"] = team["offense"]["rushing"]
        row_df["offense_S&P+_passing"] = team["offense"]["passing"]
        row_df["offense_S&P+_standard_downs"] = team["offense"]["standardDowns"]
        row_df["offense_S&P+_passing_downs"] = team["offense"]["passingDowns"]
        row_df["offense_S&P+_run_rate"] = team["offense"]["runRate"]
        row_df["offense_S&P+_pace"] = team["offense"]["pace"]

        row_df["defense_S&P+_ranking"] = team["defense"]["ranking"]
        row_df["defense_S&P+_rating"] = team["defense"]["rating"]
        row_df["defense_S&P+_success"] = team["defense"]["success"]
        row_df["defense_S&P+_explosiveness"] = team["defense"]["explosiveness"]
        row_df["defense_S&P+_rushing"] = team["defense"]["rushing"]
        row_df["defense_S&P+_passing"] = team["defense"]["passing"]
        row_df["defense_S&P+_standard_downs"] = team["defense"]["standardDowns"]
        row_df["defense_S&P+_passing_downs"] = team["defense"]["passingDowns"]
        # row_df["defense_S&P+_run_rate"] = team["defense"]["runRate"]
        row_df["defense_S&P+_havoc_total"] = team["defense"]["havoc"]["total"]
        row_df["defense_S&P+_havoc_front_seven"] = team["defense"]["havoc"][
            "frontSeven"
        ]
        row_df["defense_S&P+_havoc_db"] = team["defense"]["havoc"]["db"]
        row_df["defense_S&P+_special_teams_rating"] = team["specialTeams"]["rating"]

        final_df = pd.concat([final_df, row_df], ignore_index=True)
        del row_df
        del t_year, t_name, t_conf
        del (
            t_sp_ranking,
            t_sp_rating,
        )
        del t_2nd_order_wins, t_sos

    return final_df


def get_cfbd_srs_ratings(
    api_key: str = None,
    api_key_dir: str = None,
    season: int = None,
    team: int = None,
    # Either `year` or `team` have to be not null for this function to work.
    conference_abv: str = None,
    return_as_dict: bool = False):
    """
    Allows you to get Simple Rating System (SRS) data from the CFBD API.

    For more information about S&P+, consult the following webpages:
    - https://www.sports-reference.com/blog/2015/03/srs-calculation-details/
    - https://blog.collegefootballdata.com/talking-tech-bu/

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

    `season` (int, semi-mandatory):
        Semi-required argument.
        Specifies the season you want SRS ratings data from.
        This must be specified, otherwise this package, and by extension
        the CFBD API, will not accept the request to get SRS ratings data.
        This or `team` must be set to a valid non-null variable for this to function.

    `team` (str, semi-mandatory):
        Semi-required argument.
        Specifies the season you want SRS ratings data from.
        This must be specified, otherwise this package, and by extension
        the CFBD API, will not accept the request to get SRS ratings data.
        This or `season` must be set to a valid non-null variable for this to function.

    `conference_abv` (str, optional):
        Optional argument.
        If you only want game information from games
        involving teams a specific confrence,
        set `conference_abv` to the abbreviation
        of the conference you want game information from.

    `return_as_dict` (bool, semi-optional):
        Semi-optional argument.
        If you want this function to return the data as a dictionary (read: JSON object),
        instead of a pandas `DataFrame` object,
        set `return_as_dict` to `True`.

    Usage
    ----------
    ```
    import time

    from cfbd_json_py.ratings import get_cfbd_srs_ratings


    cfbd_key = "tigersAreAwsome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwsome":
        print("Using the user's API key declared in this script for this example.")

        # Get SRS ratings data for the 2020 CFB season.
        print("Get SRS ratings data for the 2020 CFB season.")
        json_data = get_cfbd_srs_ratings(
            api_key=cfbd_key,
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get historical SRS ratings data for the
        # University of Cincinnati Bearcats Football Team.
        print("Get historical SRS ratings data for the University of Cincinnati Bearcats Football Team.")
        json_data = get_cfbd_srs_ratings(
            api_key=cfbd_key,
            team="Cincinnati"
        )
        print(json_data)
        time.sleep(5)

        # Get SRS ratings data for the 2019 Ohio State Buckeyes Football Team.
        print("Get SRS ratings data for the 2019 Ohio State Buckeyes Football Team.")
        json_data = get_cfbd_srs_ratings(
            api_key=cfbd_key,
            season=2020,
            team="Ohio State"
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_srs_ratings(
            api_key=cfbd_key,
            season=2020,
            team="Ohio State",
            return_as_dict=True
        )
        print(json_data)

    else:
        # Alternatively, if the CFBD API key exists in this python environment,
        # or it's been set by cfbd_json_py.utls.set_cfbd_api_token(),
        # you could just call these functions directly, without setting the API key
        # in the script.
        print("Using the user's API key suposedly loaded into this python environment for this example.")

        # Get SRS ratings data for the 2020 CFB season.
        print("Get SRS ratings data for the 2020 CFB season.")
        json_data = get_cfbd_srs_ratings(
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get historical SRS ratings data for the
        # University of Cincinnati Bearcats Football Team.
        print("Get historical SRS ratings data for the University of Cincinnati Bearcats Football Team.")
        json_data = get_cfbd_srs_ratings(
            team="Cincinnati"
        )
        print(json_data)
        time.sleep(5)

        # Get SRS ratings data for the 2019 Ohio State Buckeyes Football Team.
        print("Get SRS ratings data for the 2019 Ohio State Buckeyes Football Team.")
        json_data = get_cfbd_srs_ratings(
            season=2020,
            team="Ohio State"
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_srs_ratings(
            season=2020,
            team="Ohio State",
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
    now = datetime.now()
    url = "https://api.collegefootballdata.com/ratings/srs"
    # row_df = pd.DataFrame()
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

    if season == None and team == None:
        raise ValueError(
            "`season` and/or `team` must be set to a valid, "
            + "non-null value for this function to work."
        )

    if season != None and (season > (now.year + 1)):
        raise ValueError(f"`season` cannot be greater than {season}.")
    elif season != None and season < 1869:
        raise ValueError(f"`season` cannot be less than 1869.")

    # URL builder
    ########################################################################################################################################################################################################
    # Required by the API

    if season != None and team != None:
        url += f"?year={season}&team={team}"
    elif season != None:
        url += f"?year={season}"
    elif team != None:
        url += f"?team={team}"

    if conference_abv != None:
        url += f"&conference={conference_abv}"

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

    final_df = pd.json_normalize(json_data)

    final_df.rename(columns={"rating": "srs_rating"}, inplace=True)
    return final_df


def get_cfbd_sp_plus_conference_ratings(
    api_key: str = None,
    api_key_dir: str = None,
    season: int = None,
    conference_abv: str = None,
    return_as_dict: bool = False):
    """
    Allows you to get Success rate and equivalent Points per play (S&P+)
    ratings data from the CFBD API.

    For more information about S&P+, consult the following webpages:
    - https://www.sbnation.com/college-football/2017/10/13/16457830/college-football-advanced-stats-analytics-rankings
    - https://collegefootballdata.com/sp/trends

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
        Optional argument.
        Specifies the season you want S&P+ ratings data from.
        This must be specified, otherwise this package, and by extension
        the CFBD API, will not accept the request to get S&P+ ratings data.
        This or `team` must be set to a valid non-null variable for this to function.

    `team` (str, optional):
        Optional argument.
        Specifies the season you want S&P+ ratings data from.
        This must be specified, otherwise this package, and by extension
        the CFBD API, will not accept the request to get S&P+ ratings data.
        This or `season` must be set to a valid non-null variable for this to function.

    `conference_abv` (str, optional):
        Optional argument.
        If you only want S&P+ ratings data from games
        involving teams a specific confrence,
        set `conference_abv` to the abbreviation
        of the conference you want S&P+ ratings data from.

    `return_as_dict` (bool, semi-optional):
        Semi-optional argument.
        If you want this function to return the data as a dictionary (read: JSON object),
        instead of a pandas `DataFrame` object,
        set `return_as_dict` to `True`.

    Usage
    ----------
    ```
    import time

    from cfbd_json_py.ratings import get_cfbd_sp_plus_conference_ratings


    cfbd_key = "tigersAreAwsome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwsome":
        print("Using the user's API key declared in this script for this example.")

        # Get S&P+ ratings data for the 2020 CFB season.
        print("Get S&P+ ratings data for the 2020 CFB season.")
        json_data = get_cfbd_sp_plus_conference_ratings(
            api_key=cfbd_key,
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_sp_plus_conference_ratings(
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
        print(
            "Using the user's API key suposedly loaded into this python environment for this example."
        )

        # Get S&P+ ratings data for the 2020 CFB season.
        print("Get S&P+ ratings data for the 2020 CFB season.")
        json_data = get_cfbd_sp_plus_conference_ratings(
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_sp_plus_conference_ratings(
            season=2020,
            return_as_dict=True
        )
        print(json_data)
    ```
    Returns
    ----------
    A pandas `DataFrame` object with S&P+ ratings data,
    or (if `return_as_dict` is set to `True`)
    a dictionary object with a with S&P+ ratings data.
    """
    warnings.simplefilter(action="ignore", category=FutureWarning)

    now = datetime.now()
    url = "https://api.collegefootballdata.com/ratings/sp/conferences"
    row_df = pd.DataFrame()
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

    if season == None and team == None:
        raise ValueError(
            "`season` and/or `team` must be set to a valid, "
            + "non-null value for this function to work."
        )

    if season != None and (season > (now.year + 1)):
        raise ValueError(f"`season` cannot be greater than {season}.")
    elif season != None and season < 1869:
        raise ValueError(f"`season` cannot be less than 1869.")

    # URL builder
    ########################################################################################################################################################################################################
    # Required by the API
    url_elements = 0

    if season != None and url_elements == 0:
        url += f"?year={season}"
        url_elements += 1
    elif season != None:
        url += f"&year={season}"
        url_elements += 1

    if conference_abv != None and url_elements == 0:
        url += f"?conference={conference_abv}"
        url_elements += 1
    elif conference_abv != None:
        url += f"&conference={conference_abv}"
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

    # final_df = pd.json_normalize(json_data)

    for team in tqdm(json_data):
        t_year = team["year"]
        # t_name = team["team"]
        try:
            t_conf = team["conference"]
        except:
            t_conf = None
        t_sp_rating = team["rating"]
        # t_sp_ranking = team["ranking"]
        t_2nd_order_wins = team["secondOrderWins"]
        t_sos = team["sos"]

        row_df = pd.DataFrame(
            {
                "season": t_year,
                # "team_name":t_name,
                "conference_name": t_conf,
                # "S&P+_rating":t_sp_rating,
                "second_order_wins": t_2nd_order_wins,
                "sos": t_sos,
            },
            index=[0],
        )
        # row_df["offense_S&P+_ranking"] = team["offense"]["ranking"]
        row_df["offense_S&P+_rating"] = team["offense"]["rating"]
        row_df["offense_S&P+_success"] = team["offense"]["success"]
        row_df["offense_S&P+_explosiveness"] = team["offense"]["explosiveness"]
        row_df["offense_S&P+_rushing"] = team["offense"]["rushing"]
        row_df["offense_S&P+_passing"] = team["offense"]["passing"]
        row_df["offense_S&P+_standard_downs"] = team["offense"]["standardDowns"]
        row_df["offense_S&P+_passing_downs"] = team["offense"]["passingDowns"]
        row_df["offense_S&P+_run_rate"] = team["offense"]["runRate"]
        row_df["offense_S&P+_pace"] = team["offense"]["pace"]

        # row_df["defense_S&P+_ranking"] = team["defense"]["ranking"]
        row_df["defense_S&P+_rating"] = team["defense"]["rating"]
        row_df["defense_S&P+_success"] = team["defense"]["success"]
        row_df["defense_S&P+_explosiveness"] = team["defense"]["explosiveness"]
        row_df["defense_S&P+_rushing"] = team["defense"]["rushing"]
        row_df["defense_S&P+_passing"] = team["defense"]["passing"]
        row_df["defense_S&P+_standard_downs"] = team["defense"]["standardDowns"]
        row_df["defense_S&P+_passing_downs"] = team["defense"]["passingDowns"]
        # row_df["defense_S&P+_run_rate"] = team["defense"]["runRate"]
        row_df["defense_S&P+_havoc_total"] = team["defense"]["havoc"]["total"]
        row_df["defense_S&P+_havoc_front_seven"] = team["defense"]["havoc"][
            "frontSeven"
        ]
        row_df["defense_S&P+_havoc_db"] = team["defense"]["havoc"]["db"]
        row_df["defense_S&P+_special_teams_rating"] = team["specialTeams"]["rating"]

        final_df = pd.concat([final_df, row_df], ignore_index=True)
        del row_df
        del t_year, t_conf
        del (t_sp_rating,)
        del t_2nd_order_wins, t_sos

    return final_df


def get_cfbd_elo_ratings(
    api_key: str = None,
    api_key_dir: str = None,
    season: int=None,
    week: int = None,
    season_type: str = "postseason",  # "regular" or "postseason"
    team: str = None,
    conference_abv: str = None,
    return_as_dict: bool = False):
    """
    Allows you to get Elo ratings data for CFB teams from the CFBD API.

    For more information about S&P+, consult the following webpages:
    - https://blog.collegefootballdata.com/talking-tech-elo-ratings/
    - https://fivethirtyeight.com/features/introducing-nfl-elo-ratings/

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
        Optional argument.
        Specifies the season you want S&P+ ratings data from.
        This must be specified, otherwise this package, and by extension
        the CFBD API, will not accept the request to get S&P+ ratings data.
        This or `team` must be set to a valid non-null variable for this to function.
    
    `week` (int, optional):
        Optional argument.
        If `week` is set to a valid, non-null integer,
        the CFBD API will return back Elo data for a team up to that week
        in a season.

    `season_type` (str, semi-optional):
        Semi-optional argument.
        By defualt, this will be set to "postseason".
        If `season_type` is set to "regular", 
        the API will ignore postseason games (like bowls and CFP games) when calculating elo.
        If `season_type` is set to anything but "regular" or "postseason", 
        a `ValueError()` will be raised.

    `team` (str, optional):
        Optional argument.
        Specifies the season you want S&P+ ratings data from.
        This must be specified, otherwise this package, and by extension
        the CFBD API, will not accept the request to get S&P+ ratings data.
        This or `season` must be set to a valid non-null variable for this to function.

    `conference_abv` (str, optional):
        Optional argument.
        If you only want S&P+ ratings data from games
        involving teams a specific confrence,
        set `conference_abv` to the abbreviation
        of the conference you want S&P+ ratings data from.

    `return_as_dict` (bool, semi-optional):
        Semi-optional argument.
        If you want this function to return the data as a dictionary (read: JSON object),
        instead of a pandas `DataFrame` object,
        set `return_as_dict` to `True`.

    Usage
    ----------
    ```
    import time

    from cfbd_json_py.ratings import get_cfbd_elo_ratings


    cfbd_key = "tigersAreAwsome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwsome":
        print("Using the user's API key declared in this script for this example.")

        # Get Elo ratings data for the 2020 CFB season.
        print("Get Elo ratings data for the 2020 CFB season.")
        json_data = get_cfbd_elo_ratings(
            api_key=cfbd_key, 
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get Elo ratings data up to week 12 of the 2021 CFB season.
        print("Get Elo ratings data up to week 12 of the 2021 CFB season.")
        json_data = get_cfbd_elo_ratings(
            api_key=cfbd_key, 
            season=2020,
            week=12
        )
        print(json_data)
        time.sleep(5)

        # Get Elo ratings data for the 2020 CFB season, but only for games in the regular season.
        print("Get Elo ratings data for the 2020 CFB season, but only for games in the regular season.")
        json_data = get_cfbd_elo_ratings(
            api_key=cfbd_key, 
            season=2020,
            season_type="regular"
        )
        print(json_data)
        time.sleep(5)

        # Get historical Elo ratings data for the 
        # University of Cincinnati Football Team.
        print("Get historical Elo ratings data for the University of Cincinnati Football Team.")
        json_data = get_cfbd_elo_ratings(
            api_key=cfbd_key, 
            team="Cincinnati"
        )
        print(json_data)
        time.sleep(5)


        # Get Elo ratings data for teams competing in the 
        # Atlantic Coast Confrence (ACC) in the 2021 CFB season.
        print("Get Elo ratings data for teams competing in the Atlantic Coast Confrence (ACC) in the 2021 CFB season.")
        json_data = get_cfbd_elo_ratings(
            api_key=cfbd_key, 
            season=2021,
            conference_abv="ACC"
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_elo_ratings(
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
        print(
            "Using the user's API key suposedly loaded into this python environment for this example."
        )

        # Get Elo ratings data for the 2020 CFB season.
        print("Get Elo ratings data for the 2020 CFB season.")
        json_data = get_cfbd_elo_ratings(
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get Elo ratings data up to week 12 of the 2021 CFB season.
        print("Get Elo ratings data up to week 12 of the 2021 CFB season.")
        json_data = get_cfbd_elo_ratings(
            season=2020,
            week=12
        )
        print(json_data)
        time.sleep(5)

        # Get Elo ratings data for the 2020 CFB season, but only for games in the regular season.
        print("Get Elo ratings data for the 2020 CFB season, but only for games in the regular season.")
        json_data = get_cfbd_elo_ratings(
            season=2020,
            season_type="regular"
        )
        print(json_data)
        time.sleep(5)

        # Get historical Elo ratings data for the 
        # University of Cincinnati Football Team.
        print("Get historical Elo ratings data for the University of Cincinnati Football Team.")
        json_data = get_cfbd_elo_ratings(
            team="Cincinnati"
        )
        print(json_data)
        time.sleep(5)


        # Get Elo ratings data for teams competing in the 
        # Atlantic Coast Confrence (ACC) in the 2021 CFB season.
        print("Get Elo ratings data for teams competing in the Atlantic Coast Confrence (ACC) in the 2021 CFB season.")
        json_data = get_cfbd_elo_ratings(
            season=2021,
            conference_abv="ACC"
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_elo_ratings(
            season=2020, 
            team="Cincinnati",
            return_as_dict=True
        )
        print(json_data)
    ```
    Returns
    ----------
    A pandas `DataFrame` object with Elo ratings data,
    or (if `return_as_dict` is set to `True`)
    a dictionary object with a with Elo ratings data.

    """
    now = datetime.now()
    url = "https://api.collegefootballdata.com/ratings/elo"
    # row_df = pd.DataFrame()
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

    # if season == None and team == None:
    #     raise ValueError(
    #         "`season` and/or `team` must be set to a valid, "
    #         + "non-null value for this function to work."
    #     )

    if season != None and (season > (now.year + 1)):
        raise ValueError(f"`season` cannot be greater than {season}.")
    elif season != None and season < 1869:
        raise ValueError(f"`season` cannot be less than 1869.")
    


    # URL builder
    ########################################################################################################################################################################################################
    # Required by the API

    if season != None and team != None:
        url += f"?year={season}&team={team}"
    elif season != None:
        url += f"?year={season}"
    elif team != None:
        url += f"?team={team}"

    if week != None:
        url+=f"&week={week}"

    if conference_abv != None:
        url += f"&conference={conference_abv}"

    if season_type !=None:
        url+=f"&seasonType={season_type}"

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

    final_df = pd.json_normalize(json_data)

    final_df.rename(columns={"rating": "elo_rating"}, inplace=True)

    if week != None and len(final_df)>0:
        final_df["week"] = week
    return final_df


def get_cfbd_fpi_ratings(
    api_key: str = None,
    api_key_dir: str = None,
    season: int=None,
    week: int = None,
    team: str = None,
    conference_abv: str = None,
    return_as_dict: bool = False):
    """
    Allows you to get Football Power Index (FPI) ratings data 
    for CFB teams from the CFBD API.

    For more information about FPI, consult the following webpages:
    - https://www.espn.com/blog/statsinfo/post/_/id/122612/an-inside-look-at-college-fpi
    - https://thepowerrank.com/guide-cfb-rankings/

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
        Optional argument.
        Specifies the season you want FPI ratings data from.
        This must be specified, otherwise this package, and by extension
        the CFBD API, will not accept the request to get FPI ratings data.
        This or `team` must be set to a valid non-null variable for this to function.
    
    `week` (int, optional):
        Optional argument.
        If `week` is set to a valid, non-null integer,
        the CFBD API will return back Elo data for a team up to that week
        in a season.

    `team` (str, optional):
        Optional argument.
        Specifies the season you want FPI ratings data from.
        This must be specified, otherwise this package, and by extension
        the CFBD API, will not accept the request to get FPI ratings data.
        This or `season` must be set to a valid non-null variable for this to function.

    `conference_abv` (str, optional):
        Optional argument.
        If you only want FPI ratings data from games
        involving teams a specific confrence,
        set `conference_abv` to the abbreviation
        of the conference you want FPI ratings data from.

    `return_as_dict` (bool, semi-optional):
        Semi-optional argument.
        If you want this function to return the data as a dictionary (read: JSON object),
        instead of a pandas `DataFrame` object,
        set `return_as_dict` to `True`.

    Usage
    ----------
    ```
    import time

    from cfbd_json_py.ratings import get_cfbd_fpi_ratings


    cfbd_key = "tigersAreAwsome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwsome":
        print("Using the user's API key declared in this script for this example.")

        # Get FPI ratings data for the 2020 CFB season.
        print("Get FPI ratings data for the 2020 CFB season.")
        json_data = get_cfbd_fpi_ratings(
            api_key=cfbd_key, 
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get FPI ratings data up to week 12 of the 2021 CFB season.
        print("Get FPI ratings data up to week 12 of the 2021 CFB season.")
        json_data = get_cfbd_fpi_ratings(
            api_key=cfbd_key, 
            season=2020,
            week=12
        )
        print(json_data)
        time.sleep(5)

        # Get historical FPI ratings data for the 
        # University of Cincinnati Football Team.
        print("Get historical FPI ratings data for the University of Cincinnati Football Team.")
        json_data = get_cfbd_fpi_ratings(
            api_key=cfbd_key, 
            team="Cincinnati"
        )
        print(json_data)
        time.sleep(5)


        # Get FPI ratings data for teams competing in the 
        # Atlantic Coast Confrence (ACC) in the 2021 CFB season.
        print("Get FPI ratings data for teams competing in the Atlantic Coast Confrence (ACC) in the 2021 CFB season.")
        json_data = get_cfbd_fpi_ratings(
            api_key=cfbd_key, 
            season=2021,
            conference_abv="ACC"
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_fpi_ratings(
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
        print(
            "Using the user's API key suposedly loaded into this python environment for this example."
        )

        # Get FPI ratings data for the 2020 CFB season.
        print("Get FPI ratings data for the 2020 CFB season.")
        json_data = get_cfbd_fpi_ratings(
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get FPI ratings data up to week 12 of the 2021 CFB season.
        print("Get FPI ratings data up to week 12 of the 2021 CFB season.")
        json_data = get_cfbd_fpi_ratings(
            season=2020,
            week=12
        )
        print(json_data)
        time.sleep(5)



        # Get historical FPI ratings data for the 
        # University of Cincinnati Football Team.
        print("Get historical FPI ratings data for the University of Cincinnati Football Team.")
        json_data = get_cfbd_fpi_ratings(
            team="Cincinnati"
        )
        print(json_data)
        time.sleep(5)


        # Get FPI ratings data for teams competing in the 
        # Atlantic Coast Confrence (ACC) in the 2021 CFB season.
        print("Get FPI ratings data for teams competing in the Atlantic Coast Confrence (ACC) in the 2021 CFB season.")
        json_data = get_cfbd_fpi_ratings(
            season=2021,
            conference_abv="ACC"
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_fpi_ratings(
            season=2020, 
            team="Cincinnati",
            return_as_dict=True
        )
        print(json_data)


    ```
    Returns
    ----------
    A pandas `DataFrame` object with FPI ratings data,
    or (if `return_as_dict` is set to `True`)
    a dictionary object with a with FPI ratings data.

    """
    now = datetime.now()
    url = "https://api.collegefootballdata.com/ratings/fpi"
    # row_df = pd.DataFrame()
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

    if season == None and team == None:
        raise ValueError(
            "`season` and/or `team` must be set to a valid, "
            + "non-null value for this function to work."
        )

    if season != None and (season > (now.year + 1)):
        raise ValueError(f"`season` cannot be greater than {season}.")
    elif season != None and season < 1869:
        raise ValueError(f"`season` cannot be less than 1869.")

    # URL builder
    ########################################################################################################################################################################################################
    # Required by the API

    if season != None and team != None:
        url += f"?year={season}&team={team}"
    elif season != None:
        url += f"?year={season}"
    elif team != None:
        url += f"?team={team}"

    if week != None:
        url+=f"&week={week}"

    if conference_abv != None:
        url += f"&conference={conference_abv}"

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

    final_df = pd.json_normalize(json_data)

    final_df.rename(
        columns={
            "year":"season",
            "team":"team_name",
            "conference":"conference_name",
            "resumeRanks.strenghOfRecord":"resume_strength_of_record",
            "resumeRanks.fpi":"fpi_rank",
            "resumeRanks.averageWinProbability":"resume_avg_win_probability",
            "resumeRanks.strengthOfSchedule":"resume_strength_of_schedule",
            "resumeRanks.remaningStrengthOfSchedule":"resume_remaining_strength_of_schedule",
            "resumeRanks.gameControl":"resume_game_control",
            "efficiencies.overall":"efficiency_overall",
            "efficiencies.offense":"efficiency_offense",
            "efficiencies.defense":"efficiency_defense",
            "efficiencies.specialTeams":"efficiency_special_teams",
        },
        inplace=True
    )
    return final_df
