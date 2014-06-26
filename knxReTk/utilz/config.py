#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = """
   Konnex / EIB Reverserz Toolkit

   (C) 2001-2014 by Christoph Schueler <cpu12.gems@googlemail.com>

   All Rights Reserved

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License along
   with this program; if not, write to the Free Software Foundation, Inc.,
   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

   s. FLOSS-EXCEPTION.txt
"""
__author__  = 'Christoph Schueler'
__version__ = '0.1.0'

import os
import pkgutil
import zlib

from knxReTk.utilz.logger import logger, verboseLevel

# TODO: loadProjectConfig, loadUserConfig, saveUserConfig

verboseLevel()


def homeDirectory():
    return os.path.abspath(os.path.expanduser('~/'))    # Works also under Windows -- really.

def projectConfigurationDirectory(project):
    path = os.path.join(homeDirectory(), project)
    if not os.access(path, os.F_OK):
        logger.info("Creating configuration directory '%s'" % path)
        os.mkdir(path)
        print
    return path

print projectConfigurationDirectory('knxReTk')

"""

def absConfigurationFilename(fname):
    return os.path.join(CONFIGURATION_DIRECTORY, fname)

"""

def readConfigData(project, fname):
    return pkgutil.get_data(project, 'config/%s' % fname)

def masterXML():
    return zlib.decompress(readConfigData('knxReTk', 'knx_master.Z'))

