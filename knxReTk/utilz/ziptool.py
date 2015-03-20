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

from collections import namedtuple
import hashlib
import os
import sys
import zipfile


ImageRecord = namedtuple("ImageRecord", "image fsPath hash")

def getZipFileContents(fname, password = None):
    absPath = os.path.abspath(os.path.split(fname)[0])
    subDirectory = os.path.splitext(os.path.split(fname)[1])[0]
    targetDirectoty = os.path.join(absPath, subDirectory)
    with zipfile.ZipFile(fname) as zf:
        #zf.printdir()
        for fl in zf.filelist:
            inf = zf.open(fl, 'r', password)
            completePath = os.path.join(targetDirectoty, fl.filename)
            basedir, filename = os.path.split(completePath)
            if not os.access(basedir, os.F_OK):
                os.makedirs(basedir)
            image = inf.read()
            yield ImageRecord(image, fl.filename,  hashlib.sha1(image).hexdigest())

