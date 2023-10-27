# Creation Date: 08/30/2023 01:13 EDT
# Last Updated Date: 10/20/2023 02:33 PM EDT
# Author: Joseph Armstrong (armstrongjoseph08@gmail.com)
# File Name: __init__.py
# Purpose: Allows for the python package to function,
#          by allowing you to to access functions within
#          this package.
####################################################################################################
"""
# Welcome!
This is the official docs page for the `cfbd_json_py` python package.

To the left of this page are various endpoints for this python package.
- `cfbd_json_py.betting`: 
    Holds functions for betting lines and betting data from the CFBD API.
- `cfbd_json_py.coaches`: 
    Holds functions for you to get coaching data (past and present).
- `cfbd_json_py.conferences`: 
    Holds functions for you to get information for CFB confrences.
- `cfbd_json_py.draft`: 
    Holds functions for you to get NFL draft information/data for 
    various players in the CFBD API
- `cfbd_json_py.drives`: 
    Holds functions for you to get data for offensive and/or defensive drives 
    within the CFBD API.
- `cfbd_json_py.games`: 
    Holds functions for you to get various datapoints pertaining to 
    actual CFB games within the CFBD API.
- `cfbd_json_py.metrics`: 
    Holds functions to allow you to calculate or retrive various advanced metrics 
    from the CFBD API.
- `cfbd_json_py.players`: 
    Holds functions for you to get various 
    data endpoints related to player stats, 
    player information, and player data.
- `cfbd_json_py.plays`: 
    Holds functions for play-by-play (PBP) data for CFB games, 
    as well as a way to calculate stats from PBP data.
- `cfbd_json_py.rankings`: 
    Holds functions for various CFB team ranking polls, 
    and their results.
- `cfbd_json_py.ratings`: 
    Holds functions to allow you to get various team ratings data 
    (like SP+, SRS, and Elo team ratings) from the CFBD API.
- `cfbd_json_py.recruiting`: 
    Holds functions for you to access CFB recruting data and information, 
    as well as team and player ratings for recruiting.
- `cfbd_json_py.stats`: 
    Holds functions for you to get various team stats from the CFBD API.
- `cfbd_json_py.teams`: 
    Holds functions for you to get team information and data, 
    as well as head-to-head records and matchup history.
- `cfbd_json_py.utls`: 
    Various utilities that can be used from this package.
    Outside of `cfbd_json_py.utls.set_cfbd_api_token()`, 
    you don't need to call any of these functions directly.
- `cfbd_json_py.venues`: 
    Holds functions for you to get information on 
    various venues/stadiums within the college football world.
    
# Basic Setup

If you have a CFBD API key, you have three ways to set it for this python package to use:
1. Declare the API key as a string variable in a python script (not reccomended, extreme security risk).
2. Declare the API key in your environment as `CFBD_API_KEY`.
    - `cfbd_json_py` will first look for your environment, 
    if you don't declare the API key as a string variable, 
    when calling any function in this python package that uses a CFBD API call.
    - If you're using GitHub Actions with this package, 
    just set a repository secret with the name `CFBD_API_KEY`. 
    Again, this package will automatically know where to look, 
    if you've set your API key in the environment 
3. Use `cfbd_json_py.utls.set_cfbd_api_token()` to store the API key in an encrypted file on your machine.
    - To set the API key for this package with this function, 
    run this code in a python script, 
    replacing `"TigersAreAwesome"` with your API key:

```
from cfbd_api_key.utls import set_cfbd_api_token

cfbd_api_key = "TigersAreAwesome" # replace this with your actual API key
set_cfbd_api_token(api_key=cfbd_api_key)
```

> **NOTE:** *In a future version, 
    there will be an executable application seperate from this package
    for Windows, Mac, and Linux users to effectively do the same thing 
    as the above code block, but with a graphical user interface (GUI).*

If you want to see how to use this python package after setting up your API key,
click on one of the submodules on the left 
to view the various functions within each submodule.
Each function has a tutorial script on the various ways you can call that function.

# Other Notes
- If you want to see all CFBD API endpoints that are currently supported, 
    [click here](https://api.collegefootballdata.com/api/docs/?url=/api-docs.json#/)
    to access the current Swagger docs for the entire API.
- If you want to see the source code for this package, 
    [click here](https://github.com/armstjc/cfbd-json-py) to see the current stable build of this python package on GitHub.
- If you want to see the active changelog for this python package, 
    [click here]() to view the changelog of this python package on GitHub.

"""

# Generated Functions:
from cfbd_json_py._early_access import *


# Fully Implemented Functions:
from cfbd_json_py.betting import *
from cfbd_json_py.coaches import *
from cfbd_json_py.conferences import *
from cfbd_json_py.draft import *
from cfbd_json_py.drives import *
from cfbd_json_py.games import *
from cfbd_json_py.metrics import *
from cfbd_json_py.players import *
from cfbd_json_py.plays import *
from cfbd_json_py.rankings import *
from cfbd_json_py.ratings import *
from cfbd_json_py.recruiting import *
from cfbd_json_py.stats import *
from cfbd_json_py.teams import *
from cfbd_json_py.venues import *

# Utils

from cfbd_json_py.utls import *

