# ../projectile_trails/effects/beam.py

"""Provides a beam trail effect."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from colors import Color
from core import SOURCE_ENGINE
from effects.base import TempEntity
from engines.precache import Model
from translations.strings import LangStrings

# Plugin
from ..info import info
from .base import BaseEffect, VARIABLE


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'Beam',
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Pre-cache the beam model
_model = Model(
    'sprites/laser{suffix}.vmt'.format(
        suffix='beam' if SOURCE_ENGINE == 'csgo' else ''
    )
)

# Get the LangStrings for beam effect
BEAM_STRINGS = LangStrings(info.name + '/beam_strings')


# =============================================================================
# >> CLASSES
# =============================================================================
class Beam(BaseEffect):
    """Beam trail effect."""

    variables = {
        'beam_color': VARIABLE(
            default='255,0,0',
            description=BEAM_STRINGS['Color'].get_string(),
        )
    }

    def create_trail(self):
        """Create the beam trail for the given entity."""
        # Get the values for the beam color
        rgb = str(self.convars['beam_color'])

        # Use try/except to split the color values
        try:
            color = Color(*map(int, rgb.split(',')))

        # Otherwise, set the colors to a default value
        except ValueError:
            color = Color(127, 127, 127)

        # Create the beam effect
        entity = TempEntity('BeamFollow')
        entity.start_width = 6
        entity.end_width = 6
        entity.color = color
        entity.model = _model
        entity.halo = _model
        entity.entity_index = self.entity.index
        entity.life_time = 2
        entity.create()
