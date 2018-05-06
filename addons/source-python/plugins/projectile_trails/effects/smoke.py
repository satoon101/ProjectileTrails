# ../projectile_trails/effects/smoke.py

"""Provides a smoke trail effect."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from effects.base import TempEntity
from engines.precache import Model

# Plugin
from .base import BaseEffect


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'Smoke',
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Pre-cache the smoke model
_model = Model('sprites/smoke.vmt')


# =============================================================================
# >> CLASSES
# =============================================================================
class Smoke(BaseEffect):
    """Smoke trail effect."""

    def update_trail(self):
        """Create the smoke trail for the given entity."""
        entity = TempEntity('Smoke')
        entity.origin = self.entity.origin
        entity.model = _model
        entity.scale = 1
        entity.create()
