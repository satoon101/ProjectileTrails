# ../projectile_trails/config.py

"""Provides configuration based functionality for the plugin."""


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
