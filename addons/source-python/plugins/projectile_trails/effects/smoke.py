# ../projectile_trails/effects/smoke.py

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
# 
model_index = engine_server.precache_model('sprites/smoke.vmt')


# =============================================================================
# >> CLASSES
# =============================================================================
class Smoke(BaseEffect):
    ''''''

    def dispatch_effect(self, edict, team, start, end):
        ''''''
        effects.smoke(end, model_index, 5, 0.1)
