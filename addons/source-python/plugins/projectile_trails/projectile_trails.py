# ../projectile_trails/projectile_trails.py

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
from core import GAME_NAME
#   Config
from config.manager import ConfigManager
#   Tick
from listeners import tick_listener_manager
#   Translations
from translations.strings import LangStrings

# Script Imports
from projectile_trails.config import ConfigurationManager
from projectile_trails.config import GameObjects
from projectile_trails.effects import EffectManager
from projectile_trails.entities import EntityManager
from projectile_trails.info import info
from projectile_trails.teams import GameTeams


# =============================================================================
# >> GAME VERIFICATION
# =============================================================================
# Get the NotImplemented string
_not_implemented = LangStrings(
    '{0}/strings'.format(info.basename))[
        'NotImplemented'].get_string().format(GAME_NAME)

# Is the game implemented?
if not GameObjects:

    # If not, raise an error
    raise NotImplementedError(_not_implemented)

# Are any projectiles listed for the game?
if not ('Projectiles' in GameObjects and len(GameObjects['Projectiles'])):

    # If not, raise an error
    raise NotImplementedError(_not_implemented)

# Use try/except to get the first effect for the current game
try:

    # Get the first effect listed
    _first = list(EffectManager)[0]

# Was an error encountered?
except IndexError:

    # If there are no effects, raise an error
    raise NotImplementedError(_not_implemented)


# =============================================================================
# >> PUBLIC VARIABLE
# =============================================================================
# Set the variable's value (in case it has already been created)
info.convar.set_string(info.version)

# Make the variable public
info.convar.make_public()


# =============================================================================
# >> CLASSES
# =============================================================================
class _GameEntityManager(dict):
    '''Class used to hold EntityManager instances for each entity'''

    def __init__(self):
        '''Initializes the process'''

        # Set the base tick counter
        self.current_ticks = 0

        # Loop through all entities
        for entity in GameObjects['Projectiles']:

            # Add the entity to the dictionary
            self[entity] = EntityManager(
                entity, GameObjects['Projectiles'][entity])

    def clear(self):
        '''Stops all ongoing effects and clears the dictionary'''

        # Loop through all entities in the dictionary
        for entity in self:

            # Clear the entity's dictionary
            self[entity].clear()

        # Clear the dictionary
        super(_GameEntityManager, self).clear()

    def tick_listener(self):
        '''Checks to see if the effects need updated'''

        # Increment the current tick count
        self.current_ticks += 1

        # Are more ticks needed to update?
        if self.current_ticks < ConfigurationManager.ticks.get_int():

            # If so, return
            return

        # Reset the base tick counter
        self.current_ticks = 0

        # Loop through all projectile entities for the game
        for entity in self:

            # Find all current indexes for the entity
            self[entity].find_indexes()

# Get the _GameEntityManager instance
GameEntityManager = _GameEntityManager()


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
    ConfigurationManager.ticks = config.cvar(
        'lt_wait_ticks', '7', 0, config_strings['Ticks'])

    # Loop through each entity
    for entity in GameEntityManager:

        # Create the entity's section
        config.section(_options.format(entity.upper()))

        # Loop through each team the entity supports
        for team in GameEntityManager[entity].teams:

            # Create a subsection for the team
            text = _options.format(
                entity.upper() + ' ' + GameTeams[team].upper())
            config.text('=' * len(text) + ' //')
            config.text(text + ' //')
            config.text('=' * len(text) + ' //')

            # Create the entity->team cvar
            cvar = ConfigurationManager[entity][team].cvar = config.cvar(
                'lt_{0}_{1}'.format(entity, GameTeams[team].lower()),
                _first, 0, _team_cvar.format(GameTeams[team], entity))

            # Loop through each effect
            for effect in EffectManager:

                # Loop through all variables for the effect
                for variable in EffectManager[effect].variables:

                    # Get the variable's name
                    name = 'lt_{0}_{1}_{2}_{3}'.format(
                        entity, GameTeams[team].lower(), effect, variable)

                    # Get the variable's default value
                    default = EffectManager[effect].variables[variable].default

                    # Get the variable's description
                    description = EffectManager[
                        effect].variables[variable].description

                    # Add the enity->team->effect->variable
                    # cvar to the dictionary
                    ConfigurationManager[
                        entity][team][effect][variable].cvar = config.cvar(
                            name, default, 0, description)


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def load():
    '''Registers the tick listener on load'''
    tick_listener_manager.register_listener(GameEntityManager.tick_listener)


def unload():
    '''Cleans up on script unload'''

    # Unregister the tick listener
    tick_listener_manager.unregister_listener(GameEntityManager.tick_listener)

    # Clear the entity manager to stop all active effects
    GameEntityManager.clear()
