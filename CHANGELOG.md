# CHANGELOG: cfbd_json_py


## 0.2.4 The "Speedy" Update.
- Refactored `cfbd_json_py.games.get_cfbd_player_game_stats()`, `cfbd_json_py.plays.get_cfbd_pbp_play_types()`, and `cfbd_json_py.players.get_cfbd_player_season_stats()` to use a significantly faster process to parse player stats.
- Changed `print()` statements into `logging.info()` statements for `cfbd_json_py.games.get_cfbd_player_advanced_game_stats()`
- For `cfbd_json_py.metrics.get_cfbd_predicted_ppa_from_down_distance()`, a `logging.warn()` call is now a `logging.warning()` call due to a pending deprecation of `logging.warn()`.
- Fixed an issue found in `cfbd_json_py.players.get_cfbd_pbp_stats()` where the function would warn the user about an issue that the user should not have triggered.
- Removed `tqdm` integration with `cfbd_json_py.plays.get_cfbd_pbp_play_types()`, `cfbd_json_py.rankings.get_cfbd_poll rankings()`.
- Updated the package version to `0.2.4`.

## 0.2.3 The "Hotfix" Update.
- Fixed an issue raised in #51 where the `[player_id]` column would be entirely blank in `cfbd_json_py.players.get_cfbd_player_season_stats()`.
- Updated the package version to `0.2.3`.

## 0.2.2 The "Version Bump" Update
- Updated the package version to `0.2.2`.

## 0.2.1 The "College Football is BACK! (2024)" Update
- Fixed a bug in `cfbd_json_py.drives.get_cfbd_drives_info()` where the `ncaa_division` parameter would become malformed, the API call wouldn't filter by `ncaa_division`, but the API call would still be accepted.
- Updated the package to comply with changes made in version `4.6.0` of the CFBD V1 API. These changes in this API version removed the `game_id` parameter from `cfbd_json_py.betting.get_cfbd_betting_lines()` and from `cfbd_json_py.games.get_cfbd_weather_info()`.
- Updated the package version to `0.2.1`.

## 0.2.0 The "Patreon" Update
- Re-implemented the process of storing a user's API key. If you have used `cfbd_json_py.utls.set_cfbd_api_token()` in the past, you do not need to do anything to migrate your API key to this new process.
- The following functions require a user to subscribe to the [CFBD Patreon](https://www.patreon.com/collegefootballdata):
  - Implemented `cfbd_json_py.games.get_cfbd_live_scoreboard()`, a function that allows a user to get live scoreboard data directly from the CFBD API, if they subscribe to the CFBD patreon.
  - Implemented `cfbd_json_py.games.get_cfbd_weather_info()`, a function that allows a user to get weather data directly from the CFBD API, if they subscribe to the CFBD patreon.
  - Partially implemented `cfbd_json_py.plays.get_cfbd_live_pbp_data()`, a function that allows someone to access live play-by-play (PBP) data, if they subscribe to the CFBD patreon.
- Implemented a new file header template for all python files.
- Applied some minor formatting changes to the python code.
- Updated the package version to `0.2.0`, because of the new season (2024).


## 0.1.2: The "Spell Check" update
- Fixed spelling errors previously present in earlier versions of this python package.
- Updated the package version to `0.1.2`.

## 0.1.1: The "housekeeping" update
- Cleaned up the formatting of all functions and python code.
- Updated the package version to `0.1.1`.

## 0.1.0: The "beta release" update
- Optimized a number of functions in this python package by using `pandas.json_normalize()` instead of looping through the data for some functions.
- Finalized the python package so it can be used by others.
- Updated the package version to `0.1.0`.

## 0.0.20: The "ratings" update

- Implemented `cfbd_json_py.ratings.get_cfbd_fpi_ratings()`, a function that allows a user to get Football Power Index (FPI) ratings data directly from the CFBD API.  
- Implemented `cfbd_json_py.ratings.get_cfbd_elo_ratings()`, a function that allows a user to get Elo ratings data directly from the CFBD API.  
- Implemented `cfbd_json_py.ratings.get_cfbd_sp_plus_conference_ratings()`, a function that allows a user to get Success rate and equivalent Points per play (S&P+) ratings data, grouped by conference, directly from the CFBD API.  
- Implemented `cfbd_json_py.ratings.get_cfbd_sp_plus_ratings()`, a function that allows a user to get Success rate and equivalent Points per play (S&P+) ratings data, directly from the CFBD API.  
- Implemented `cfbd_json_py.ratings.get_cfbd_sp_plus_ratings()`, a function that allows a user to get Simple Rating System (SRS) ratings data, directly from the CFBD API.  
- Updated the package version to `0.0.20`.

## 0.0.19: The "stats" Update

- Implemented `cfbd_json_py.stats.get_cfbd_team_stat_categories()`, a function that allows a user to get a list of team stat categories, directly from the CFBD API.
- Implemented `cfbd_json_py.stats.get_cfbd_advanced_team_game_stats()`, a function that allows a user to get advanced CFB team game stats, from the CFBD API.
- Implemented `cfbd_json_py.stats.get_cfbd_advanced_team_season_stats()`, a function that allows a user to get advanced CFB team season stats, from the CFBD API.
- Implemented `cfbd_json_py.stats.get_cfbd_team_season_stats()`, a function that allows a user to get CFB team season stats, from the CFBD API.
- Implemented `cfbd_json_py.metrics.get_cfbd_fg_expected_points()`, a function based off of the recently added `/metrics/fg/ep` endpoint to the CFBD API in version `4.5.2`,  which returns the expected points of a field goal for every yard line on a football field.
- Updated the package's GitHub repo to identify the current version of the CFBD API as `"4.5.2"` instead of `"4.5.1"`
- Updated the package version to `0.0.19`.


## 0.0.18: The "recruiting" Update
- Implemented `cfbd_json_py.recruiting.get_cfbd_team_recruiting_group_ratings()`, a function that allows a user to get CFB recruiting data, grouped by the team and position, from the CFBD API.
- Implemented `cfbd_json_py.recruiting.get_cfbd_team_recruiting_ratings()`, a function that allows a user to get team recruiting rankings, from the CFBD API.
- Implemented `cfbd_json_py.recruiting.get_cfbd_player_recruit_ratings()`, a function that allows a user to get a list of players recruited to CFB teams, from the CFBD API.
- Updated the package version to `0.0.18`.

## 0.0.17: The "Teams" Update
- Implemented `cfbd_json_py.teams.get_cfbd_team_matchup_history()`, a function that allows a user to get a list of matchups between two teams from the CFBD API.
- Implemented `cfbd_json_py.teams.get_cfbd_team_talent_rankings()`, a function that allows a user to get team talent ranking from the CFBD API.
- Implemented `cfbd_json_py.teams.get_cfbd_team_rosters()`, a function that allows a user to get team roster data from the CFBD API.
- Implemented `cfbd_json_py.teams.get_cfbd_fbs_team_list()`, a function that allows a user to get a list of FBS teams from the CFBD API.
- Updated the `documentation` section of `pyproject.toml` to point to the following URL: https://armstjc.github.io/cfbd-json-py/cfbd_json_py.html
- Updated the package version to `0.0.17`.

## 0.0.16: The "Maintenance" Update
- **NOTE**: This update is to push the previous `0.0.15` update to PyPi.
- Implemented `cfbd_json_py.teams.get_cfbd_team_information()`, a function that allows a user to get CFB team information from the CFBD API.
- Updated the package version to `0.0.16`.

## 0.0.15: The "Play-by-play" Update

- Implemented `cfbd_json_py.plays.get_cfbd_pbp_data()`, a function that allows a user to get CFB play-by-play (PBP) stats from the CFBD API.
- Implemented `cfbd_json_py.plays.get_cfbd_pbp_data()`, a function that allows a user to get CFB PBP data from the CFBD API.
- Implemented `cfbd_json_py.plays.get_cfbd_pbp_play_types()`, a function that allows a user to get a list of valid inputs for the `play_type` parameter for `cfbd_json_py.plays.get_cfbd_pbp_data()`.
- Implemented `cfbd_json_py.plays.get_cfbd_pbp_stat_types()`, a function that allows a user to get a list of valid inputs for the `stat_type_id` parameter for `cfbd_json_py.plays.get_cfbd_pbp_stats()`.
- Updated the package version to `0.0.15`.

## 0.0.14: The "Rankings" Update

- Implemented `cfbd_json_py.rankings.get_cfbd_poll_rankings()`, a function that allows a user to get CFB poll data from the CFBD API.
- Updated the package version to `0.0.14`.

## 0.0.13: The "Rankings" Update

- Implemented `cfbd_json_py.rankings.get_cfbd_poll_rankings()`, a function that allows a user to get CFB poll data from the CFBD API.
- Updated the package version to `0.0.13`.

## 0.0.12: The "Venues" Update

- Implemented `cfbd_json_py.venues.get_cfbd_venues()`, a function that allows a user to a list of CFB venues from the CFBD API.
- Updated the package version to `0.0.12`.

## 0.0.11: The "Players" Update

- Implemented `cfbd_json_py.players.get_cfbd_transfer_portal_data()`, a function that allows a user to get transfer portal data from the CFBD API.
- Implemented `cfbd_json_py.players.get_cfbd_player_season_stats()`, a function that allows a user to get player season stats from the CFBD API.
- Implemented `cfbd_json_py.players.get_cfbd_returning_production()`, a function that allows a user to get returning production data from the CFBD API.
- Implemented `cfbd_json_py.players.get_cfbd_player_usage()`, a function that allows a user to get player usage data from the CFBD API.
- Implemented `cfbd_json_py.players.get_cfbd_pregame_win_probability_data()`, a function that allows a user to lookup known players in the CFBD API.
- Updated the function descriptions for `cfbd_json_py.games.get_cfbd_player_game_stats()`, and added a `["season"]` column to the function's output, should `return_as_dict = False`.
- Updated the validation logic for the `season` input variable for the following functions, by allowing a user to lookup data for the next CFB season:
  - `cfbd_json_py.drives.get_cfbd_drives_info()`
  - `cfbd_json_py.games.get_cfbd_games()`
  - `cfbd_json_py.games.get_cfbd_season_weeks()`
  - `cfbd_json_py.games.get_cfbd_game_media_info()`
  - `cfbd_json_py.games.get_cfbd_player_game_stats()`
  - `cfbd_json_py.metrics.get_cfbd_team_season_ppa_data()`
  - `cfbd_json_py.metrics.get_cfbd_team_game_ppa_data()`
  - `cfbd_json_py.metrics.get_cfbd_player_game_ppa_data()`
  - `cfbd_json_py.metrics.get_cfbd_player_season_ppa_data()`
  - `cfbd_json_py.metrics.get_cfbd_pregame_win_probability_data()`
  - `cfbd_json_py.metrics.get_cfbd_pregame_win_probability_data()`
- Updated the package version to `0.0.11`.

## 0.0.10: The "Metrics" Update

- Implemented `cfbd_json_py.metrics.get_cfbd_pregame_win_probability_data()`, a function that allows a user to get pregame win probability data from the CFBD API.
- Implemented `cfbd_json_py.metrics.get_cfbd_game_win_probability_data()`, a function that allows a user to get win probability data from a valid game ID in the CFBD API.
- Implemented `cfbd_json_py.metrics.get_cfbd_player_season_ppa_data()`, a function that allows a user to get player game PPA data from the CFBD API.
- Implemented `cfbd_json_py.metrics.get_cfbd_player_game_ppa_data()`, a function that allows a user to get player season PPA data from the CFBD API.
- Implemented `cfbd_json_py.metrics.get_cfbd_team_game_ppa_data()`, a function that allows a user to get team game PPA data from the CFBD API.
- Implemented `cfbd_json_py.metrics.get_cfbd_team_season_ppa_data()`, a function that allows a user to get team season PPA data from the CFBD API.
- Implemented `cfbd_json_py.metrics.get_cfbd_predicted_ppa_from_down_distance()`, a function that allows a user to get predicted PPA values from the CFBD API, given a down and distance (like 1st and 10).
- Updated the function descriptions for the following functions:
  - `cfbd_json_py.utls.reverse_cipher_encrypt()`
  - `cfbd_json_py.utls.reverse_cipher_decrypt()`
  - `cfbd_json_py.utls.get_cfbd_api_token()`
- Updated the `README.md` file to give users a general idea on what this python package is, how to install it, and how to access this python package's docs.
- Added a front page to the Docs website for this python package.
- Updated the package version to `0.0.10`.

## 0.0.9: The "Bug Fixes 1" Update
- Attempted another fix for the `generate_docs.yml` GitHub Workflow to allow it to call `pdoc` properly within GitHub Actions.
- Removed the PyArrow package as a required package for this python package.
- Updated the package version to `0.0.9`.

## 0.0.8: The "Games" Update

- Implemented `cfbd_json_py.games.get_cfbd_player_advanced_game_stats()`, a function that allows a user to get advanced player game stats for actual CFB games in a specific time frame, from the CFBD API.
- Implemented `cfbd_json_py.games.get_cfbd_player_game_stats()`, a function that allows a user to get player game stats for actual CFB games in a specific time frame, from the CFBD API.
- Implemented `cfbd_json_py.games.get_cfbd_game_media_info()`, a function that allows a user to get a list of known broadcasters for actual CFB games in a specific time frame, from the CFBD API.
- Implemented `cfbd_json_py.games.get_cfbd_season_weeks()`, a function that allows a user to get a list of weeks that occurred in a given CFB season from the CFBD API.
- Implemented `cfbd_json_py.games.get_cfbd_team_records()`, a function that allows a user to get team records data from the CFBD API.
- Fixed multiple bugs that would prevent a user from properly calling `cfbd_json_py.games.get_cfbd_games()` in certain edge cases.
- Attempted a fix for the `generate_docs.yml` GitHub Workflow to allow it to call `pdoc` properly within GitHub Actions.
- Updated the package version to `0.0.8`.

## 0.0.7: The "Infrastructure" Update.

- Implemented `cfbd_json_py.games.get_cfbd_games()`, a function that allows a user to get game/schedule data from the CFBD API.
- Added a Docs webpage framework to this package by using [pdoc](https://pdoc.dev/)
- Added `cfbd_json_py._early_access`, a section specifically for CFBD API endpoints that exist, but aren't implemented yet by this python package.
- Added python file descriptors to track changes, detail when a file was first created, and explain the python file's purpose.
- Implemented the `check_cfbd_api_compatibility.py` python script, a script that checks if this python package is compatible with the most recent version of the CFBD API, and raises a `ValueError()` if that isn't the case.
- Updated the package version to `0.0.7`.

## 0.0.6: The "Drives" Update.

- Implemented `cfbd_json_py.drives.get_cfbd_drives_info()`, a function that allows a user to get CFB drive data from the CFBD API.
- Added a sample python file for `cfbd_json_py.draft.get_cfbd_nfl_draft_info()` in the "Usage" section for the function's description, as well as cleaning up the code formatting for this function.
- Fixed a minor spelling error in the function description for `cfbd_json_py.betting.get_cfbd_betting_lines()`
- Updated the package version to `0.0.6`.

## 0.0.5: The "Draft" Update.

- Implemented `cfbd_json_py.draft.get_cfbd_nfl_teams()`, a function that allows a user to get a list of NFL teams from the CFBD API.
- Implemented `cfbd_json_py.draft.get_cfbd_nfl_positions()`, a function that allows a user to get a list of player positions for the NFL Draft from the CFBD API.
- Implemented `cfbd_json_py.draft.get_cfbd_nfl_draft_info()`, a function that allows a user to get a list of actual NFL Draft selections from the CFBD API.
- Updated the function descriptions for the following functions:
  - `cfbd_json_py.betting.get_cfbd_betting_lines()`
  - `cfbd_json_py.coaches.get_cfbd_coaches_info()`
  - `cfbd_json_py.conferences.get_cfbd_conference_info()`
- Updated the package version to `0.0.5`.

## 0.0.4: The "Conferences" Update.

- Implemented `cfbd_json_py.conferences.get_cfbd_conference_info()`, a function that allows a user to get CFB conference info from the CFBD API.
- Updated the package version to `0.0.4`.

## 0.0.3: The "Coaches" Update.

- Implemented `cfbd_json_py.coaches.get_cfbd_coaches_info()`, a function that allows a user to get CFB head coach information from a specified season, time frame, team, or name.
- Updated the sample script found in the help guide for `cfbd_json_py.betting.get_cfbd_betting_lines()`.
- Fixed a bug in `cfbd_json_py.betting.get_cfbd_betting_lines()` that would always result in the function not recognizing if the imputed `api_key` is the placeholder key inside the sample script for this function.
- Updated the package version to `0.0.3`.

## 0.0.2: The "Betting" Update.

- Removed the option to cache data. This may be implemented in a future version.
- Implemented `cfbd_json_py.betting.get_cfbd_betting_lines()`, a function that allows a user to get betting lines for a season, a week, and/or for a specific team for the regular season, or postseason.
- Changed `cfbd_json_py.utls.get_cfbd_api_token()` to log, not print out the fact that the CFBD API key the function is trying to find is not present in the current Python environment.
- Updated the package version to `0.0.2`.

## 0.0.1: The "First Steps" Update

- Implemented the core structure of the python package.
- Updated the package version to `0.0.1`.
