# Creation Date: 08/30/2023 01:13 EDT
# Last Updated Date: 10/06/2023 07:53 PM EDT
# Author: Joseph Armstrong (armstrongjoseph08@gmail.com)
# File Name: ratings.py
# Purpose: Houses functions pertaining to CFB team rating data within the CFBD API.
####################################################################################################

def get_cfbd_sp_plus_ratings(
        api_key: str = None,
        api_key_dir: str = None,
        season: int = None,
        team: int = None,
        # Either `year` or `team` have to be not null for this function to work.

        return_as_dict: bool = False):
    """

    """
    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )


def get_cfbd_srs_ratings(
        api_key: str = None,
        api_key_dir: str = None,
        season: int = None,
        team: int = None,
        # Either `year` or `team` have to be not null for this function to work.
        conferenece: str = None,

        return_as_dict: bool = False):
    """

    """
    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )


def get_cfbd_sp_plus_conference_ratings(
        season: int,
        api_key: str = None,
        api_key_dir: str = None,
        conference_abv: str = None,

        return_as_dict: bool = False):
    """

    """
    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )


def get_cfbd_elo_ratings(
        season: int,
        api_key: str = None,
        api_key_dir: str = None,
        week: int = None,
        season_type: str = 'regular',  # "regular" or "postseason"
        team: str = None,
        conference_abv: str = None,

        return_as_dict: bool = False):
    """

    """
    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )
