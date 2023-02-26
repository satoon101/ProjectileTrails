# ../projectile_trails/effects/base.py

"""Provides a base class for all effects to inherit."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from collections import namedtuple

# Source.Python
from filters.players import PlayerIter
from filters.recipients import RecipientFilter
from mathlib import Vector
from players.teams import teams_by_number


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'BaseEffect',
    'VARIABLE',
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
VARIABLE = namedtuple('VARIABLE', ('default', 'description'))


# =============================================================================
# >> CLASSES
# =============================================================================
class BaseEffect:
    """Base class used for all effects.

    Effects must override existing methods to utilize them.
    """

    variables = {}

    def __init__(self, entity, convars, team_index):
        """Store the given information and create the trail."""
        super().__init__()
        self.entity = entity
        self.location = Vector(*self.entity.origin)
        self.convars = convars
        self.team_index = team_index
        self.create_trail()

    def get_recipients(self):
        """Return a RecipientFilter for the recipients of the effect."""
        # pylint: disable=import-outside-toplevel
        # pylint: disable=cyclic-import
        from ..config import team_only
        team_filter = ()
        if bool(team_only):
            team_filter = PlayerIter(teams_by_number[self.team_index])
        return RecipientFilter(*team_filter)

    def get_updated_locations(self):
        """Update the stored location and return both the old and new."""
        location = self.location
        self.location = Vector(*self.entity.origin)
        return location, self.location

    def create_temp_entity(self, entity):
        """Create the temp entity with the necessary recipients."""
        entity.create(self.get_recipients())

    def create_trail(self):
        """Create the trail on initialization."""

    def update_trail(self):
        """Create/update the trail for each interval."""

    def remove_trail(self):
        """Remove the effect from the entity."""
