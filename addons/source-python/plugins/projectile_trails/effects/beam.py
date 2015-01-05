# ../projectile_trails/effects/beam.py

"""Provides a beam trail effect."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
from core import SOURCE_ENGINE
from cvars import ConVar
from engines.precache import Model
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
model = Model('sprites/laser{0}.vmt'.format(
    'beam' if SOURCE_ENGINE == 'csgo' else ''))

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

    def dispatch_effect(self, instance):
        """Create the beam trail for the given edict."""
        # Get the values for the beam color
        values = ConVar(
            'lt_{0}_{1}_beam_color'.format(instance.classname, game_teams[
                instance.team_number].lower())).get_string()

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
            instance.origin, instance.location, model.index, model.index,
            0, 0, 0.5, 10, 10, 1, 1, red, green, blue, 255, 30)
