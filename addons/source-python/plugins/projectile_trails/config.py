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

    _config.text(CONFIG_STRINGS['Options'])
    _config.text('"' + '", "'.join(EFFECT_DICTIONARY) + '"')

    for _proj, _weapon in PROJECTILE_ENTITIES.items():
        _config.section(
            CONFIG_STRINGS['Section:Weapon'].get_string(
                weapon=_weapon.upper(),
            )
        )
        for _team_num, _team_name in GAME_TEAMS.items():
            _team_name = _team_name.lower()
            _config.text('-' * 40 + ' //')
            _config.text(
                CONFIG_STRINGS['Section:Team'].get_string(
                    team=_team_name.upper(),
                ).center(40) + ' //'
            )
            _config.text('-' * 40 + ' //')
            EFFECT_CONVARS[_proj][_team_num]['effect'] = _config.cvar(
                name=f'{_weapon}_{_team_name}_effect',
                default='beam',
                description=CONFIG_STRINGS['Cvar:Description'].get_string(
                    weapon=_weapon,
                    team=_team_name.upper(),
                )
            )
            for _variable, _instance in _variables.items():
                EFFECT_CONVARS[_proj][_team_num][_variable] = _config.cvar(
                    name=f'{_weapon}_{_team_name}_{_variable}',
                    default=_instance.default,
                    description=_instance.description.get_string(
                        weapon=_weapon,
                        team=_team_name.upper(),
                    ),
                )
