# CHANGELOG: cfbd_json_py

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
- Updated the validation logic for the `season` input variable for the following functions, by alowing a user to lookup data for the next CFB season:
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

- Implemented `cfbd_json_py.games.get_cfbd_player_advanced_game_stats()`, a function that allows a user to get advanced player game stats for actual CFB games in a specific timeframe, from the CFBD API.
- Implemented `cfbd_json_py.games.get_cfbd_player_game_stats()`, a function that allows a user to get player game stats for actual CFB games in a specific timeframe, from the CFBD API.
- Implemented `cfbd_json_py.games.get_cfbd_game_media_info()`, a function that allows a user to get a list of known broadcasters for actual CFB games in a specific timeframe, from the CFBD API.
- Implemented `cfbd_json_py.games.get_cfbd_season_weeks()`, a function that allows a user to get a list of weeks that occured in a given CFB season from the CFBD API.
- Implemented `cfbd_json_py.games.get_cfbd_team_records()`, a function that allows a user to get team records data from the CFBD API.
- Fixed multiple bugs that would prevent a user from properly calling `cfbd_json_py.games.get_cfbd_games()` in certian edge cases.
- Attempted a fix for the `generate_docs.yml` GitHub Workflow to allow it to call `pdoc` properly within GitHub Actions.
- Updated the package version to `0.0.8`.

## 0.0.7: The "Infrastructure" Update.

- Implemented `cfbd_json_py.games.get_cfbd_games()`, a function that allows a user to get game/schedule data from the CFBD API.
- Added a Docs webpage framework to this package by using [pdoc](https://pdoc.dev/)
- Added `cfbd_json_py._early_access`, a section specifically for CFBD API endpoints that exist, but aren't implemented yet by this python package.
- Added python file descriptors to track changes, detail when a file was first created, and explian the python file's purpose.
- Implemented the `check_cfbd_api_compatability.py` python script, a script that checks if this python package is compatible with the most recent version of the CFBD API, and raises a `ValueError()` if that isn't the case.
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

- Implemented `cfbd_json_py.conferences.get_cfbd_conference_info()`, a function that allows a user to get CFB confrence info from the CFBD API.
- Updated the package version to `0.0.4`.

## 0.0.3: The "Coaches" Update.

- Implemented `cfbd_json_py.coaches.get_cfbd_coaches_info()`, a function that allows a user to get CFB head coach information from a specified season, timeframe, team, or name.
- Updated the sample script found in the help guide for `cfbd_json_py.betting.get_cfbd_betting_lines()`.
- Fixed a bug in `cfbd_json_py.betting.get_cfbd_betting_lines()` that would always result in the function not recognizing if the inputed `api_key` is the placeholder key inside the sample script for this function.
- Updated the package version to `0.0.3`.

## 0.0.2: The "Betting" Update.

- Removed the option to cache data. This may be implemented in a future version.
- Implemented `cfbd_json_py.betting.get_cfbd_betting_lines()`, a function that allows a user to get betting lines for a season, a week, and/or for a specific team for the regular season, or postseason.
- Changed `cfbd_json_py.utls.get_cfbd_api_token()`` to log, not print out the fact that the CFBD API key the function is trying to find is not present in the current Python environment.
- Updated the package version to `0.0.2`.

## 0.0.1: The "First Steps" Update

- Implemented the core structure of the python package.
- Updated the package version to `0.0.1`.
