# ../projectile_trails/effects/beam.py

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
from projectile_trails.teams import GameTeams
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
    ''''''

    def __init__(self):
        ''''''
        self.variables['color'] = Variable(
            '255,0,0', beam_strings['Color'].get_string())

    def dispatch_effect(self, edict, team, start, end):
        ''''''

        #
        values = ConVar('lt_{0}_{1}_beam_color'.format(
            edict.get_class_name(), GameTeams[team].lower())).get_string()

        # Use try/except to split the color values
        try:

            #
            red, green, blue = map(int, values.split(','))

        #
        except ValueError:

            red = green = blue = 127

        #
        effects.beam(
            start, end, model_index, model_index, 0, 0,
            0.5, 10, 10, 1, 1, red, green, blue, 255, 30)
