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

from collections import namedtuple, defaultdict
import re

from knxReTk.utilz.logger import logger

ValueProperty = namedtuple('ValueProperty', 'name value')
ArrayProperty = namedtuple('ArrayProperty', 'name value size')
MemorySection = namedtuple('MemorySection', 'start end r w x')
SECTION = re.compile(r'^\[(?P<name>[^]]*)\]$')
VALUE_PROPERTY = re.compile(r'^(?P<property>[^=]*)=\s*(?:0[xX])?(?P<value>[0-9a-fA-F]*)(?:\[(?P<arraySize>\d+)\])?\s*$')

MEMORY_SECTION = re.compile("""^(?P<property>[^=]*)=\s*(?:0[xX])?(?P<start>[0-9a-fA-F]*)
\s*,\s*(?:0[xX])?(?P<end>[0-9a-fA-F]*)\s*,\s*
(?P<attribs>[RWX]+)
\s*$""", re.VERBOSE)

class Symbols(object):

    def __init__(self, symbolData, mcu, mask):
        self.mcu = mcu
        self.mask = mask
        self.sections = defaultdict(list)
        currentSection = None
        for line in symbolData.splitlines():
            line = line.split('#', 2)
            line = line[0]
            line = line.strip()
            if not line: continue
            match = SECTION.match(line)
            if match:
                currentSection = match.group('name')
                currentSection = tuple(currentSection.split('.'))
                #print "Section:", currentSection
            else:
                match = VALUE_PROPERTY.match(line)
                if match:
                    prop = match.group('property')
                    prop = prop.strip()
                    value = int(match.group('value'), 16)
                    arraySize = match.group('arraySize')
                    if arraySize:
                        self.sections[currentSection].append(ArrayProperty(prop, value, arraySize, ))
                    else:
                        self.sections[currentSection].append(ValueProperty(prop, value, ))
                else:
                    match = MEMORY_SECTION.match(line)
                    if match:
                        start = int(match.group('start'), 16)
                        end = int(match.group('end'), 16)
                        attribs = match.group('attribs')
                        r = True if 'R' in attribs else False
                        w = True if 'W' in attribs else False
                        x = True if 'X' in attribs else False
                        self.sections[currentSection].append(MemorySection(start, end, r, w, x, ))
                    else:
                        print "*** NO MATCH [%s] ***" % line
        self._items = {}
        for name, section in self.sections.items():
            if name[0] == mask or name[0] == mcu: #  or (name[0] in 'EIBCommon', 'EEPROMProlog'):
                if len(name) > 1 and name[1] == 'MemoryMap':
                    self.memoryMap = section
                else:
                    print name #, section
                    self._items.update(dict([(item.value, item.name) for item in section]))
    @property
    def interruptVectors(self):
        return self.sections[(self.mcu, 'Vectors')]

    def __str__(self):
        return str(self._items)

    __repr__ = __str__

    def __contains__(self, value):
        return value in self._items and True or False
        #return True if value in self._items else False

    def __getitem__(self, index):
        return self._items[index]

