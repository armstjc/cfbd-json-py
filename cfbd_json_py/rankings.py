# Creation Date: 08/30/2023 01:13 EDT
# Last Updated Date: 11/08/2023 10:00 PM EST
# Author: Joseph Armstrong (armstrongjoseph08@gmail.com)
# File Name: rankings.py
# Purpose: Houses functions pertaining to CFB poll data within the CFBD API.
####################################################################################################

from datetime import datetime

import pandas as pd
import requests
from tqdm import tqdm
from cfbd_json_py.utls import get_cfbd_api_token


def get_cfbd_poll_rankings(
        season: int,
        api_key: str = None,
        api_key_dir: str = None,
        week: int = None,
        season_type: str = "regular",  # "regular" or "postseason"

        return_as_dict: bool = False):
    """
    Allows you to get CFB poll rankings data from the CFBD API.
    
    Parameters
    ----------
    `season` (int, mandatory):
        Required argument.
        Specifies the season you want CFB poll rankings data from.
        This must be specified, otherwise this package, and by extension
        the CFBD API, will not accept the request to get CFB poll rankings data.

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
        to load CFB poll rankings data from games in that season, and in that week.
        
    `season_type` (str, semi-optional):
        Semi-optional argument.
        By defualt, this will be set to "regular", for the CFB regular season.
        If you want CFB poll rankings data for non-regular season games, 
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

    from cfbd_json_py.rankings import get_cfbd_poll_rankings


    cfbd_key = "tigersAreAwsome"  # placeholder for your CFBD API Key.

    if cfbd_key != "tigersAreAwsome":
        print("Using the user's API key declared in this script for this example.")

        # Get CFB poll data for the 2020 CFB season.
        print("Get CFB poll data for the 2020 CFB season.")
        json_data = get_cfbd_poll_rankings(
            api_key=cfbd_key,
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get CFB poll data from week 10 of the 2023 CFB season.
        print("Get CFB poll data from week 10 of the 2023 CFB season.")
        json_data = get_cfbd_poll_rankings(
            api_key=cfbd_key,
            season=2023,
            week=10
        )
        print(json_data)
        time.sleep(5)

        # Get CFB poll data for the 2021 CFB season, during the postseason.
        print("Get CFB poll data for the 2021 CFB season, during the postseason.")
        json_data = get_cfbd_poll_rankings(
            api_key=cfbd_key,
            season=2021,
            season_type="postseason"
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_poll_rankings(
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

        # Get CFB poll data for the 2020 CFB season.
        print("Get CFB poll data for the 2020 CFB season.")
        json_data = get_cfbd_poll_rankings(
            season=2020
        )
        print(json_data)
        time.sleep(5)

        # Get CFB poll data from week 10 of the 2023 CFB season.
        print("Get CFB poll data from week 10 of the 2023 CFB season.")
        json_data = get_cfbd_poll_rankings(
            season=2023,
            week=10
        )
        print(json_data)
        time.sleep(5)

        # Get CFB poll data for the 2021 CFB season, during the postseason.
        print("Get CFB poll data for the 2021 CFB season, during the postseason.")
        json_data = get_cfbd_poll_rankings(
            season=2021,
            season_type="postseason"
        )
        print(json_data)
        time.sleep(5)

        # You can also tell this function to just return the API call as
        # a Dictionary (read: JSON) object.
        print("You can also tell this function to just return the API call as a Dictionary (read: JSON) object.")
        json_data = get_cfbd_poll_rankings(
            season=2020,
            week=10,
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
    rankings_df = pd.DataFrame()
    row_df = pd.DataFrame()
    url = "https://api.collegefootballdata.com/rankings"

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
    # URL builder
    ########################################################################################################################################################################################################

    # Required by API
    url += f"?year={season}"

    if week != None:
        url += f"&week={week}"

    if season_type != None:
        url += f"&seasonType={season_type}"

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
    
    for week in tqdm(json_data):
        w_season = week['season']
        w_season_type = week['seasonType']
        w_week = week['week']

        for poll in week['polls']:
            p_poll_name = poll['poll']
            
            for team in poll['ranks']:
                row_df = pd.DataFrame(
                    {
                        "season":w_season,
                        "season_type":w_season_type,
                        "week":w_week,
                        "poll_name":p_poll_name
                    },
                    index=[0]
                )

                row_df['poll_rank'] = team['rank']
                row_df['school_name'] = team['school']
                row_df['conference_name'] = team['conference']
                row_df['first_place_votes'] = team['firstPlaceVotes']
                row_df['points'] = team['points']

                rankings_df = pd.concat([rankings_df,row_df],ignore_index=True)
                del row_df
                
            del p_poll_name

        del w_season, w_season_type, w_week

    return rankings_df