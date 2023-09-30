# CHANGELOG: cfbd_json_py

## 0.0.4: The "Conferences" Update.

- Implemented `get_cfbd_coaches_info()`, a function that allows a user to get CFB confrence info from the CFBD API.
- Updated the package version to `0.0.4`.

## 0.0.3: The "Coaches" Update.

- Implemented `get_cfbd_coaches_info()`, a function that allows a user to get CFB head coach information from a specified season, timeframe, team, or name.
- Updated the sample script found in the help guide for `get_cfbd_betting_lines()`.
- Fixed a bug in `get_cfbd_betting_lines()` that would always result in the function not recognizing if the inputed `api_key` is the placeholder key inside the sample script for this function.
- Updated the package version to `0.0.3`.

## 0.0.2: The "Betting" Update.

- Removed the option to cache data. This may be implemented in a future version.
- Implemented `cfbd_json_py.betting.get_cfbd_betting_lines()`, a function that allows a user to get betting lines for a season, a week, and/or for a specific team for the regular season, or postseason.
- Changed `cfbd_json_py.utls.get_cfbd_api_token()`` to log, not print out the fact that the CFBD API key the function is trying to find is not present in the current Python environment.
- Updated the package version to `0.0.2`.

## 0.0.1: The "First Steps" Update

- Implemented the core structure of the python package.
- Updated the package version to `0.0.1`.
