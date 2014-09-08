# ../projectile_trails/config.py

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
GameObjects = ConfigObj(
    PLUGIN_DATA_PATH.joinpath('projectile_trails', GAME_NAME + '.ini'))


# =============================================================================
# >> CLASSES
# =============================================================================
class _ConfigurationManager(dict):
    '''Class used to create children automatically to store cvars'''

    def __missing__(self, item):
        '''Returns a new _ConfigurationManager
            instance as the value for the given item'''
        value = self[item] = _ConfigurationManager()
        return value

# Get the _ConfigurationManager instance
ConfigurationManager = _ConfigurationManager()
