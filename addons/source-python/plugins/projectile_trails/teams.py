# ../projectile_trails/teams.py

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
from entities import EntityGenerator


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Store an empty dictionary to store teams by number and name
GameTeams = {}

# Loop through each entity on the server
for edict in EntityGenerator():

    # Use try/except to get the entity's team name property, if it exists
    try:

        # Get the entity's teamname property
        teamname = edict.get_prop_string('m_szTeamname')

    # Was an exception raised?
    except (TypeError, ValueError):

        # If not, no need to add this as a team
        continue

    # Get the team number
    teamnumber = edict.get_prop_int('m_iTeamNum')

    # Store the team number and name
    GameTeams[teamnumber] = teamname
