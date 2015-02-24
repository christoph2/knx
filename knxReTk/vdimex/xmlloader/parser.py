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

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

from xml.sax import make_parser
from xml.sax import ContentHandler
import xml.sax.saxutils as saxutils

camelCaseLower = lambda n : n[0].lower() + n[1 : ]
escape = lambda x: saxutils.unescape(x, {'\n': '&#xA;', '\r': '&#xD;'})
unescape = lambda x: saxutils.unescape(x, {'&#xA;': '\n', '&#xD;': '\r'})

class XMLHandler(ContentHandler):
    def __init__(self):
        self.level = 0
        self.pos = 0
        self.currentElement = None
        self.tags = []
        self.uniqueTags = []
        self.unhandledTags = set()

    def startElement(self, name, attrs):
        attrs = dict(attrs)

        tempAttrs = dict()
        while attrs:
            k, v = attrs.popitem()
            tempAttrs[camelCaseLower(k)] = v
        attrs = tempAttrs

        self.currentElement = attrs

        self.level += 1
        self.tags.append(name)

        callback = "on%sStart" % name
        if hasattr(self, callback):
            getattr(self, callback)(name, attrs)
        else:
            self.unhandledTags.add((self.level, name, ))

        if len(self.uniqueTags) < self.level:
            self.uniqueTags.append(set())
        self.uniqueTags[self.level - 1].add(name)

        self.pos += 1

    def characters(self, ch):
        text = ch.strip()
        if text:
            self.currentElement['textContent'] = text

    def endElement(self, name):
        callback = "on%sEnd" % name
        if hasattr(self, callback):
            getattr(self, callback)(name)
        self.level -= 1
        self.tags.pop()


def parse(data, parserClass):
    handler = parserClass()
    parser = make_parser()
    parser.setContentHandler(handler)
    parser.parse(StringIO.StringIO(data))
    return handler

