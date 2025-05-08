# ../projectile_trails/effects/dust.py

"""Provides a dust trail effect."""

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
    "Dust",
)


# =============================================================================
# >> CLASSES
# =============================================================================
class Dust(BaseEffect):
    """Dust trail effect."""

    def update_trail(self):
        """Create the smoke trail for the given entity."""
        entity = TempEntity("Dust")
        entity.origin = self.entity.origin
        entity.size = 20
        self.create_temp_entity(entity)
