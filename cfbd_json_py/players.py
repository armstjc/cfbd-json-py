# Creation Date: 08/30/2023 01:13 EDT
# Last Updated Date: 10/06/2023 07:53 PM EDT
# Author: Joseph Armstrong (armstrongjoseph08@gmail.com)
# File Name: players.py
# Purpose: Houses functions pertaining to CFB player data within the CFBD API.
####################################################################################################


def cfbd_player_search(
        search_str: str,
        api_key: str = None,
        api_key_dir: str = None,
        position: str = None,
        team: str = None,
        season: int = None,

        return_as_dict: bool = False):
    """

    """
    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )


def get_cfbd_player_usage(
        season: int,
        api_key: str = None,
        api_key_dir: str = None,
        team: str = None,
        conference_abv: str = None,
        position: str = None,
        player_id: int = None,
        exclude_garbage_time: bool = False,
        return_as_dict: bool = False):
    """

    """
    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )


def get_cfbd_returning_production(
        season: int,
        api_key: str = None,
        api_key_dir: str = None,
        team: str = None,
        conference_abv: str = None,

        return_as_dict: bool = False):
    """

    """
    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )


def get_cfbd_player_season_stats(
        season: int,
        api_key: str = None,
        api_key_dir: str = None,
        team: str = None,
        conference_abv: str = None,
        start_week: int = None,
        end_week: int = None,
        season_type: str = 'regular',  # "regular", "postseason", or "both"
        stat_category: str = None,

        return_as_dict: bool = False):
    """

    """
    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )


def get_cfbd_transfer_portal_data(
        season: int,
        api_key: str = None,
        api_key_dir: str = None,

        return_as_dict: bool = False):
    """

    """
    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )
