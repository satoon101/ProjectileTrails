# ../projectile_trails/effects/sparks.py

"""Provides a sparks trail effect."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from effects.base import TempEntity

# Plugin
from .base import BaseEffect

# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    "Sparks",
)


# =============================================================================
# >> CLASSES
# =============================================================================
class Sparks(BaseEffect):
    """Sparks trail effect."""

    def update_trail(self):
        """Create the sparks trail for the given entity."""
        entity = TempEntity("Sparks")
        entity.origin = self.entity.origin
        direction = self.entity.base_velocity
        direction.negate()
        entity.direction = direction
        entity.trail_length = 3
        entity.magnitude = 1
        self.create_temp_entity(entity)
