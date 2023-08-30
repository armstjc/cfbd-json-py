
from cfbd_json_py.utls import get_cfbd_api_token


def get_cfbd_betting_lines(
        year: int,
        api_key: str = None,
        api_key_dir: str = None,
        game_id: int = None,
        week: int = None,
        season_type: str = "regular",
        team: str = None,
        home_team: str = None,
        away_team: str = None,
        conference_abv: str = None,
        cache_data: bool = False,
        cache_dir: str = None,
        return_as_dict: bool = False):
    """
    Retrives betting information from the CFBD API for a given season, 
    or you could only get betting information for a single game.

    Parameters
    ----------

    `year` (int, mandatory):
        The season you want to retrive betting information from.

    `api_key` (str, optional):
        Optional argument. 
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
        If `season_type` is set to anything byt "regular" or "postseason", 
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

    `cache_data` (bool, semi-optional):
        Semi-optional argument.
        By default, `cache_data` will be set to `False`.
        If `cache_data` is set to `True`, 
        this function will cache any data downloaded from the CFBD API.
        If there is a previously cached request, 
        this function will attempt to load the previously cached data, 
        instead of making an API request in most cases.

    `cache_dir` (str, optional):
        Optional argument.
        If `cache_data` is set to `True`, and `cache_dir` is not null, 
        this function will try to cache any data downloaded to this custom directory,
        instead of caching the data in the user's home directory.

    `return_as_dict` (bool, semi-optional):
        Semi-optional argument.
        If you want this function to return the data as a dictionary, 
        instead of a pandas `DataFrame` object,
        set `return_as_dict` to `True`.

    Returns
    ----------
    A pandas `DataFrame` object with college football betting data, 
    or (if `return_as_dict` is set to `True`) 
    a dictionary object with college football betting data. 
    """

    if api_key != None:
        real_api_key = api_key
        del api_key
    else:
        real_api_key = get_cfbd_api_token(api_key_dir=api_key_dir)

    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )
