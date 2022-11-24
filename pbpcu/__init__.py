#!/usr/bin/env python
"""
PBPCU - PB Planetary Computer Utilities

See other source files for details
"""

from distutils.version import LooseVersion

PBPCU_VERSION_MAJOR = 0
PBPCU_VERSION_MINOR = 0
PBPCU_VERSION_PATCH = 2

PBPCU_VERSION = f"{PBPCU_VERSION_MAJOR}.{PBPCU_VERSION_MINOR}.{PBPCU_VERSION_PATCH}"
PBPCU_VERSION_OBJ = LooseVersion(PBPCU_VERSION)
__version__ = PBPCU_VERSION

PBPCU_COPYRIGHT_YEAR = "2022"
PBPCU_COPYRIGHT_NAMES = "Pete Bunting"
