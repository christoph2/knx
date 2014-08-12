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

from knxReTk.utilz.logger import logger


class MemoryExplorer(object):

    def __init__(self, size, offset = 0x0000):
        self.memory = [0] * (size >> 3)
        self.offset = offset
        self.size = size

    def _getBit(self, by, bit):
        return (by & (1 << bit)) >> bit

    def _setBit(self, by, bit, value):
        return by | (value << bit)

    def _getByteAndBit(self, addr):
        addr -= self.offset
        by = addr / 8
        bi = addr % 8
        return (by, bi, )

    def _setExplored(self, addr):
        by, bi = self._getByteAndBit(addr)
        mem = self.memory[by]
        mem = self._setBit(mem, bi, 1)
        self.memory[by] = mem

    def setExplored(self, addr, size):
        for x in range(addr, addr + size):
            self._setExplored(x)

    def isExplored(self, addr):
        by, bi = self._getByteAndBit(addr)
        mem = self.memory[by]
        mem = self._getBit(mem, bi)
        return mem

