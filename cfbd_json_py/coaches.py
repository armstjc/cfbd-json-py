# Creation Date: 08/30/2023 01:13 EDT
# Last Updated Date: 08/13/2024 02:10 PM EDT
# Author: Joseph Armstrong (armstrongjoseph08@gmail.com)
# File Name: coaches.py
# Purpose: Houses functions pertaining to coaching data within the CFBD API.
###############################################################################

import logging
import warnings

import pandas as pd
import requests
from tqdm import tqdm

from cfbd_json_py.utls import get_cfbd_api_token


def get_cfbd_coaches_info(
    api_key: str = None,
    api_key_dir: str = None,
    first_name: str = None,
    last_name: str = None,
    team: str = None,
    season: int = None,
    min_season: int = None,
    max_season: int = None,
    year: int = None,
    return_as_dict: bool = False,
):
    """
    Retrieves information from the CFBD API on CFB Head Coaches.

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

    `first_name` (str, optional):
        Optional argument.
        If you want to only look up coaches with a specific first name,
        set this variable to that specific first name, and this function
        will attempt to look up coaches with that specific first name.

    `last_name` (str, optional):
        Optional argument.
        If you want to only look up coaches with a specific last name,
        set this variable to that specific first name, and this function
        will attempt to look up coaches with that specific last name.

    `team` (str, optional):
        Optional argument.
        If you want to filter and drill down to coaches who coached a specific
        CFB team, set this

    `season` (int, optional):
        Optional argument.
        If you only want coaches from a specific season,
        set this variable to that season.

    `min_season` (int, optional):
        Optional argument.
        Similar to `year`, but used in tandem with `max_season`
        to get coaches who coached with in a range of seasons.

    `max_season` (int, optional):
        Optional argument.
        Similar to `year`, but used in tandem with `min_season`
        to get coaches who coached with in a range of seasons.

    `year` (int):
        Alternative keyword for `season`

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

    from cfbd_json_py.coaches import get_cfbd_coaches_info

    cfbd_key = "tigersAreAwesome"  # placeholder for your CFBD API Key.

    if cfbd_key is not "tigersAreAwesome":
        print(
            "Using the user's API key declared in this script "+
            "for this example."
        )

        # Getting all coaches in the 2020 CFB season
        print("Getting every coach in the 2020 CFB season.")
        json_data = get_cfbd_coaches_info(
            api_key=cfbd_key,
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Getting all coaches in the 2020 CFB season,
        # with a first name of "Luke"
        print(
            "Getting every coach in the 2020 CFB season, "+
            "with a first name of \"Luke\"."
        )
        json_data = get_cfbd_coaches_info(
            api_key=cfbd_key,
            season=2020,
            first_name="Luke"
        )
        print(json_data)
        time.sleep(5)

        # Getting all coaches in the 2020 CFB season, with a last name of "Day"
        print(
            "Getting all coaches in the 2020 CFB season, " +
            "with a last name of \"Day\"."
        )
        json_data = get_cfbd_coaches_info(
            api_key=cfbd_key,
            season=2020,
            last_name="Day"
        )
        print(json_data)
        time.sleep(5)

        # Getting every head coach for
        # the 2020 Southern Mississippi Golden Eagles
        print(
            "Getting every head coach for " +
            "the 2020 Southern Mississippi Golden Eagles."
        )
        json_data = get_cfbd_coaches_info(
            api_key=cfbd_key,
            season=2020,
            team="Southern Mississippi"
        )
        print(json_data)
        time.sleep(5)

        # Getting every head coach between the 2019 and 2022 CFB seasons
        print("Getting every head coach between the 2019 and 2022 CFB seasons")
        json_data = get_cfbd_coaches_info(
            api_key=cfbd_key,
            min_season=2019,
            max_season=2022
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call
        # as a Dictionary (read: JSON) object.
        print(
            "You can also tell this function to just return the API call " +
            "as a Dictionary (read: JSON) object."
        )
        json_data = get_cfbd_coaches_info(
            api_key=cfbd_key,
            season=2022,
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

        # Getting every coach in the 2020 CFB season.
        print("Getting every coach in the 2020 CFB season.")
        json_data = get_cfbd_coaches_info(season=2020)
        print(json_data)
        time.sleep(5)


        # Getting every coach in the 2020 CFB season,
        # with a first name of "Luke".
        print(
            "Getting every coach in the 2020 CFB season, " +
            "with a first name of \"Luke\"."
        )
        json_data = get_cfbd_coaches_info(
            season=2020,
            first_name="Luke"
        )
        print(json_data)
        time.sleep(5)

        # Getting every coach in the 2020 CFB season,
        # with a last name of "Day".
        print(
            "Getting every coach in the 2020 CFB season, " +
            "with a last name of \"Day\"."
        )
        json_data = get_cfbd_coaches_info(
            season=2020,
            last_name="Day"
        )
        print(json_data)
        time.sleep(5)

        # Getting every head coach for
        # the 2020 Southern Mississippi Golden Eagles.
        print(
            "Getting every head coach for the " +
            "2020 Southern Mississippi Golden Eagles."
        )
        json_data = get_cfbd_coaches_info(
            season=2020,
            team="Southern Mississippi"
        )
        print(json_data)
        time.sleep(5)

        # Getting every head coach between the 2019 and 2022 CFB seasons.
        print(
            "Getting every head coach between the 2019 and 2022 CFB seasons."
        )
        json_data = get_cfbd_coaches_info(
            min_season=2019,
            max_season=2022
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call
        # as a Dictionary (read: JSON) object.
        print(
            "You can also tell this function to just return the API call " +
            "as a Dictionary (read: JSON) object."
        )
        json_data = get_cfbd_coaches_info(
            season=2022,
            team="Cincinnati",
            return_as_dict=True
        )
        print(json_data)

    ```
    Returns
    ----------
    A pandas `DataFrame` object with CFB head coach data,
    or (if `return_as_dict` is set to `True`)
    a dictionary object with CFB head coach data.
    """
    warnings.simplefilter(action="ignore", category=FutureWarning)

    coaches_df = pd.DataFrame()
    row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/coaches"

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

    if min_season is not None and max_season is None:
        if season is not None and min_season is not season:
            raise LookupError(
                "It is ambiguous which year you want coaching information "
                + "from, because you set the following values "
                + "for the following variables:"
                + f"\n- `year`: {season}"
                + f"\n- `min_season`: {min_season}"
                + f"\n`max_season`: {max_season}"
                + "\nIf you want to get coaches who coached in "
                + "a specified range of seasons, "
                + "set `min_season` and `max_season` to the range of seasons "
                + "you want coaching information from."
            )
        elif season is not None and min_season is season:
            logging.warning(
                "If you only want coaching information for a single season, "
                + "and not for a range of seasons, only set `year` "
                + "to the season you want coaching info for, "
                + "and leave `min_season` and `max_season` as `None` (NULL)."
            )
            min_season = None
        elif season is None:
            logging.warning(
                "If you only want coaching information for a single season, "
                + "and not for a range of seasons, only set `year` to "
                + "the season you want coaching info for, "
                + "and leave `min_season` and `max_season` as `None` (NULL)."
            )
            season = min_season
            min_season = None

    elif min_season is None and max_season is not None:
        if season is not None and max_season is not season:
            raise LookupError(
                "It is ambiguous which year you want "
                + "coaching information from, "
                + "because you set the following values "
                + "for the following variables:"
                + f"\n- `year`: {season}"
                + f"\n- `min_season`: {min_season}"
                + f"\n`max_season`: {max_season}"
                + "\nIf you want to get coaches who coached "
                + "in a specified range of seasons, "
                + "set `min_season` and `max_season` to the range of seasons "
                + "you want coaching information from."
            )
        elif season is not None and max_season == season:
            logging.warning(
                "If you only want coaching information for "
                + "a single season, and not for a range of seasons, "
                + "only set `year` to the season you want coaching info for, "
                + "and leave `min_season` and `max_season` as `None` (NULL)."
            )
            min_season = None
        elif season is None:
            logging.warning(
                "If you only want coaching information for "
                + "a single season, and not for a range of seasons, "
                + "only set `year` to the season you want coaching info for, "
                + "and leave `min_season` and `max_season` as `None` (NULL)."
            )
            season = max_season
            max_season = None

    if min_season is not None and max_season is not None:
        if season is not None:
            raise LookupError(
                "It is ambiguous which year you want "
                + "coaching information from, because you set "
                + "the following values for the following variables:"
                + f"\n- `year`: {season}"
                + f"\n- `min_season`: {min_season}"
                + f"\n`max_season`: {max_season}"
                + "\nIf you want to get coaches who coached in "
                + "a specified range of seasons, "
                + "set `min_season` and `max_season` to the range of "
                + "seasons you want coaching information from."
            )
        elif min_season > max_season:
            raise ValueError(
                "`min_season` cannot be greater than `max_season`."
            )

    # URL builder
    ##########################################################################

    url_elements = 0

    if first_name is not None and url_elements == 0:
        url += f"?firstName={first_name}"
        url_elements += 1
    elif first_name is not None:
        url += f"&firstName={first_name}"
        url_elements += 1

    if last_name is not None and url_elements == 0:
        url += f"?lastName={last_name}"
        url_elements += 1
    elif last_name is not None:
        url += f"&lastName={last_name}"
        url_elements += 1

    if team is not None and url_elements == 0:
        url += f"?team={team}"
        url_elements += 1
    elif team is not None:
        url += f"&team={team}"
        url_elements += 1

    if season is not None:
        if season is not None and url_elements == 0:
            url += f"?year={season}"
            url_elements += 1
        elif season is not None:
            url += f"&year={season}"
            url_elements += 1

    elif min_season is not None and max_season is not None:
        if url_elements == 0:
            url += f"?minYear={min_season}&maxYear={max_season}"
            url_elements += 1
        else:
            url += f"&minYear={min_season}&maxYear={max_season}"
            url_elements += 1

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

    for coach in tqdm(json_data):
        coach_first_name = coach["first_name"]
        coach_last_name = coach["last_name"]
        coach_hire_date = coach["hire_date"]

        row_df = pd.json_normalize(coach["seasons"])
        row_df["coach_first_name"] = coach_first_name
        row_df["coach_last_name"] = coach_last_name
        row_df["coach_hire_date"] = coach_hire_date

        coaches_df = pd.concat([coaches_df, row_df], ignore_index=True)

        del coach_first_name, coach_last_name, coach_hire_date
    # coaches_df = pd.json_normalize(json_data)
    return coaches_df
