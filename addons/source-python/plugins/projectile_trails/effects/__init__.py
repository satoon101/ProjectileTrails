# ../projectile_trails/effects/__init__.py

"""Stores all valid effects for the current game."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   Importlib
from importlib import import_module

# Script Imports
from projectile_trails.config import game_objects
from projectile_trails.effects.base import BaseEffect


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Create an empty dictionary to store the effects by name and instance
effect_manager = {}

# Loop through each file in the effects folder
for effect, classname in game_objects['Effects'].iteritems():

    # Import the module
    module = import_module('projectile_trails.effects.' + effect)

    # Use try/except to add the object to the effect_manager dictionary
    try:

        # Get the class object
        instance = module.__dict__[classname]

    # Was an exception encountered?
    except KeyError:

        # Move on to the next effect
        continue

    # Use try/except in case the object is not a class object
    try:

        # Is the class object a BaseEffect sub-class?
        if not issubclass(instance, BaseEffect):

            # Move on to the next effect
            continue

    # Was an exception encountered?
    except TypeError:

        # Move on to the next effect
        continue

    # Add the instance to the dictionary
    effect_manager[effect] = instance()
