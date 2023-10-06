
def get_cfbd_pbp_data(
        season: int,
        api_key: str = None,
        api_key_dir: str = None,
        week: int = None,
        # required if team, offense, or defense, not specified
        team: str = None,
        offensive_team: str = None,
        defensive_team: str = None,
        conference_abv: str = None,
        offensive_conference_abv: str = None,
        defensive_conference_abv: str = None,
        play_type: int = None,
        ncaa_division: str = "fbs",

        return_as_dict: bool = False):
    """

    """
    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )


def get_cfbd_pbp_play_types(
        api_key: str = None,
        api_key_dir: str = None,

        return_as_dict: bool = False):
    """

    """
    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )


def get_cfbd_pbp_stats(
        season: int,
        api_key: str = None,
        api_key_dir: str = None,
        week: int = None,
        team: str = None,
        game_id: int = None,
        athlete_id: int = None,
        stat_type_id: int = None,
        season_type: str = "regular",  # "regular", "postseason", or "both"
        conference_abv: str = None,

        return_as_dict: bool = False):
    """

    """
    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )


def get_cfbd_pbp_stat_types(
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


def get_cfbd_live_pbp_data(
        game_id: int,
        api_key: str = None,
        api_key_dir: str = None,

        return_as_dict: bool = False):
    """

    """
    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )
