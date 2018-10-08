"""
"""

import os

PATH_VERSION = "VERSION"

MODULE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), '')

path_version = os.path.join(MODULE_PATH, PATH_VERSION)
with open(path_version, 'r') as inn:
    version = inn.read().strip()

__version__ = version

# flake8: noqa  --- ignore imported but unused flake8 warnings

from . deep_core import Core
from . settings import Settings
from . paths import Paths
