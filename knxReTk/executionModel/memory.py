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

import array

from knxReTk.utilz.logger import logger


class ProtectionPolicy(object):

    def check(self, address):
        return True


class Memory(object):
    BIG_ENDIAN = 0
    LITTLE_ENDIAN = 1

    def __init__(self, fp, protectionPolicy = None):
        self._image = array.array('B', fp.read())
        if not protectionPolicy:
            self._protectionPolicy = ProtectionPolicy()

    def createGetter(self, byteSize, endianess):
        def getB(addr):
            res = 0
            for idx in range(byteSize):
                res *= 0x100
                res += self._image[addr + idx]
            return res

        def getL(addr):
            res = 0
            for idx in range(byteSize - 1, -1, -1):
                res *= 0x100
                res += self._image[addr + idx]
            return res

        if endianess == Memory.BIG_ENDIAN:
            return getB
        elif endianess == Memory.LITTLE_ENDIAN:
            return getL
        else:
            raise ValueError("Invalid endianess '%s'." % endianess)

    def getBlob(self, addr, size):
        return self._image[addr : addr + size]

    def __len__(self):
        return len(self._image)


class ReadOnlyMemory(Memory):
    pass


class ReadWriteMemory(Memory):

    def createSetter(self, byteSize, endianess):
        def setB(addr, value):
            for idx in range(byteSize - 1, - 1, -1):
                temp = value & 0xff
                #print hex(temp), idx
                value >>= 8
                self._image[addr + idx] = temp

        def setL(addr, value):
            res = 0
            for idx in range(byteSize):
                temp = value & 0xff
                #print hex(temp), idx
                value >>= 8
                self._image[addr + idx] = temp

        if endianess == Memory.BIG_ENDIAN:
            return setB
        elif endianess == Memory.LITTLE_ENDIAN:
            return setL
        else:
            raise ValueError("Invalid endianess '%s'." % endianess)


##
##fin = file(r"C:\projekte\csProjects\pyKNX\bcu20.bin", "rb")
##
##mem = ReadWriteMemory(fin)
##
##setB = mem.createSetter(4, mem.BIG_ENDIAN)
##getB = mem.createGetter(4, mem.BIG_ENDIAN)
##setB(0x26, 0x11223344)
##print "0x%08X" % getB(0x26)
##
##setL = mem.createSetter(4, mem.LITTLE_ENDIAN)
##getL = mem.createGetter(4, mem.LITTLE_ENDIAN)
##setL(0x26, 0x11223344)
##print "0x%08X" % getL(0x26)
##


