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
__version__ = '0.9'


import itertools
import re
import string
import types

IDENTITY_TRANSFORMATION = string.maketrans('', '')

def translator(frm = '', to = '', delete = '', keep = None):
    if isUnicodeString(frm):
        raise TypeError('frm paramater: Unicode not supported.')

    if len(to) == 1:
        to = to * len(frm)
    trans = string.maketrans(frm, to)
    if keep is not None:
        """
        For your applications it might be preferable to ignore delete if keep is specified, or,
        perhaps better, to raise an exception if they are both specified, since it may not make
        much sense to let them both be given in the same call to translator, anyway.
        """
        allchars = string.maketrans('', '')
        delete = allchars.translate(allchars, keep.translate(allchars, delete))
    def translate(s):
        if isUnicodeString(s):
            raise TypeError('Unicode not supported.')
        return s.translate(trans, delete)
    return translate


def containsAny(seq, aset):
    for item in itertools.ifilter(aset.__contains__, seq):
        return True
    return False

def containsOnly(seq, aset):
    """ Check whether sequence seq contains ONLY items in aset. """
    for c in seq:
        if c not in aset:
            return False
    return True

def containsAll(seq, aset):
    """ Check whether sequence seq contains ALL the items in aset. """
    return not set(aset).difference(seq)

"""
#
# Specialized (non-unicode) versions:
#
def containsAny(astr, strset):
    return len(strset) != len(strset.translate(IDENTITY_TRANSFORMATION, astr))

def containsAll(astr, strset):
    return not strset.translate(IDENTITY_TRANSFORMATION, astr)
"""

isUnicodeString = lambda s: isinstance(s, types.UnicodeType)

digitsOnly = translator(keep = string.digits)
noDigits = translator(delete = string.digits)
digitsToHash = translator(frm = string.digits, to = '#')
noVowels = translator(delete = 'aeiuoAEIUO')
noVowelsLower = lambda n: noVowels(n.lower())
noVowelsUpper = lambda n: noVowels(n.upper())


def removeDuplicates(astring):
    prevChar = ''
    result = []
    for ch in astring.strip():
        if ch != prevChar:
            result.append(ch)
        prevChar = ch

    return ''.join(result)

def reformat(text, leftMargin = 1, rightMargin = 80):
    resultLines = []
    for origLine in re.split(r"\n", text):
        line = ' ' * (leftMargin - 1)
        for word in origLine.split():
            if (len(line) + len(word) - leftMargin + 1) <= (rightMargin - leftMargin):
                line += "%s " % word
            else:
                resultLines.append(line.rstrip())
                line = "%s%s " % ((' ' * (leftMargin - 1)) , word)
        resultLines.append(line.rstrip())
    return '\n'.join(resultLines)

