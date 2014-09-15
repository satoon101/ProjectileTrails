# ../projectile_trails/entities.py

"""Provides a class that creates trails for entities."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   Random
from random import choice

# Source.Python Imports
from entities import EntityGenerator
from entities.helpers import edict_from_index
from entities.helpers import index_from_edict
#   Filters
from filters.players import PlayerIter

# Script Imports
from projectile_trails.config import configuration_manager
from projectile_trails.effects import effect_manager
from projectile_trails.teams import game_teams


# =============================================================================
# >> CLASSES
# =============================================================================
class EntityManager(dict):

    """Dictionary class used to store edicts for the instantiating entity."""

    def __init__(self, entity, teams):
        """Store the entity and the teams for the entity."""
        # Store the entity
        self.entity = entity

        # Store the teams for the entity
        self.teams = frozenset(
            [int(x) for x in teams.split(',') if int(x) in game_teams])

    def __missing__(self, index):
        """Called when a new edict is being added to the dictionary."""
        # Get the Edict instance for the index
        edict = edict_from_index(index)

        # Get the team for the edict
        team = self.get_team_number(edict)

        # Get the effect for the edict
        effect = self.get_effect(team)

        # Add the edict to the dictionary
        value = self[index] = IndexManager(edict, team, effect)

        # Return the IndexManager instance
        return value

    def clear(self):
        """Clear the dictionary after removing all trails."""
        # Loop through each edict in the dictionary
        for index in self:

            # Remove the trail from the edict
            self[index].remove_trail()

        # Clear the dictionary
        super(EntityManager, self).clear()

    def find_indexes(self):
        """Find all current indexes and dispatch effects."""
        # Get a set of edicts currently on the server for the entity type
        indexlist = {
            index_from_edict(edict) for
            edict in EntityGenerator(self.entity, True)}

        # Loop through the current edicts in the
        # dictionary that are no longer on the server
        for index in set(self).difference(indexlist):

            # Does the effect need removed for the current index?
            if not self[index].effect is None:

                # Remove the effect from the index
                self[index].effect.remove_index(index)

            # Remove the index from the dictionary
            del self[index]

        # Loop through all edicts currently on the server
        for index in indexlist:

            # Does the entity need an effect dispatched?
            if not self[index].effect is None:

                # Create the trail
                self[index].create_trail()

    def get_team_number(self, edict):
        """Return the team number to use for the edict."""
        # Get the edict's team number
        team = edict.get_prop_int('m_iTeamNum')

        # Is the edict's team number in the entity's team list?
        if team in self.teams:

            # Return the edict's team number
            return team

        # Get the handle of the owner of the edict
        owner = edict.get_prop_int('m_hOwnerEntity')

        # Loop through all players on the server by their inthandle and team
        for handle, team in PlayerIter(return_types=['inthandle', 'team']):

            # Is the current player the owner of the edict?
            if handle == owner:

                # Return the current player's team
                return team

        # Is 0 a valid team for the entity?
        if 0 in self.teams:

            # Return 0
            return 0

        # Return a random team from the entity's team list
        return choice(list(self.teams))

    def get_effect(self, team):
        """Return the effect to use for the edict."""
        # Get the effect name from the entity->team cvar
        name = configuration_manager[
            self.entity][team].cvar.get_string().lower()

        # Is the effect name in the effect_manager?
        if name in effect_manager:

            # Return the effect's instance
            return effect_manager[name]

        # Is the effect set to random?
        if name == 'random':

            # Return a random effect from the effect_manager
            return effect_manager[choice(list(effect_manager))]

        # Return None (no effect for this entity)
        return None


class IndexManager(object):

    """Class used to interact with an edict and its effect."""

    def __init__(self, edict, team, effect):
        """Store the base attributes on instatiation."""
        # Store the edict
        self.edict = edict

        # Store the team number
        self.team = team

        # Store the effect
        self.effect = effect

        # Store the edict's current location vector
        self.location = self.edict.get_prop_vector('m_vecOrigin')

    def create_trail(self):
        """Create the trail for the edict."""
        # Get the edict's current location vector
        location = self.edict.get_prop_vector('m_vecOrigin')

        # Is the location the same as the previous?
        if location == self.location:

            # No need to do anything
            return

        # Dispatch the effect for the edict
        # with its old location and new location
        self.effect.dispatch_effect(
            self.edict, self.team, location, self.location)

        # Set the stored location to the current location
        self.location = location

    def remove_trail(self):
        """Remove the trail from the edict."""
        self.effect.remove_effect(self.edict)
