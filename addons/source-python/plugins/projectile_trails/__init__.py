# ../projectile_trails/__init__.py

"""Verifies the game is supported."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Core
from core import GAME_NAME
#   Translations
from translations.strings import LangStrings
#   Weapons
from weapons.manager import weapon_manager

# Script Imports
from projectile_trails.info import info
from projectile_trails.teams import game_teams


# =============================================================================
# >> GAME VERIFICATION
# =============================================================================
# Are any projectiles listed for the game?
if not weapon_manager.projectiles:

    # If not, raise an error
    raise NotImplementedError(LangStrings('{0}/strings'.format(
        info.basename))['NotImplemented'].get_string().format(GAME_NAME))

# Are there any valid teams for the game?
if not game_teams:

    raise NotImplementedError(LangStrings('{0}/strings'.format(
        info.basename))['NotImplemented'].get_string().format(GAME_NAME))
