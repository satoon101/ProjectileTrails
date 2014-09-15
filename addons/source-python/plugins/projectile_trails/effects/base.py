# ../projectile_trails/effects/base.py

"""Provides a base class for all effects to inherit."""


# =============================================================================
# >> CLASSES
# =============================================================================
class BaseEffect(object):

    """Base class used for all effects.

    Effects must override existing methods to utilize them.
    """

    def __new__(cls):
        """Create the new instance and adds the variables attribute."""
        cls = object.__new__(cls)
        cls.variables = _VariableDictionary()
        return cls

    def dispatch_effect(self, edict, team, start, end):
        """Called when the effect should be dispatched for the given edict.

        This is called every tick for entities as long as
            they have moved since the previous tick.

        Effects that attach to entities should store the edict
            on attachment in a data structure.
        """

    def remove_effect(self, edict):
        """Called when the effect should be removed from the given edict.

        This is called when the script is being unloaded.
        """

    def remove_index(self, index):
        """Called when the index is no longer on the server.

        This is called so that effects that attach to an entity
            can remove the entity from their data structure.
        """


class _VariableDictionary(dict):

    """Dictionary class used to store Variable instances."""

    def __setitem__(self, item, value):
        """Verify that the given instance is a Variable instance."""
        # Is the given value a Variable instance?
        if not isinstance(value, Variable):

            # If not, raise an error
            raise ValueError('Value must be a Variable instance')

        # Set the item in the dictionary
        super(_VariableDictionary, self).__setitem__(item, value)


class Variable(object):

    """Class to be used by effects to create effect specific variables."""

    def __init__(self, default, description):
        """Store the base attributes of the cvar."""
        self.default = default
        self.description = description
