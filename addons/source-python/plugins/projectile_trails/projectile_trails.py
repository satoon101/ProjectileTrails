# ../projectile_trails/projectile_trails.py

"""Displays trail effects for projectile weapons."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from random import choice

# Source.Python
from core import GAME_NAME
from engines.server import global_vars
from listeners import OnEntitySpawned, OnEntityDeleted, OnTick
from weapons.entity import Weapon

# Plugin
from . import PROJECTILE_ENTITIES
from .config import EFFECT_CONVARS, ticks
from .effects import EFFECT_DICTIONARY
from .strings import TRANSLATION_STRINGS
from .teams import GAME_TEAMS


# =============================================================================
# >> GAME VERIFICATION
# =============================================================================
# Are any projectiles listed for the game?
if not PROJECTILE_ENTITIES:
    raise NotImplementedError(
        TRANSLATION_STRINGS['No Projectiles'].get_string().format(
            game=GAME_NAME,
        )
    )

# Are there any valid teams for the game?
if not GAME_TEAMS:
    raise NotImplementedError(
        TRANSLATION_STRINGS['No Teams'].get_string().format(
            game=GAME_NAME,
        )
    )


# =============================================================================
# >> CLASSES
# =============================================================================
class _GameEntityManager(dict):
    """Class used to hold EntityManager instances for each entity."""

    def __delitem__(self, index):
        """Remove the trail from the entity prior to removing it from dict."""
        if index not in self:
            return

        self[index].remove_trail()
        super().__delitem__(index)

    def add_entity(self, entity, convars):
        """Add the entity to the dictionary if it needs a trail effect."""
        effect = self._get_effect(convars)
        if effect is not None:
            self[entity.index] = effect(entity, convars)

    @staticmethod
    def _get_effect(convars):
        """Return the effect to be used for the entity."""
        effect = str(convars['effect']).lower()
        if effect in EFFECT_DICTIONARY:
            return EFFECT_DICTIONARY[effect]

        if effect == 'random':
            return choice(EFFECT_DICTIONARY.values())

        return None

    def clear(self):
        """Stop all ongoing effects and clear the dictionary."""
        for index in list(self):
            del self[index]

    def tick_listener(self):
        """Check to see if the effects need updated."""
        # Are more ticks needed to update?
        if global_vars.tick_count % int(ticks):
            return

        for instance in self.values():
            instance.update_trail()

game_entity_manager = _GameEntityManager()


# =============================================================================
# >> LISTENERS
# =============================================================================
@OnEntitySpawned
def _entity_spawned(base_entity):
    """Add the entity to the dictionary if it is a projectile."""
    if not base_entity.is_networked():
        return

    class_name = base_entity.classname
    if class_name not in PROJECTILE_ENTITIES:
        return

    projectile = Weapon(base_entity.index)
    team_index = projectile.owner.team_index
    if team_index in EFFECT_CONVARS[class_name]:
        game_entity_manager.add_entity(
            entity=base_entity,
            convars=EFFECT_CONVARS[class_name][team_index],
        )


@OnEntityDeleted
def _entity_deleted(base_entity):
    """Remove the entity from the dictionary if it is a projectile."""
    if not base_entity.is_networked():
        return

    index = base_entity.index
    del game_entity_manager[index]


@OnTick
def _on_tick():
    """Call the tick listener."""
    game_entity_manager.tick_listener()
