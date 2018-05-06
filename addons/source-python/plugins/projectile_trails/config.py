# ../projectile_trails/config.py

"""Provides configuration based functionality for the plugin."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from collections import defaultdict
from operator import attrgetter

# Source.Python
from config.manager import ConfigManager

# Plugin
from . import PROJECTILE_ENTITIES
from .effects import EFFECT_DICTIONARY
from .info import info
from .strings import CONFIG_STRINGS
from .teams import GAME_TEAMS


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'EFFECT_CONVARS',
    'ticks',
)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
_variables = dict([
    (key, instance[key]) for instance in list(
        map(
            attrgetter('variables'),
            EFFECT_DICTIONARY.values()
        )
    ) for key in instance
])

EFFECT_CONVARS = defaultdict(lambda: defaultdict(dict))

with ConfigManager(info.name, 'pt_') as _config:
    ticks = _config.cvar(
        name='ticks_between_check',
        description=CONFIG_STRINGS['Ticks'],
        default=7,
    )

    for _weapon in PROJECTILE_ENTITIES:
        # TODO: create weapon section
        for _team_num, _team_name in GAME_TEAMS.items():
            _team_name = _team_name.lower()
            # TODO: create team section
            # TODO: add choices
            # TODO: add description
            EFFECT_CONVARS[_weapon][_team_num]['effect'] = _config.cvar(
                name=f'{_weapon}_{_team_name}_effect',
                default='beam',
            )
            # TODO: add effect specific cvars
            for _variable, _instance in _variables.items():
                EFFECT_CONVARS[_weapon][_team_num][_variable] = _config.cvar(
                    name=f'{_weapon}_{_team_name}_{_variable}',
                    default=_instance.default,
                    description=_instance.description,
                )
