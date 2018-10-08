"""
"""

with open('VERSION') as inn:
    version = inn.read().strip()

__version__ = version

# flake8: noqa  --- ignore imported but unused flake8 warnings

from . deep_core import Core
from . settings import Settings
from . paths import Paths
