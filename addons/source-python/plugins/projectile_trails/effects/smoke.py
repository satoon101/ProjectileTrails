# ../projectile_trails/effects/smoke.py

"""Provides a smoke trail effect."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
from engines.server import engine_server
from effects import effects

# Script Imports
from projectile_trails.effects.base import BaseEffect


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Precache the smoke model
model_index = engine_server.precache_model('sprites/smoke.vmt')


# =============================================================================
# >> CLASSES
# =============================================================================
class Smoke(BaseEffect):

    """Smoke effect."""

    def dispatch_effect(self, instance):
        """Create the smoke trail for the given edict."""
        effects.smoke(instance.location, model_index, 5, 0.1)
