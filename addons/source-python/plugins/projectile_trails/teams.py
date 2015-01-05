# ../projectile_trails/teams.py

"""Provides teams by number/name for the current game."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Site-Package Imports
#   ConfigObj
from configobj import ConfigObj

# Source.Python Imports
#   Core
from core import GAME_NAME
#   Filters
from filters.entities import EntityIter
#   Paths
from paths import PLUGIN_DATA_PATH

# Script Imports
from projectile_trails.info import info


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Get any odd team names stored in ../data/plugins/projectile_trails/
_odd_teams = ConfigObj(PLUGIN_DATA_PATH.joinpath(
    info.basename + '.ini')).get(GAME_NAME, {})

# Store an empty dictionary to store teams by number and name
game_teams = {}

# Loop through each entity on the server
for entity in EntityIter(return_types='entity'):

    # Use try/except to get the entity's team name property, if it exists
    try:

        # Get the team's name
        _teamname = entity.teamname

    # Was an exception raised?
    except AttributeError:

        # If not, no need to add this as a team
        continue

    # Get the team's number
    _teamnum = entity.team

    # Is the team possibly invalid?
    if _teamname in ('Unassigned', 'Spectator'):

        # Is the team not in the odd teams dictionary?
        if _teamnum not in _odd_teams:
            continue

        # Set the odd team name
        _teamname = _odd_teams[_teamnum]

    # Store the team number and name
    game_teams[_teamnum] = _teamname
