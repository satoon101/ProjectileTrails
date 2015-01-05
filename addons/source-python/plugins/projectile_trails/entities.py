# ../projectile_trails/entities.py

"""Provides a class that creates trails for entities."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   Contextlib
from contextlib import suppress
#   Random
from random import choice

# Source.Python Imports
from entities.entity import BaseEntity
from entities.helpers import index_from_inthandle
#   Filters
from filters.entities import EntityIter
#   Players
from players.entity import PlayerEntity

# Script Imports
from projectile_trails.config import configuration_manager
from projectile_trails.effects import effect_manager
from projectile_trails.teams import game_teams


# =============================================================================
# >> CLASSES
# =============================================================================
class EntityManager(dict):

    """Dictionary class used to store edicts for the instantiating entity."""

    def __init__(self, classname, teams):
        """Store the entity and the teams for the entity."""
        # Call super's init
        super(EntityManager, self).__init__()

        # Store the entity
        self.classname = classname

        # Store the teams for the entity
        self.teams = frozenset(
            [int(x) for x in teams.split(',') if int(x) in game_teams])

    def __missing__(self, index):
        """Called when a new edict is being added to the dictionary."""
        # Add the entity to the dictionary
        instance = self[index] = IndexManager(index)

        # Set the location for the entity
        instance.location = instance.origin

        # Get the team for the entity
        instance.team = self.get_team_number(instance)

        # Get the effect for the entity
        instance.effect = self.get_effect(instance.team)

        # Return the IndexManager instance
        return instance

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
        indexlist = {[index for index in EntityIter(self.classname)]}

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

    def get_team_number(self, instance):
        """Return the team number to use for the edict."""
        # Is the entity's team number in the entity's team list?
        if instance.team in self.teams:

            # Return the edict's team number
            return instance.team

        # Try to get the owner's index
        with suppress(ValueError):

            # Get the owner of the entity
            owner = PlayerEntity(index_from_inthandle(instance.owner))

            # Return the owner's team
            return owner.team

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
            self.classname][team].cvar.get_string().lower()

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


class IndexManager(BaseEntity):

    """Class used to interact with an edict and its effect."""

    # Set the base attributes
    team_number = None
    effect = None
    location = None

    def create_trail(self):
        """Create the trail for the edict."""
        # Is the location the same as the previous?
        if self.origin == self.location:

            # No need to do anything
            return

        # Dispatch the effect for the edict
        # with its old location and new location
        self.effect.dispatch_effect(self)

        # Set the stored location to the current location
        self.location = self.origin

    def remove_trail(self):
        """Remove the trail from the edict."""
        self.effect.remove_effect(self)
