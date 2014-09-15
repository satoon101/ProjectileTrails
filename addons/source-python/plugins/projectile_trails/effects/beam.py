# ../projectile_trails/effects/beam.py

"""Provides a beam trail effect."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
from cvars import ConVar
from engines.server import engine_server
from effects import effects
#   Translations
from translations.strings import LangStrings

# Script Imports
from projectile_trails.info import info
from projectile_trails.teams import game_teams
from projectile_trails.effects.base import BaseEffect
from projectile_trails.effects.base import Variable


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Precache the beam model
model_index = engine_server.precache_model('sprites/laser.vmt')

# Get the LangStrings for beam effect
beam_strings = LangStrings(info.basename + '/beam_strings')


# =============================================================================
# >> CLASSES
# =============================================================================
class Beam(BaseEffect):

    """Beam effect."""

    def __init__(self):
        """Create the color cvar."""
        self.variables['color'] = Variable(
            '255,0,0', beam_strings['Color'].get_string())

    def dispatch_effect(self, edict, team, start, end):
        """Create the beam trail for the given edict."""
        # Get the values for the beam color
        values = ConVar('lt_{0}_{1}_beam_color'.format(
            edict.get_class_name(), game_teams[team].lower())).get_string()

        # Use try/except to split the color values
        try:

            # Get the rgb values
            red, green, blue = map(int, values.split(','))

        # Was an exception encountered?
        except ValueError:

            # Set the colors to a default value
            red = green = blue = 127

        # Create the beam effect
        effects.beam(
            start, end, model_index, model_index, 0, 0,
            0.5, 10, 10, 1, 1, red, green, blue, 255, 30)
