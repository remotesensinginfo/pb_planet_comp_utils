#!/usr/bin/env python
"""
Setup script for pb_planet_comp_utils.

"""
#  This file is part of 'pb_planet_comp_utils'
#  Copyright (C) 2022  Pete Bunting
#
# Purpose:  Installation of the pb_planet_comp_utils module
#
# Author: Pete Bunting
# Email: pfb@aber.ac.uk
# Date: 24/11/2022
# Version: 1.0
#
# History:
# Version 1.0 - Created.

from setuptools import setup

import pbpcu

setup(name='pbpcu',
    version=pbpcu.PBPCU_VERSION,
    description='PB Plantary Computer Utilities',
    author='Pete Bunting',
    author_email='pfb@aber.ac.uk',
    packages=['pbpcu', 'pbpcu/sentinel2', 'pbpcu/landsat'],
    license='LICENSE.txt',
    url='https://github.com/remotesensinginfo/pb_planet_comp_utils',
    classifiers=['Intended Audience :: Developers',
                 'Intended Audience :: Remote Sensing Scientists',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 3.8'
                 'Programming Language :: Python :: 3.9'
                 'Programming Language :: Python :: 3.10',
                 'Programming Language :: Python :: 3.11'])
