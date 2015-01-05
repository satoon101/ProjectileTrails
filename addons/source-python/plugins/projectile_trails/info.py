# ../projectile_trails/info.py

"""Provides/stores information about the plugin."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
from cvars.public import PublicConVar
#   Addons
from plugins.info import PluginInfo


# =============================================================================
# >> ADDON INFO
# =============================================================================
info = PluginInfo()
info.name = 'Projectile Trails'
info.author = 'Satoon101'
info.version = '1.0'
info.basename = 'projectile_trails'
info.variable = info.basename + '_version'
info.url = ''
info.convar = PublicConVar(
    info.variable, info.version, 0, info.name + ' Version')
