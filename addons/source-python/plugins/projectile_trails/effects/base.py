# ../projectile_trails/effects/base.py

"""Provides a base class for all effects to inherit."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from collections import namedtuple

# Source.Python
from mathlib import Vector


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
class BaseEffect(object):
    """Base class used for all effects.

    Effects must override existing methods to utilize them.
    """

    variables = {}

    def __init__(self, entity, convars):
        """Store the given information and create the trail."""
        super().__init__()
        self.entity = entity
        self.location = Vector(*self.entity.origin)
        self.convars = convars
        self.create_trail()

    def get_updated_locations(self):
        """Update the stored location and return both the old and new."""
        location = self.location
        self.location = Vector(*self.entity.origin)
        return location, self.location

    def create_trail(self):
        """Create the trail on initialization."""

    def update_trail(self):
        """Create/update the trail for each interval."""

    def remove_trail(self):
        """Remove the effect from the entity."""
