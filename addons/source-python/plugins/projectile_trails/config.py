# ../projectile_trails/config.py

"""Provides configuration based functionality for the plugin."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   ConfigObj
from configobj import ConfigObj

# Source.Python Imports
from core import GAME_NAME
from paths import PLUGIN_DATA_PATH


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Get the game's ini file
game_objects = ConfigObj(
    PLUGIN_DATA_PATH.joinpath('projectile_trails', GAME_NAME + '.ini'))


# =============================================================================
# >> CLASSES
# =============================================================================
class _ConfigurationManager(dict):

    """Class used to create children automatically to store cvars."""

    def __missing__(self, item):
        """Return a new _ConfigurationManager instance recursively."""
        value = self[item] = _ConfigurationManager()
        return value

# Get the _ConfigurationManager instance
configuration_manager = _ConfigurationManager()
