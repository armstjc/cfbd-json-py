# Creation Date: 08/30/2023 01:13 EDT
# Last Updated Date: 10/06/2023 07:54 PM EDT
# Author: Joseph Armstrong (armstrongjoseph08@gmail.com)
# File Name: recruiting.py
# Purpose: Houses functions pertaining to CFB recruiting data within the CFBD API.
####################################################################################################

def get_cfbd_player_recruit_ratings(
        api_key: str = None,
        api_key_dir: str = None,
        season: int = None,
        team: str = None,
        # `year` and/or `team` need to be not null for this function to work.
        recruit_classification: str = "HighSchool",
        # Can be "HighSchool", "JUCO", or "PrepSchool"
        position: str = None,
        state: str = None,

        return_as_dict: bool = False):
    """

    """
    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )


def get_cfbd_team_recruiting_ratings(
        api_key: str = None,
        api_key_dir: str = None,
        season: int = None,
        team: str = None,

        return_as_dict: bool = False):
    """

    """
    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )


def get_cfbd_team_recruiting_group_ratings(
        api_key: str = None,
        api_key_dir: str = None,
        start_season: int = None,
        end_season: int = None,
        team: str = None,
        conference_abv: str = None,

        return_as_dict: bool = False):
    """

    """
    raise NotImplementedError(
        'This function has yet to be implemented by this version.'
    )
