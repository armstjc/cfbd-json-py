# Creation Date: 08/30/2023 01:13 EDT
# Last Updated Date: 11/04/2023 02:55 PM EDT
# Author: Joseph Armstrong (armstrongjoseph08@gmail.com)
# File Name: drives.py
# Purpose: Houses functions pertaining to CFB drive data within the CFBD API.
####################################################################################################

from datetime import datetime
import logging
import pandas as pd
import requests
from tqdm import tqdm

from cfbd_json_py.utls import get_cfbd_api_token


def get_cfbd_drives_info(
        season: int,
        api_key: str = None,
        api_key_dir: str = None,
        season_type: str = "regular",
        week: int = None,
        team: str = None,
        offensive_team: str = None,
        defensive_team: str = None,
        conference_abv: str = None,
        offensive_conference_abv: str = None,
        defensive_conference_abv: str = None,
        ncaa_division: str = "fbs",
        return_as_dict: bool = False):
    """
    Retrives a list of CFB drives from the CFBD API.

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

    `conference_abv` (str, optional):
        Optional argument.
        If you only want CFB drive data from games 
        involving teams from a specific confrence, 
        set `conference_abv` to the abbreviation 
        of the conference you want CFB drive data from.
        For a list of confrences, 
        use the `cfbd_json_py.conferences.get_cfbd_conference_info()`
        function.

    `offensive_conference_abv` (str, optional):
        Optional argument.
        If you only want CFB drive data from games 
        where the offensive team is from a specific confrenece,
        set `conference_abv` to the abbreviation 
        of the conference you want CFB drive data from.
        For a list of confrences, 
        use the `cfbd_json_py.conferences.get_cfbd_conference_info()`
        function.

    `defensive_conference_abv` (str, optional):
        Optional argument.
        If you only want CFB drive data from games 
        where the defensive team is from a specific confrenece,
        set `conference_abv` to the abbreviation 
        of the conference you want CFB drive data from.
        For a list of confrences, 
        use the `cfbd_json_py.conferences.get_cfbd_conference_info()`
        function.

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

    from cfbd_json_py.drives import get_cfbd_drives_info

    cfbd_key = "tigersAreAwsome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwsome":
        print("Using the user's API key declared in this script for this example.")

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
        print("Get CFB Drive data from games involving the 2020 Cincinnati Bearcats Football Team.")
        json_data = get_cfbd_drives_info(
            api_key=cfbd_key,
            season=2020,
            team="Cincinnati"
        )
        print(json_data)
        time.sleep(5)

        # Get CFB Drive data from games involving the 2020 Ohio Bobcats
        # Football Team, when Ohio was on offense.
        print("Get CFB Drive data from games involving the 2020 Ohio Bobcats Football Team, when Ohio was on offense.")
        json_data = get_cfbd_drives_info(
            api_key=cfbd_key,
            season=2020,
            offensive_team="Ohio"
        )
        print(json_data)
        time.sleep(5)

        # Get CFB Drive data from games involving the 2020 Ohio State Buckeyes
        # Football Team, when Ohio was on offense.
        print("Get CFB Drive data from games involving the 2020 Ohio State Buckeyes Football Team, when Ohio State was on defense.")
        json_data = get_cfbd_drives_info(
            api_key=cfbd_key,
            season=2020,
            defensive_team="Ohio State"
        )
        print(json_data)
        time.sleep(5)

        # Get CFB Drive data from Big 12 games in the 2020 CFB season.
        print("Get CFB Drive data from games involving the 2020 Ohio State Buckeyes Football Team, when Ohio State was on defense.")
        json_data = get_cfbd_drives_info(
            api_key=cfbd_key,
            season=2020,
            conference_abv="B12"
        )
        print(json_data)
        time.sleep(5)

        # Get CFB Drive data from Big 10 (B1G) games in the 2020 CFB season,
        # where the Big 10 team was on offense.
        print("Get CFB Drive data from games involving the 2020 Ohio State Buckeyes Football Team, when Ohio State was on defense.")
        json_data = get_cfbd_drives_info(
            api_key=cfbd_key,
            season=2020,
            offensive_conference_abv="B1G"
        )
        print(json_data)
        time.sleep(5)

        # Get CFB Drive data from  Mid-American Conference (MAC) games
        # in the 2020 CFB season, where the MAC team was on offense.
        print("Get CFB Drive data from games involving the 2020 Ohio State Buckeyes Football Team, when Ohio State was on defense.")
        json_data = get_cfbd_drives_info(
            api_key=cfbd_key,
            season=2020,
            defensive_conference_abv="MAC"
        )
        print(json_data)
        time.sleep(5)

        # Get CFB Drive data from Football Championship Subdivision (FCS) games
        # in week 3 ofthe 2020 CFB season,
        # where the MAC team was on offense.
        print("Get CFB Drive data from games involving the 2020 Ohio State Buckeyes Football Team, when Ohio State was on defense.")
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
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
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
        # you could just call these functions directly, without setting the API key
        # in the script.
        print("Using the user's API key suposedly loaded into this python environment for this example.")

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
        print("Get CFB Drive data from games involving the 2020 Cincinnati Bearcats Football Team.")
        json_data = get_cfbd_drives_info(
            season=2020,
            team="Cincinnati"
        )
        print(json_data)
        time.sleep(5)

        # Get CFB Drive data from games involving the 2020 Ohio Bobcats
        # Football Team, when Ohio was on offense.
        print("Get CFB Drive data from games involving the 2020 Ohio Bobcats Football Team, when Ohio was on offense.")
        json_data = get_cfbd_drives_info(
            season=2020,
            offensive_team="Ohio"
        )
        print(json_data)
        time.sleep(5)

        # Get CFB Drive data from games involving the 2020 Ohio State Buckeyes
        # Football Team, when Ohio was on offense.
        print("Get CFB Drive data from games involving the 2020 Ohio State Buckeyes Football Team, when Ohio State was on defense.")
        json_data = get_cfbd_drives_info(
            season=2020,
            defensive_team="Ohio State"
        )
        print(json_data)
        time.sleep(5)

        # Get CFB Drive data from Big 12 games in the 2020 CFB season.
        print("Get CFB Drive data from games involving the 2020 Ohio State Buckeyes Football Team, when Ohio State was on defense.")
        json_data = get_cfbd_drives_info(
            season=2020,
            conference_abv="B12"
        )
        print(json_data)
        time.sleep(5)

        # Get CFB Drive data from Big 10 (B1G) games in the 2020 CFB season,
        # where the Big 10 team was on offense.
        print("Get CFB Drive data from games involving the 2020 Ohio State Buckeyes Football Team, when Ohio State was on defense.")
        json_data = get_cfbd_drives_info(
            season=2020,
            offensive_conference_abv="B1G"
        )
        print(json_data)
        time.sleep(5)

        # Get CFB Drive data from  Mid-American Conference (MAC) games
        # in the 2020 CFB season, where the MAC team was on offense.
        print("Get CFB Drive data from games involving the 2020 Ohio State Buckeyes Football Team, when Ohio State was on defense.")
        json_data = get_cfbd_drives_info(
            season=2020,
            defensive_conference_abv="MAC"
        )
        print(json_data)
        time.sleep(5)

        # Get CFB Drive data from Football Championship Subdivision (FCS) games
        # in week 3 ofthe 2020 CFB season,
        # where the MAC team was on offense.
        print("Get CFB Drive data from games involving the 2020 Ohio State Buckeyes Football Team, when Ohio State was on defense.")
        json_data = get_cfbd_drives_info(
            season=2020,
            week=3,
            ncaa_division="fcs"
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
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
    row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/drives"

    # Input validation
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
            f"\n\nYou entered:\n{ncaa_division}"
        )

    # URL builder
    ########################################################################################################################################################################################################

    # Required by API
    url += f"?seasonType={season_type}"

    url += f"&year={season}"

    if week != None:
        url += f"&week={week}"

    if team != None:
        url += f"&team={team}"

    if offensive_team != None:
        url += f"&offense={offensive_team}"

    if defensive_team != None:
        url += f"&defense={defensive_team}"

    if conference_abv != None:
        url += f"&conference={conference_abv}"

    if offensive_conference_abv != None:
        url += f"&offenseConference={offensive_conference_abv}"

    if defensive_conference_abv != None:
        url += f"&defenseConference={defensive_conference_abv}"

    if ncaa_division != None:
        url += f"&classification={ncaa_division.lower}"

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

    for drive in tqdm(json_data):
        offense = drive['offense']
        row_df = pd.DataFrame(
            {
                "offense": offense
            }, index=[0]
        )
        del offense

        row_df['offense_conference'] = drive['offense_conference']
        row_df['defense'] = drive['defense']
        row_df['defense_conference'] = drive['defense_conference']
        row_df['game_id'] = drive['game_id']
        row_df['drive_id'] = drive['id']
        row_df['drive_number'] = drive['drive_number']
        row_df['is_scoring_drive'] = drive['scoring']
        row_df['drive_start_period'] = drive['start_period']
        row_df['drive_start_yardline'] = drive['start_yardline']
        row_df['drive_start_yards_to_goal'] = drive['start_yards_to_goal']
        row_df['drive_start_time_minutes'] = drive['start_time']['minutes']
        row_df['drive_start_time_seconds'] = drive['start_time']['seconds']
        row_df['drive_end_period'] = drive['end_period']
        row_df['drive_end_yardline'] = drive['end_yardline']
        row_df['drive_end_yards_to_goal'] = drive['end_yards_to_goal']
        row_df['drive_end_time_minutes'] = drive['end_time']['minutes']
        row_df['drive_end_time_seconds'] = drive['end_time']['seconds']
        row_df['drive_elapsed_minutes'] = drive['elapsed']['minutes']
        row_df['drive_elapsed_seconds'] = drive['elapsed']['seconds']
        row_df['drive_plays'] = drive['plays']
        row_df['drive_yards'] = drive['yards']
        row_df['drive_result'] = drive['drive_result']
        row_df['is_home_offense'] = drive['is_home_offense']
        row_df['start_offense_score'] = drive['start_offense_score']
        row_df['start_defense_score'] = drive['start_defense_score']
        row_df['end_offense_score'] = drive['end_offense_score']
        row_df['end_defense_score'] = drive['end_defense_score']

        cfb_drives_df = pd.concat([cfb_drives_df, row_df], ignore_index=True)

        del row_df

    if len(cfb_drives_df) == 0:
        logging.error(
            "The CFBD API accepted your inputs, " +
            "but found no data within your specified input paramaters." +
            " Please double check your input paramaters."
        )

    return cfb_drives_df
