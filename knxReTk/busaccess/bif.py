#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = """
    KONNEX/EIB-Protocol-Stack.

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

import abc


class BIF(object):
    """Businterface Interface.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, **kws):
        for k, v in kws.items():
            setattr(self, k, v)
        self.connected = False

    def __del__(self):
        if self.connected:
            self.disconnect()

    @abc.abstractmethod
    def connect(self):
        pass

    @abc.abstractmethod
    def disconnect(self):
        pass

    abc.abstractmethod
    def write(self, request):
        pass

    @abc.abstractmethod
    def read(self, count):
        pass

    @abc.abstractproperty
    def closed(self):
        pass

