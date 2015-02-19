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


class BaseMixin(object):

    def convertAttributes(self, attrs):
        for k, v in attrs.items():
            if k.startswith('is') or k.startswith('has') and k != 'hash':
                attrs[k] = True if v == '1' else False
        if 'id' in attrs:
            _id = attrs.pop('id')
            attrs['_id'] = _id  # Make identifier usable by MongoDB.
        return attrs

    def convert(self, dict_, key, type_):
        if key in dict_:
            dict_[key] = type_(dict_[key])


class HardwareMixin(BaseMixin):
    """Process 'hardware.xml' files.
    """

    hardwareList = []

    def onHardwareStart(self, name, attrs):
        if attrs:
            attrs = self.convertAttributes(attrs)
            self.convert(attrs, 'busCurrent', float)
            self.convert(attrs, 'VersionNumber', int)
            self.convert(attrs, 'nonRegRelevantDataVersion', int)
            attrs['products'] = []
            attrs['hardware2Programs'] = []
            self.hardwareEntry = attrs

    def onHardwareEnd(self, name):
        if self.level == 5:
            self.hardwareList.append(self.hardwareEntry)

    def onProductStart(self, name, attrs):
        attrs = self.convertAttributes(attrs)
        self.convert(attrs, 'widthInMillimeter', float)
        self.convert(attrs, 'nonRegRelevantDataVersion', int)

        self.product = attrs
        self.hardwareEntry['products'].append(self.product)

    def onHardware2ProgramStart(self, name, attrs):
        attrs = self.convertAttributes(attrs)
        self.hardware2Program = attrs
        self.hardwareEntry['hardware2Programs'].append(self.hardware2Program)

    def onApplicationProgramRefStart(self, name, attrs):
        if len(attrs) != 1:
            raise TypeError("onApplicationProgramRefStart")
        else:
            self.hardware2Program['applicationProgramRef']= attrs['refId']

    def onRegistrationInfoStart(self, name, attrs):
        if hasattr(self, 'hardware2Program'):
            self.hardware2Program['RegistrationInfo'] = attrs
        else:
            pass
            #print "*** NO hardware2Program!!!",
            #print " " * self.level, "<", self.level, self.tags[-1], attrs


class LanguageMixin(BaseMixin):
    """Process translation entries.
    """

    languageIdentifier = None
    translationUnit = None
    translationElement = None
    translationList = []
    translations = dict()

    def onLanguageStart(self, name, attrs):
        attrs = self.convertAttributes(attrs)
        self.languageIdentifier = attrs['identifier']

    def onLanguageEnd(self, name):
        pass

    def onTranslationUnitStart(self, name, attrs):
        self.translationUnit = attrs['refId']

    def onTranslationElementStart(self, name, attrs):
        self.translationElement = attrs['refId']

    def onTranslationStart(self, name, attrs):
        self.translations.setdefault(self.translationUnit, {})
        self.translations[self.translationUnit].setdefault(self.translationElement, {})
        self.translations[self.translationUnit][self.translationElement].setdefault(self.languageIdentifier, []).append(attrs)

