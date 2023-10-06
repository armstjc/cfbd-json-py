def get_cfbd_team_season_stats(
        api_key: str = None,
        api_key_dir: str = None,
        year: int = None,
        team: str = None,
        # `year` and/or `team` need to be not null for this function to work.
        conference_abv: str = None,
        start_week: int = None,
        end_week: int = None,

        return_as_dict: bool = False):
    """

    """
    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )


def get_cfbd_advanced_team_season_stats(
        api_key: str = None,
        api_key_dir: str = None,
        year: int = None,
        team: str = None,
        # `year` and/or `team` need to be not null for this function to work.
        exclude_garbage_time: bool = False,
        start_week: int = None,
        end_week: int = None,

        return_as_dict: bool = False):
    """

    """
    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )


def get_cfbd_advanced_team_game_stats(
        api_key: str = None,
        api_key_dir: str = None,
        year: int = None,
        team: str = None,
        # `year` and/or `team` need to be not null for this function to work.
        week: int = None,
        opponent: str = None,
        exclude_garbage_time: bool = False,
        season_type: str = "regular",  # "regular", "postseason", or "both"

        return_as_dict: bool = False):
    """

    """
    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )


def get_cfbd_team_stat_categories(
        api_key: str = None,
        api_key_dir: str = None,

        return_as_dict: bool = False):
    """

    """
    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )
