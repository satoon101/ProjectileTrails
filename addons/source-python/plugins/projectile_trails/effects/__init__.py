# ../projectile_trails/effects/__init__.py

"""Stores all valid effects for the current game."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from importlib import import_module

# Site-package
from path import Path

# Plugin
from .base import BaseEffect
from ..info import info


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'EFFECT_DICTIONARY',
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Create an empty dictionary to store the effects by name and instance
EFFECT_DICTIONARY = {}

# Loop through each file in the effects folder
for _file in Path(__file__).parent.files('[a-z]*'):
    _module = import_module(f'{info.name}.effects.{_file.stem}')
    for _item in getattr(_module, '__all__', []):
        _instance = getattr(_module, _item)
        if issubclass(_instance, BaseEffect) and _instance is not BaseEffect:
            EFFECT_DICTIONARY[_item.lower()] = _instance
