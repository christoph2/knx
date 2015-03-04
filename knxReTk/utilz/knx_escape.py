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

import re
import zlib

ESCAPE = re.compile(r'\.[0-9A-F]{2}')
NON_ALNUM = re.compile(r'[^a-z0-1]', re.I)

def escape(value):
    """This section summarizes the naming rules for elements of the KNX XML schema. All these IDs are constructed
    so that they are globally unique. Detailed descriptions are included in the individual element descriptions.
    Note that many IDs of subordinate elements start with the ID of the parent element, then – separated by an
    underscore – additional specification. Often part of the constructed ID is a unique number. How this number
    is to be generated and which unique constraints apply for the given element is described in detail in the
    individual element descriptions. Because IDs can contain only letters, digits, dot, hyphen and underscore
    characters (see XML Namespaces specification, production for NCName), and hyphen and underscore are already
    used as separators, all characters from strings that are not letters or digits have to be escaped: A
    character which is neither a letter nor a digit is represented as a dot, followed by 2 hexadecimal digits
    representing the UTF-8 encoding of the character. Example: a slash (/) is represented as ".2F", a German
    umlaut ä (Unicode code point U+00E4) as ".C3.A4".
    """
    if value.isalnum():
        return value
    else:
        result = []
        for ch in value:
            if not ch.isalnum():
                result.append(".%02X" % ord(ch))
            else:
                result.append(ch)
        return ''.join(result)

"""
def nonAlNumReplacer(match):
    return ".%X" % ord(match.group())

def escape(text):
    return NON_ALNUM.sub(nonAlNumReplacer, text)
"""

def unescaper(match):
    return chr(int(match.group()[1:], 16))

def unescape(value):
    return ESCAPE.sub(unescaper, value)

def masterXML():
    return zlib.decompress(readConfigData('knxReTk', 'knx_master.Z'))
