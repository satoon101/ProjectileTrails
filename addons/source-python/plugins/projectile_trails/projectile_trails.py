# ../projectile_trails/projectile_trails.py

"""Displays trail effects for projectile weapons."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Config
from config.manager import ConfigManager
#   Tick
from listeners import tick_listener_manager
#   Translations
from translations.strings import LangStrings
#   Weapons
from weapons import weapon_manager

# Script Imports
from projectile_trails.config import configuration_manager
from projectile_trails.effects import effect_manager
from projectile_trails.entities import EntityManager
from projectile_trails.info import info
from projectile_trails.teams import game_teams


# =============================================================================
# >> CLASSES
# =============================================================================
class _GameEntityManager(dict):

    """Class used to hold EntityManager instances for each entity."""

    def __init__(self):
        """Initialize the process."""
        # Call the super class' init
        super(_GameEntityManager, self).__init__()

        # Set the base tick counter
        self.current_ticks = 0

        # Loop through all projectile entities
        for classname in weapon_manager.projectiles:

            # Add the entity to the dictionary
            self[classname] = EntityManager(classname)

    def clear(self):
        """Stop all ongoing effects and clears the dictionary."""
        # Loop through all entities in the dictionary
        for entity in self:

            # Clear the entity's dictionary
            self[entity].clear()

        # Clear the dictionary
        super(_GameEntityManager, self).clear()

    def tick_listener(self):
        """Check to see if the effects need updated."""
        # Increment the current tick count
        self.current_ticks += 1

        # Are more ticks needed to update?
        if self.current_ticks < configuration_manager.ticks.get_int():

            # If so, return
            return

        # Reset the base tick counter
        self.current_ticks = 0

        # Loop through all projectile entities for the game
        for entity in self:

            # Find all current indexes for the entity
            self[entity].find_indexes()

# Get the _GameEntityManager instance
game_entity_manager = _GameEntityManager()


# =============================================================================
# >> CONFIGURATION SETUP
# =============================================================================
# Get the LangStrings for the config file
config_strings = LangStrings('{0}/config_strings'.format(info.basename))

# Store the common strings
_options = config_strings['Options'].get_string()
_team_cvar = config_strings['TeamCvar'].get_string()

# Create the config file
with ConfigManager(info.basename) as config:

    # Add the config header
    config.header = config_strings[
        'Main'].get_string().format(info.name, info.version)

    # Create the tick cvar
    configuration_manager.ticks = config.cvar(
        'lt_wait_ticks', '7', 0, config_strings['Ticks'])

    # Loop through each entity
    for _entity in game_entity_manager:

        # Create the entity's section
        config.section(_options.format(_entity.upper()))

        # Loop through each team the entity supports
        for team in game_entity_manager[_entity].teams:

            # Create a subsection for the team
            text = _options.format(
                _entity.upper() + ' ' + game_teams[team].upper())
            config.text('=' * len(text) + ' //')
            config.text(text + ' //')
            config.text('=' * len(text) + ' //')

            # Create the entity->team cvar
            cvar = configuration_manager[_entity][team].cvar = config.cvar(
                'lt_{0}_{1}'.format(_entity, game_teams[team].lower()),
                'smoke', 0, _team_cvar.format(game_teams[team], _entity))

            # Loop through each effect
            for effect in effect_manager:

                # Loop through all variables for the effect
                for variable in effect_manager[effect].variables:

                    # Get the variable's name
                    name = 'lt_{0}_{1}_{2}_{3}'.format(
                        _entity, game_teams[team].lower(), effect, variable)

                    # Get the variable's default value
                    default = effect_manager[
                        effect].variables[variable].default

                    # Get the variable's description
                    description = effect_manager[
                        effect].variables[variable].description

                    # Add the enity->team->effect->variable
                    # cvar to the dictionary
                    configuration_manager[
                        _entity][team][effect][variable].cvar = config.cvar(
                            name, default, 0, description)


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def load():
    """Register the tick listener on load."""
    tick_listener_manager.register_listener(game_entity_manager.tick_listener)


def unload():
    """Clean up on script unload."""
    # Unregister the tick listener
    tick_listener_manager.unregister_listener(
        game_entity_manager.tick_listener)

    # Clear the entity manager to stop all active effects
    game_entity_manager.clear()
