# CHANGELOG: cfbd_json_py

## 0.0.8: The "Games" Update

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
