
def get_cfbd_predicted_ppa_from_down_distance(
        down: int,
        distance: int,
        api_key: str = None,
        api_key_dir: str = None):
    """
    """

    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )


def get_cfbd_team_ppa_data(
        api_key: str = None,
        api_key_dir: str = None,
        year: int = None,
        team: str = None,
        # `year` and/or `team` must be not null for this function to work.
        conference_abv: str = None,
        exclude_garbage_time: bool = False,

        return_as_dict: bool = False):
    """

    """

    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )


def get_cfbd_game_ppa_data(
        season: int,
        api_key: str = None,
        api_key_dir: str = None,
        week: int = None,
        team: str = None,
        conference_abv: str = None,
        exclude_garbage_time: bool = False,
        season_type: str = "regular",  # "regular" or "postseason"

        return_as_dict: bool = False):
    """

    """

    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )


def get_cfbd_game_player_ppa_data(
        season: int,
        api_key: str = None,
        api_key_dir: str = None,
        week: int = None,
        team: str = None,
        # A week or team must be specified
        position: str = None,
        player_id: int = None,
        play_threshold: int = None,
        exclude_garbage_time: bool = False,
        season_type: str = "regular",  # "regular" or "postseason"

        return_as_dict: bool = False):
    """

    """

    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )


def get_cfbd_season_player_ppa_data(
        season: int,
        api_key: str = None,
        api_key_dir: str = None,
        team: str = None,
        conference_abv: str = None,
        position: str = None,
        player_id: int = None,
        play_threshold: int = None,
        exclude_garbage_time: bool = False,

        return_as_dict: bool = False):
    """

    """
    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )


def get_cfbd_game_win_probability_data(
        game_id: int,
        api_key: str = None,
        api_key_dir: str = None,

        return_as_dict: bool = False):
    """

    """
    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )


def get_cfbd_pregame_win_probability_data(
        season: int,
        api_key: str = None,
        api_key_dir: str = None,
        week: int = None,
        team: str = None,
        season_type: str = "regular",  # "regular" or "postseason"

        return_as_dict: bool = False):
    """

    """
    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )
