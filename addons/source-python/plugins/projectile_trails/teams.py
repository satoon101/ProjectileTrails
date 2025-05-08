# ../projectile_trails/teams.py

"""Provides teams by number/name for the current game."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Site-Package
from configobj import ConfigObj

# Source.Python
from core import GAME_NAME
from filters.entities import EntityIter
from paths import PLUGIN_DATA_PATH
from players.teams import team_managers, teams_by_number

# Plugin
from .info import info

# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    "GAME_TEAMS",
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Get any odd team names stored in ../data/plugins/projectile_trails/
_odd_teams = ConfigObj(
    PLUGIN_DATA_PATH / info.name + ".ini",
).get(GAME_NAME, {})

GAME_TEAMS = {}
for manager in team_managers:
    for entity in EntityIter(manager):
        if teams_by_number[entity.team] in ("un", "spec"):
            continue

        GAME_TEAMS[entity.team] = entity.team_name

GAME_TEAMS.update(_odd_teams)
