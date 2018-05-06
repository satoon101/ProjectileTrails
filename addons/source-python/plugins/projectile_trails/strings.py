# ../projectile_trails/strings.py

"""Contains all translation variables for the base plugin."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from translations.strings import LangStrings

# Plugin
from .info import info


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'CONFIG_STRINGS',
    'TRANSLATION_STRINGS',
)


# =============================================================================
# >> GAME VERIFICATION
# =============================================================================
CONFIG_STRINGS = LangStrings(info.name + '/config_strings')
TRANSLATION_STRINGS = LangStrings(info.name + '/strings')
