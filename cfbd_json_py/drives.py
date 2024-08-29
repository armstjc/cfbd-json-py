# Creation Date: 08/30/2023 01:13 EDT
# Last Updated Date: 08/13/2024 02:10 PM EDT
# Author: Joseph Armstrong (armstrongjoseph08@gmail.com)
# File Name: drives.py
# Purpose: Houses functions pertaining to CFB drive data within the CFBD API.
###############################################################################

import logging
from datetime import datetime

import pandas as pd
import requests

from cfbd_json_py.utls import get_cfbd_api_token


def get_cfbd_drives_info(
    api_key: str = None,
    api_key_dir: str = None,
    season: int = None,
    season_type: str = "regular",
    week: int = None,
    team: str = None,
    offensive_team: str = None,
    defensive_team: str = None,
    conference: str = None,
    offensive_conference: str = None,
    defensive_conference: str = None,
    ncaa_division: str = "fbs",
    year: int = None,
    offense: str = None,
    defense: str = None,
    classification: str = None,
    return_as_dict: bool = False,
):
    """
    Retrieves a list of CFB drives from the CFBD API.

    Parameters
    ----------
    `season` (int, mandatory):
        Required argument.
        Specifies the season you want CFB drive information from.
        This must be specified, otherwise this package, and by extension
        the CFBD API, will not accept the request to get CFB drive information.

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
        If you want CFB drive data for non-regular season games,
        set `season_type` to "postseason".
        If `season_type` is set to anything but "regular" or "postseason",
        a `ValueError()` will be raised.

    `week` (int, optional):
        Optional argument.
        If `week` is set to an integer, this function will attempt
        to load CFB drive data from games in that season, and that week.

    `team` (str, optional):
        Optional argument.
        If you only want CFB drive data for a team,
        regardless if they are the home/away team,
        set `team` to the name of the team you want CFB drive data from.

    `offensive_team` (str, optional):
        Optional argument.
        If you only want CFB drive data from a team, while they are on offense,
        regardless if they are the home/away team,
        set `team` to the name of the team you want CFB drive data from.

    `defensive_team` (str, optional):
        Optional argument.
        If you only want CFB drive data from a team, while they are on defense,
        regardless if they are the home/away team,
        set `team` to the name of the team you want CFB drive data from.

    `conference` (str, optional):
        Optional argument.
        If you only want CFB drive data from games
        involving teams from a specific conference,
        set `conference` to the abbreviation
        of the conference you want CFB drive data from.
        For a list of conferences,
        use the `cfbd_json_py.conferences.get_cfbd_conference_info()`
        function.

    `offensive_conference` (str, optional):
        Optional argument.
        If you only want CFB drive data from games
        where the offensive team is from a specific conference,
        set `conference` to the abbreviation
        of the conference you want CFB drive data from.
        For a list of conferences,
        use the `cfbd_json_py.conferences.get_cfbd_conference_info()`
        function.

    `defensive_conference` (str, optional):
        Optional argument.
        If you only want CFB drive data from games
        where the defensive team is from a specific conference,
        set `conference` to the abbreviation
        of the conference you want CFB drive data from.
        For a list of conferences,
        use the `cfbd_json_py.conferences.get_cfbd_conference_info()`
        function.

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

    `offense` (str):
        Alternative keyword for `offensive_team`

    `defense` (str):
        Alternative keyword for `defensive_team`

    `classification` (str):
        Alternative keyword for `ncaa_division`

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

    from cfbd_json_py.drives import get_cfbd_drives_info

    cfbd_key = "tigersAreAwesome"  # placeholder for your CFBD API Key.

    if cfbd_key is not "tigersAreAwesome":
        print(
            "Using the user's API key declared in this script " +
            "for this example."
        )

        # Get CFB Drive data from the 2020 CFB season.
        print("Get CFB Drive data from the 2020 CFB season.")
        json_data = get_cfbd_drives_info(
            api_key=cfbd_key,
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get CFB Drive data from week 10 of the 2020 CFB season.
        print("Get CFB Drive data from week 10 of the 2020 CFB season.")
        json_data = get_cfbd_drives_info(
            api_key=cfbd_key,
            season=2020,
            week=10
        )
        print(json_data)
        time.sleep(5)

        # Get CFB Drive data from games involving the 2020 Cincinnati Bearcats
        # Football Team.
        print(
            "Get CFB Drive data from games involving " +
            "the 2020 Cincinnati Bearcats Football Team."
        )
        json_data = get_cfbd_drives_info(
            api_key=cfbd_key,
            season=2020,
            team="Cincinnati"
        )
        print(json_data)
        time.sleep(5)

        # Get CFB Drive data from games involving the 2020 Ohio Bobcats
        # Football Team, when Ohio was on offense.
        print(
            "Get CFB Drive data from games involving " +
            "the 2020 Ohio Bobcats Football Team, when Ohio was on offense."
        )
        json_data = get_cfbd_drives_info(
            api_key=cfbd_key,
            season=2020,
            offensive_team="Ohio"
        )
        print(json_data)
        time.sleep(5)

        # Get CFB Drive data from games involving the 2020 Ohio State Buckeyes
        # Football Team, when Ohio was on offense.
        print(
            "Get CFB Drive data from games involving " +
            "the 2020 Ohio State Buckeyes Football Team, " +
            "when Ohio State was on defense."
        )
        json_data = get_cfbd_drives_info(
            api_key=cfbd_key,
            season=2020,
            defensive_team="Ohio State"
        )
        print(json_data)
        time.sleep(5)

        # Get CFB Drive data from Big 12 games in the 2020 CFB season.
        print(
            "Get CFB Drive data from games involving " +
            "the 2020 Ohio State Buckeyes Football Team, " +
            "when Ohio State was on defense."
        )
        json_data = get_cfbd_drives_info(
            api_key=cfbd_key,
            season=2020,
            conference="B12"
        )
        print(json_data)
        time.sleep(5)

        # Get CFB Drive data from Big 10 (B1G) games in the 2020 CFB season,
        # where the Big 10 team was on offense.
        print(
            "Get CFB Drive data from games involving " +
            "the 2020 Ohio State Buckeyes Football Team, " +
            "when Ohio State was on defense."
        )
        json_data = get_cfbd_drives_info(
            api_key=cfbd_key,
            season=2020,
            offensive_conference="B1G"
        )
        print(json_data)
        time.sleep(5)

        # Get CFB Drive data from  Mid-American Conference (MAC) games
        # in the 2020 CFB season, where the MAC team was on offense.
        print(
            "Get CFB Drive data from games involving " +
            "the 2020 Ohio State Buckeyes Football Team, " +
            "when Ohio State was on defense."
        )
        json_data = get_cfbd_drives_info(
            api_key=cfbd_key,
            season=2020,
            defensive_conference="MAC"
        )
        print(json_data)
        time.sleep(5)

        # Get CFB Drive data from Football Championship Subdivision (FCS) games
        # in week 3 of the 2020 CFB season,
        # where the MAC team was on offense.
        print(
            "Get CFB Drive data from games involving " +
            "the 2020 Ohio State Buckeyes Football Team, " +
            "when Ohio State was on defense."
        )
        json_data = get_cfbd_drives_info(
            api_key=cfbd_key,
            season=2020,
            week=3,
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
        json_data = get_cfbd_drives_info(
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

        # Get CFB Drive data from the 2020 CFB season.
        print("Get CFB Drive data from the 2020 CFB season.")
        json_data = get_cfbd_drives_info(
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get CFB Drive data from week 10 of the 2020 CFB season.
        print("Get CFB Drive data from week 10 of the 2020 CFB season.")
        json_data = get_cfbd_drives_info(
            season=2020,
            week=10
        )
        print(json_data)
        time.sleep(5)

        # Get CFB Drive data from games involving the 2020 Cincinnati Bearcats
        # Football Team.
        print(
            "Get CFB Drive data from games involving " +
            "the 2020 Cincinnati Bearcats Football Team."
        )
        json_data = get_cfbd_drives_info(
            season=2020,
            team="Cincinnati"
        )
        print(json_data)
        time.sleep(5)

        # Get CFB Drive data from games involving the 2020 Ohio Bobcats
        # Football Team, when Ohio was on offense.
        print(
            "Get CFB Drive data from games involving " +
            "the 2020 Ohio Bobcats Football Team, when Ohio was on offense."
        )
        json_data = get_cfbd_drives_info(
            season=2020,
            offensive_team="Ohio"
        )
        print(json_data)
        time.sleep(5)

        # Get CFB Drive data from games involving the 2020 Ohio State Buckeyes
        # Football Team, when Ohio was on offense.
        print(
            "Get CFB Drive data from games involving " +
            "the 2020 Ohio State Buckeyes Football Team, " +
            "when Ohio State was on defense."
        )
        json_data = get_cfbd_drives_info(
            season=2020,
            defensive_team="Ohio State"
        )
        print(json_data)
        time.sleep(5)

        # Get CFB Drive data from Big 12 games in the 2020 CFB season.
        print(
            "Get CFB Drive data from games involving " +
            "the 2020 Ohio State Buckeyes Football Team, " +
            "when Ohio State was on defense."
        )
        json_data = get_cfbd_drives_info(
            season=2020,
            conference="B12"
        )
        print(json_data)
        time.sleep(5)

        # Get CFB Drive data from Big 10 (B1G) games in the 2020 CFB season,
        # where the Big 10 team was on offense.
        print(
            "Get CFB Drive data from games involving " +
            "the 2020 Ohio State Buckeyes Football Team, " +
            "when Ohio State was on defense."
        )
        json_data = get_cfbd_drives_info(
            season=2020,
            offensive_conference="B1G"
        )
        print(json_data)
        time.sleep(5)

        # Get CFB Drive data from  Mid-American Conference (MAC) games
        # in the 2020 CFB season, where the MAC team was on offense.
        print(
            "Get CFB Drive data from games involving " +
            "the 2020 Ohio State Buckeyes Football Team, " +
            "when Ohio State was on defense."
        )
        json_data = get_cfbd_drives_info(
            season=2020,
            defensive_conference="MAC"
        )
        print(json_data)
        time.sleep(5)

        # Get CFB Drive data from Football Championship Subdivision (FCS) games
        # in week 3 of the 2020 CFB season,
        # where the MAC team was on offense.
        print(
            "Get CFB Drive data from games involving " +
            "the 2020 Ohio State Buckeyes Football Team, " +
            "when Ohio State was on defense."
        )
        json_data = get_cfbd_drives_info(
            season=2020,
            week=3,
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
        json_data = get_cfbd_drives_info(
            season=2020,
            week=10,
            return_as_dict=True
        )
        print(json_data)

    ```

    Returns
    ----------
    A pandas `DataFrame` object with CFB drive data,
    or (if `return_as_dict` is set to `True`)
    a dictionary object with CFB drive data.

    """
    now = datetime.now()
    cfb_drives_df = pd.DataFrame()
    # row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/drives"

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

    # `offense` to `offensive_team`
    if (
        offense is not None
        and offensive_team is not None
        and (offense is not offensive_team)
    ):
        raise ValueError(
            "When using this function, "
            + "please specify a season in EITHER "
            + "`offense` or `offensive_team`."
        )
    if offensive_team is not None:
        pass
    elif offense is not None:
        offensive_team = offense

    # `defense` to `defensive_team`
    if (
        defense is not None
        and defensive_team is not None
        and (defense is not defensive_team)
    ):
        raise ValueError(
            "When using this function, "
            + "please specify a season in EITHER "
            + "`defense` or `defensive_team`."
        )
    if defensive_team is not None:
        pass
    elif defense is not None:
        defensive_team = defense

    # `classification` to `ncaa_division`
    if (
        classification is not None
        and ncaa_division is not None
        and (classification is not ncaa_division)
    ):
        raise ValueError(
            "When using this function, "
            + "please specify a season in EITHER "
            + "`classification` or `ncaa_division`."
        )
    if ncaa_division is not None:
        pass
    elif defense is not None:
        ncaa_division = classification

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
            '`season_type` must be set to either ' +
            '"regular" or "postseason" for this function to work.'
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
            + f"\n\nYou entered:\n{ncaa_division}"
        )

    # URL builder
    ##########################################################################

    # Required by API
    url += f"?seasonType={season_type}"

    url += f"&year={season}"

    if week is not None:
        url += f"&week={week}"

    if team is not None:
        url += f"&team={team}"

    if offensive_team is not None:
        url += f"&offense={offensive_team}"

    if defensive_team is not None:
        url += f"&defense={defensive_team}"

    if conference is not None:
        url += f"&conference={conference}"

    if offensive_conference is not None:
        url += f"&offenseConference={offensive_conference}"

    if defensive_conference is not None:
        url += f"&defenseConference={defensive_conference}"

    if ncaa_division is not None:
        url += f"&classification={ncaa_division.lower()}"

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

    cfb_drives_df = pd.json_normalize(json_data)
    cfb_drives_df.to_csv("test.csv")
    # print(cfb_drives_df.columns)
    cfb_drives_df.rename(
        columns={
            "offense": "offense_team_name",
            "offense_conference": "offense_conference_name",
            "defense": "defense_name",
            "defense_conference": "defense_conference_name",
            "id": "drive_id",
            "scoring": "is_scoring_drive",
            "start_time.minutes": "start_time_minutes",
            "start_time.seconds": "start_time_seconds",
            "end_time.minutes": "end_time_minutes",
            "end_time.seconds": "end_time_seconds",
            "elapsed.minutes": "elapsed_minutes",
            "elapsed.seconds": "elapsed_seconds",
        },
        inplace=True,
    )
    if len(cfb_drives_df) == 0:
        logging.error(
            "The CFBD API accepted your inputs, "
            + "but found no data within your specified input parameters."
            + " Please double check your input parameters."
        )

    return cfb_drives_df
