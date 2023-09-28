
def get_cfbd_games(
        year: int,
        api_key: str = None,
        api_key_dir: str = None,
        season_type: str = "regular",
        team: str = None,
        home_team: str = None,
        away_team: str = None,
        conference: str = None,
        ncaa_division: str = "fbs",
        game_id: int = None,

        return_as_dict: bool = False):
    """

    """

    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )


def get_cfbd_team_records(
        api_key: str = None,
        api_key_dir: str = None,
        year: int = None,
        team: str = None,  # Must specify either a year or team
        conference: str = None,

        return_as_dict: bool = False):
    """

    """

    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )


def get_cfbd_season_weeks(
        year: int,
        api_key: str = None,
        api_key_dir: str = None,

        return_as_dict: bool = False):
    """

    """

    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )


def get_cfbd_game_media_info(
        year: int,
        api_key: str = None,
        api_key_dir: str = None,
        season_type: str = "regular",  # "regular", "postseason", or "both"
        week: int = None,
        team: str = None,
        conference: str = None,
        media_type: str = "all",  # "tv", "radio", "web", "ppv", or "mobile"
        ncaa_division: str = "fbs",

        return_as_dict: bool = False):
    """

    """

    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )


def get_cfbd_player_game_stats(
        year: int,
        api_key: str = None,
        api_key_dir: str = None,
        season_type: str = "regular",  # "regular" or "postseason"
        week: int = None,
        team: str = None,
        conference: str = None,
        # `week`, `team`, and/or conference must be not null for this function to work.
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
        year: int = None,
        week: int = None,
        season_type: str = "regular",  # "regular", "postseason", or "both"
        conference: str = None):
    """

    """

    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )
