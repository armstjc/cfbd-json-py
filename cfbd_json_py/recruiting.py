# Creation Date: 08/30/2023 01:13 EDT
# Last Updated Date: 08/13/2024 02:10 PM EDT
# Author: Joseph Armstrong (armstrongjoseph08@gmail.com)
# File Name: recruiting.py
# Purpose: Houses functions pertaining to CFB recruiting data
#    within the CFBD API.
###############################################################################

import logging
from datetime import datetime

import pandas as pd
import requests

from cfbd_json_py.utls import get_cfbd_api_token


def get_cfbd_player_recruit_ratings(
    api_key: str = None,
    api_key_dir: str = None,
    season: int = None,
    team: str = None,
    # `year` and/or `team` need to be not null for this function to work.
    recruit_classification: str = None,
    # Can be "HighSchool", "JUCO", or "PrepSchool"
    position: str = None,
    state: str = None,
    return_as_dict: bool = False,
):
    """
    Allows you to get CFB player recruiting data from the CFBD API.

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
        Specifies the season you want CFB recruiting data from.
        This must be specified, otherwise this package, and by extension
        the CFBD API, will not accept the request to get CFB recruiting data.
        This or `team` must be set to a valid non-null variable
        for this to function.

    `team` (str, semi-mandatory):
        Semi-required argument.
        Specifies the season you want CFB recruiting data from.
        This must be specified, otherwise this package, and by extension
        the CFBD API, will not accept the request to get CFB recruiting data.
        This or `season` must be set to a valid non-null variable
        for this to function.

    `recruit_classification` (str, optional):
        Optional argument.
        By default, this is sent to `None`,
        so one can get all recruits from a given season and/or team.

        If you want to filter by what type of recruit,
        the following values are valid for `recruit_classification`:
        - `HighSchool`: Exactly what it says on the tin. These are HS recruits.
        - `JUCO`: JUnior COllege recruits.
            These are recruits who are transferring from a
            junior college to an NCAA college.
        - `PrepSchool`: College Prep school recruits.
            These are recruits from places such as
            the Fork Union Military Academy in Fort Union, VA
            or Palmetto Prep in Columbia, SC.

    `position` (str, optional):
        Optional argument.
        If you ony want recruits from a specific position,
        set `position` to that position's acronym.
        Acronyms such as `DUAL` for "DUAL-threat QBs"
        and `APB` for "All-Purpose running Backs" are valid inputs.

    `state` (str, optional):
        Optional argument.
        If you only want recruits from a specific state in the United Sates,
        set `state` to he USPS abbreviation of that state
        (like `OH` for Ohio, or `IN` for Indiana).

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

    from cfbd_json_py.recruiting import get_cfbd_player_recruit_ratings


    cfbd_key = "tigersAreAwesome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwesome":
        print(
            "Using the user's API key declared in this script " +
            "for this example."
        )

        # Get a list of all recruits for the 2020 recruiting class.
        print("Get a list of all recruits for the 2020 recruiting class.")
        json_data = get_cfbd_player_recruit_ratings(
            api_key=cfbd_key,
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get a list of all recruits from
        # the 2020 Ohio State Buckeyes recruiting class.
        print(
            "Get a list of all recruits from " +
            "the 2020 Ohio State Buckeyes recruiting class."
        )
        json_data = get_cfbd_player_recruit_ratings(
            api_key=cfbd_key,
            season=2020,
            team="Ohio State"
        )
        print(json_data)
        time.sleep(5)

        # Get a list of all recruits JUCO recruits for
        # the 2019 recruiting class.
        print(
            "Get a list of all recruits JUCO recruits for " +
            "the 2019 recruiting class."
        )
        json_data = get_cfbd_player_recruit_ratings(
            api_key=cfbd_key,
            season=2019,
            recruit_classification="JUCO"
        )
        print(json_data)
        time.sleep(5)

        # Get a list of all wide receiver recruits
        # from the 2018 recruiting class.
        print(
            "Get a list of all wide receiver recruits " +
            "from the 2018 recruiting class."
        )
        json_data = get_cfbd_player_recruit_ratings(
            api_key=cfbd_key,
            season=2020,
            position="WR"
        )
        print(json_data)
        time.sleep(5)

        # Get a list of all recruits from
        # the state of Idaho in the 2017 recruiting class.
        print(
            "Get a list of all recruits " +
            "from the state of Idaho in the 2017 recruiting class."
        )
        json_data = get_cfbd_player_recruit_ratings(
            api_key=cfbd_key,
            season=2020,
            state="ID"
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print(
            "You can also tell this function to just return the API call " +
            "as a Dictionary (read: JSON) object."
        )
        json_data = get_cfbd_player_recruit_ratings(
            api_key=cfbd_key,
            season=2020,
            team="Ohio",
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


        # Get a list of all recruits for the 2020 recruiting class.
        print("Get a list of all recruits for the 2020 recruiting class.")
        json_data = get_cfbd_player_recruit_ratings(
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get a list of all recruits from
        # the 2020 Ohio State Buckeyes recruiting class.
        print(
            "Get a list of all recruits from " +
            "the 2020 Ohio State Buckeyes recruiting class."
        )
        json_data = get_cfbd_player_recruit_ratings(
            season=2020,
            team="Ohio State"
        )
        print(json_data)
        time.sleep(5)

        # Get a list of all recruits JUCO recruits for
        # the 2019 recruiting class.
        print(
            "Get a list of all recruits JUCO recruits for " +
            "the 2019 recruiting class."
        )
        json_data = get_cfbd_player_recruit_ratings(
            season=2019,
            recruit_classification="JUCO"
        )
        print(json_data)
        time.sleep(5)

        # Get a list of all wide receiver recruits
        # from the 2018 recruiting class.
        print(
            "Get a list of all wide receiver recruits " +
            "from the 2018 recruiting class."
        )
        json_data = get_cfbd_player_recruit_ratings(
            season=2020,
            position="WR"
        )
        print(json_data)
        time.sleep(5)

        # Get a list of all recruits from
        # the state of Idaho in the 2017 recruiting class.
        print(
            "Get a list of all recruits " +
            "from the state of Idaho in the 2017 recruiting class."
        )
        json_data = get_cfbd_player_recruit_ratings(
            season=2020,
            state="ID"
        )
        print(json_data)
        time.sleep(5)


        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print(
            "You can also tell this function to just return the API call " +
            "as a Dictionary (read: JSON) object."
        )
        json_data = get_cfbd_player_recruit_ratings(
            season=2020,
            team="Ohio",
            return_as_dict=True
        )
        print(json_data)
    ```
    Returns
    ----------
    A pandas `DataFrame` object with CFB team recruiting ratings,
    or (if `return_as_dict` is set to `True`)
    a dictionary object with CFB team recruiting ratings.

    """

    now = datetime.now()
    recruit_df = pd.DataFrame()
    # row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/recruiting/players"

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

    if season > (now.year + 1):
        raise ValueError(f"`season` cannot be greater than {season}.")
    elif season < 1869:
        raise ValueError("`season` cannot be less than 1869.")

    if (
        recruit_classification == "HighSchool"
        or recruit_classification == "JUCO"
        or recruit_classification == "PrepSchool"
    ):
        logging.info("Correct `recruit_classification` inputted.")
    elif recruit_classification is None:
        logging.info(
            "`recruit_classification` is skipped in this function call."
        )
    else:
        raise ValueError(
            "`recruit_classification` must be set "
            + "to one of the following values "
            + "\n\t- `HighSchool`"
            + "\n\t- `JUCO`"
            + "\n\t- `PrepSchool`"
        )

    if season is None and team is None:
        raise ValueError(
            "`season` and/or `team` must be set to "
            + "valid non-null values for this function to work."
        )

    # URL builder
    ##########################################################################

    # Required by API
    if team is not None and season is None:
        url += f"?team={team}"
    elif season is not None and team is None:
        url += f"?year={season}"
    elif season is not None and team is not None:
        url += f"?year={season}&team={team}"

    if recruit_classification is not None:
        url += f"&classification={recruit_classification}"

    if position is not None:
        url += f"&position={position}"

    if state is not None:
        url += f"&state={state}"

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

    # for player in tqdm(json_data):
    #     pass
    recruit_df = pd.json_normalize(json_data)

    recruit_df.rename(
        columns={
            "id": "recruit_id",
            "athleteId": "athlete_id",
            "recruitType": "recruit_type",
            "year": "season",
            "name": "player_name",
            "school": "previous_school",
            "committedTo": "college_commit_team",
            "stateProvince": "state_province",
            "hometownInfo.latitude": "hometown_latitude",
            "hometownInfo.longitude": "hometown_longitude",
            "hometownInfo.fipsCode": "hometown_fips_code",
        },
        inplace=True,
    )

    return recruit_df


def get_cfbd_team_recruiting_ratings(
    api_key: str = None,
    api_key_dir: str = None,
    season: int = None,
    team: str = None,
    return_as_dict: bool = False,
):
    """
    Allows you to get CFB team recruiting rankings data from the CFBD API.

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
        Specifies the season you want CFB recruiting data from.
        This must be specified, otherwise this package, and by extension
        the CFBD API, will not accept the request to get CFB recruiting data.
        This or `team` must be set to a valid non-null variable
        for this to function.

    `team` (str, semi-mandatory):
        Semi-required argument.
        Specifies the season you want CFB recruiting data from.
        This must be specified, otherwise this package, and by extension
        the CFBD API, will not accept the request to get CFB recruiting data.
        This or `season` must be set to a valid non-null variable
        for this to function.

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

    from cfbd_json_py.recruiting import get_cfbd_team_recruiting_ratings


    cfbd_key = "tigersAreAwesome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwesome":
        print(
            "Using the user's API key declared in this script " +
            "for this example."
        )

        # Get a team recruiting rankings for the 2020 CFB season.
        print("Get a team recruiting rankings for the 2020 CFB season.")
        json_data = get_cfbd_team_recruiting_ratings(
            api_key=cfbd_key,
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get a historical team recruiting rankings for
        # the Ohio State Buckeyes Football team.
        print(
            "Get a historical team recruiting rankings for " +
            "the Ohio State Buckeyes Football team."
        )
        json_data = get_cfbd_team_recruiting_ratings(
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
        json_data = get_cfbd_team_recruiting_ratings(
            api_key=cfbd_key,
            season=2020,
            team="Ohio",
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


        # Get a team recruiting rankings for the 2020 CFB season.
        print("Get a team recruiting rankings for the 2020 CFB season.")
        json_data = get_cfbd_team_recruiting_ratings(
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get a historical team recruiting rankings for
        # the Ohio State Buckeyes Football team.
        print(
            "Get a historical team recruiting rankings for " +
            "the Ohio State Buckeyes Football team."
        )
        json_data = get_cfbd_team_recruiting_ratings(
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
        json_data = get_cfbd_team_recruiting_ratings(
            season=2020,
            team="Ohio",
            return_as_dict=True
        )
        print(json_data)

    ```
    Returns
    ----------
    A pandas `DataFrame` object with CFB Poll data,
    or (if `return_as_dict` is set to `True`)
    a dictionary object with CFB Poll data.
    """

    now = datetime.now()
    recruit_df = pd.DataFrame()
    # row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/recruiting/teams"

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

    if season is not None and season > (now.year + 1):
        raise ValueError(f"`season` cannot be greater than {season}.")
    elif season is not None and season < 1869:
        raise ValueError("`season` cannot be less than 1869.")

    if season is None and team is None:
        raise ValueError(
            "`season` and/or `team` must be set to "
            + "valid non-null values for this function to work."
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

    # for player in tqdm(json_data):
    #     pass
    recruit_df = pd.json_normalize(json_data)

    return recruit_df


def get_cfbd_team_recruiting_group_ratings(
    api_key: str = None,
    api_key_dir: str = None,
    start_season: int = None,
    end_season: int = None,
    team: str = None,
    conference: str = None,
    return_as_dict: bool = False,
):
    """
    Allows you to get CFB player recruiting data,
    grouped by the team and position,
    from the CFBD API.

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

    `start_season` (int, optional):
        Optional argument.
        If `start_season` is set to a valid integer,
        the API will filter out every recruiting season that
        is less than `start_season`.

    `end_season` (int, optional):
        Optional argument.
        If `start_season` is set to a valid integer,
        the API will filter out every recruiting season that
        is greater than `end_season`.

    `team` (str, semi-mandatory):
        Semi-required argument.
        Specifies the season you want CFB recruiting data from.
        This must be specified, otherwise this package, and by extension
        the CFBD API, will not accept the request to get CFB recruiting data.
        This or `season` must be set to a valid non-null variable
        for this to function.

    `conference` (str, optional):
        Optional argument.
        If you only want CFB recruiting data
        from teams in a specific conference,
        set `conference` to the abbreviation
        of the conference you want CFB recruiting data from.
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

    from cfbd_json_py.recruiting import get_cfbd_team_recruiting_group_ratings


    cfbd_key = "tigersAreAwesome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwesome":
        print(
            "Using the user's API key declared in this script " +
            "for this example."
        )

        # Get recruiting data between 2020 and 2023,
        # grouped by team and position.
        print(
            "Get recruiting data between 2020 and 2023, " +
            "grouped by team and position."
        )
        json_data = get_cfbd_team_recruiting_group_ratings(
            api_key=cfbd_key,
            start_season=2020,
            end_season=2023
        )
        print(json_data)
        time.sleep(5)

        # Get recruiting data between 2020 and 2023,
        # grouped by team and position,
        # for the Ohio State Buckeyes Football team.
        print(
            "Get recruiting data between 2020 and 2023, " +
            "grouped by team and position, " +
            "for the Ohio State Buckeyes Football team."
        )
        json_data = get_cfbd_team_recruiting_group_ratings(
            api_key=cfbd_key,
            start_season=2020,
            end_season=2023,
            team="Ohio State"
        )
        print(json_data)
        time.sleep(5)

        # Get recruiting data starting in 2020,
        # grouped by team and position.
        print(
            "Get recruiting data starting in 2020, " +
            "grouped by team and position."
        )
        json_data = get_cfbd_team_recruiting_group_ratings(
            api_key=cfbd_key,
            start_season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get recruiting data ending in 2018,
        # grouped by team and position.
        print(
            "Get recruiting data ending in 2018, grouped by team and position."
        )
        json_data = get_cfbd_team_recruiting_group_ratings(
            api_key=cfbd_key,
            start_season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get recruiting data starting in 2020,
        # grouped by team and position,
        # but only for Mountain West conference (MWC) teams.
        print(
            "Get recruiting data starting in 2020, " +
            "grouped by team and position, " +
            "but only for Mountain West conference (MWC) teams."
        )
        json_data = get_cfbd_team_recruiting_group_ratings(
            api_key=cfbd_key,
            start_season=2020,
            conference="MWC"
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print(
            "You can also tell this function to just return the API call " +
            "as a Dictionary (read: JSON) object."
        )
        json_data = get_cfbd_team_recruiting_group_ratings(
            api_key=cfbd_key,
            start_season=2020,
            end_season=2023,
            team="Ohio",
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


        # Get recruiting data between 2020 and 2023,
        # grouped by team and position.
        print(
            "Get recruiting data between 2020 and 2023, " +
            "grouped by team and position."
        )
        json_data = get_cfbd_team_recruiting_group_ratings(
            start_season=2020,
            end_season=2023
        )
        print(json_data)
        time.sleep(5)

        # Get recruiting data between 2020 and 2023,
        # grouped by team and position,
        # for the Ohio State Buckeyes Football team.
        print(
            "Get recruiting data between 2020 and 2023, " +
            "grouped by team and position, " +
            "for the Ohio State Buckeyes Football team."
        )
        json_data = get_cfbd_team_recruiting_group_ratings(
            start_season=2020,
            end_season=2023,
            team="Ohio State"
        )
        print(json_data)
        time.sleep(5)

        # Get recruiting data starting in 2020,
        # grouped by team and position.
        print(
            "Get recruiting data starting in 2020, " +
            "grouped by team and position."
        )
        json_data = get_cfbd_team_recruiting_group_ratings(
            start_season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get recruiting data ending in 2018,
        # grouped by team and position.
        print(
            "Get recruiting data ending in 2018, grouped by team and position."
        )
        json_data = get_cfbd_team_recruiting_group_ratings(
            end_season=2018
        )
        print(json_data)
        time.sleep(5)

        # Get recruiting data starting in 2020,
        # grouped by team and position,
        # but only for Mountain West conference (MWC) teams.
        print(
            "Get recruiting data starting in 2020, " +
            "grouped by team and position, " +
            "but only for Mountain West conference (MWC) teams."
        )
        json_data = get_cfbd_team_recruiting_group_ratings(
            start_season=2020,
            conference="MWC"
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print(
            "You can also tell this function to just return the API call " +
            "as a Dictionary (read: JSON) object."
        )
        json_data = get_cfbd_team_recruiting_group_ratings(
            start_season=2020,
            end_season=2023,
            team="Ohio",
            return_as_dict=True
        )
        print(json_data)
    ```
    Returns
    ----------
    A pandas `DataFrame` object with CFB team recruiting ratings,
    or (if `return_as_dict` is set to `True`)
    a dictionary object with CFB team recruiting ratings.
    """
    now = datetime.now()
    recruit_df = pd.DataFrame()
    # row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/recruiting/groups"

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

    if start_season is not None and start_season > (now.year + 1):
        raise ValueError(f"`season` cannot be greater than {start_season}.")
    elif start_season is not None and start_season < 1869:
        raise ValueError("`season` cannot be less than 1869.")

    if end_season is not None and end_season > (now.year + 1):
        raise ValueError(f"`season` cannot be greater than {end_season}.")
    elif end_season is not None and end_season < 1869:
        raise ValueError("`season` cannot be less than 1869.")

    # URL builder
    ##########################################################################

    url_elements = 0

    if start_season is not None and url_elements == 0:
        url += f"?startYear={start_season}"
        url_elements += 1
    elif start_season is not None:
        url += f"&startYear={start_season}"
        url_elements += 1

    if end_season is not None and url_elements == 0:
        url += f"?endYear={end_season}"
        url_elements += 1
    elif end_season is not None:
        url += f"&endYear={end_season}"
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

    # for player in tqdm(json_data):
    #     pass
    recruit_df = pd.json_normalize(json_data)

    return recruit_df
