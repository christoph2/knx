#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = """
   Konnex / EIB Reverserz Toolkit

   (C) 2001-2015 by Christoph Schueler <cpu12.gems@googlemail.com>

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

#from collections import namedtuple, OrderedDict
#import Queue
#import sys
import threading

class Thread(threading.Thread):

    registry = []

    def __init__(self):
        super(Thread, self).__init__()
        self.quitEvent = threading.Event()
        self.register(self)

    def register(self, thread):
        Thread.registry.append(thread)

    def quit(self):
        self.quitEvent.set()
        self.join()

    @classmethod
    def quitAll(self):
        for thread in Thread.registry:
            thread.quit()

    def getName(self):
        return "%s-%u" % (self.__class__.__name__, self.ident)

    def run(self):
        print "Starting {0} thread.".format(self.getName())
        while True:
            signal = self.quitEvent.wait(timeout = 0.01)
            if signal == True:
                break
            self.execute()
        print "Exiting {0} thread.".format(self.getName())

    def execute(self):
        raise NotImplementedError("'execute()' method needs to be overriden.")

