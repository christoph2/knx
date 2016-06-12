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

from copy import copy

toBoolean = lambda v: True if (v == '1' or v == 'true') else False


class BaseMixin(object):

    result = []

    def convertAttributes(self, attrs):
        for k, v in attrs.items():
            if k.startswith('is') or k.startswith('has') and k != 'hash':
                attrs[k] = toBoolean(v)
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
            self.result.append(self.hardwareEntry)

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


from pprint import pprint

class CatalogMixin(BaseMixin):

    def printit (self):
        print "=" * 60
        pprint(self.result, indent = 3)
        print "=" * 60

    def __init__(self):
        self.catalogLevel = 0
        self.result = {'sections': [], '_id': self.hashValue}
        self.stack = [self.result]
        self.currentSection = None
        self.items = []

    def onManufacturerStart(self, name, attrs):
        self.result.update(attrs)

    def onCatalogSectionStart(self, name, attrs):
        self.catalogLevel += 1
        attrs = self.convertAttributes(attrs)
        self.convert(attrs, 'nonRegRelevantDataVersion', int)

        #print "  " * self.catalogLevel, attrs

        self.newSection = {"sections": [], "items": []}
        self.newSection.update(attrs)
        self.stack.append(self.newSection)
        if self.currentSection:
            self.currentSection['sections'].append(self.newSection)
        else:
            pass
        self.currentSection = self.newSection

    def onCatalogSectionEnd(self, name):
        self.catalogLevel -= 1
        if self.catalogLevel > 0:
            self.stack.pop()
            self.currentSection = self.stack[-1]
            self.items = []
        else:
            self.result['sections'].append(self.currentSection)
            self.currentSection = None

    def onCatalogItemStart(self, name, attrs):
        attrs = self.convertAttributes(attrs)
        self.convert(attrs, 'numbers', int)
        self.convert(attrs, 'nonRegRelevantDataVersion', int)
        self.currentSection["items"].append(attrs)

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


class ApplicationMixin(BaseMixin):

    def __init__(self):
        self.manufacturers = {}
        self.currentManufacturer = None
        self.currentSegment = None
        self.currentApplication = None
        self.currentParameterType = None
        self.currentParameterRefContainer = []
        self.currentFixup = None
        self.result = self.manufacturers

    def onManufacturerStart(self, name, attrs):
        if attrs['refId'] not in self.manufacturers:
            self.currentManufacturer = {'_id': attrs['refId'], 'applicationPrograms': []}
            self.manufacturers[attrs['refId']] = self.currentManufacturer
        else:
            if not self.currentManufacturer:
                self.currentManufacturer = self.manufacturers[attrs['refId']]

    def onApplicationProgramStart(self, name, attrs):
        attrs = self.convertAttributes(attrs)

        self.convert(attrs, 'applicationVersion', int)
        self.convert(attrs, 'applicationNumber', int)
        self.convert(attrs, 'peiType', int)
        self.convert(attrs, 'additionalAddressesCount', int)
        self.convert(attrs, 'nonRegRelevantDataVersion', int)
        #self.convert(attrs, '', int)
        self.convert(attrs, 'dynamicTableManagement', toBoolean)
        self.convert(attrs, 'linkable', toBoolean)
        self.convert(attrs, 'preEts4Style', toBoolean)
        self.convert(attrs, 'convertedFromPreEts4Data', toBoolean)
        self.convert(attrs, 'downloadInfoIncomplete', toBoolean)
        self.convert(attrs, 'createdFromLegacySchemaVersion', toBoolean)
        self.convert(attrs, 'broken', toBoolean)
        attrs['static'] = {'code': {"segments": []}, 'parameterTypes': [], 'parameters': [], 'parameterRefs': [],
            'loadProcedures': [],"options": None, 'fixups': [], 'addressTable': {}, 'associationTable': {},
            'extensions': [], 'comObjectTable': {'comObjects': []}, 'comObjectRefs': []
        }
        attrs['dynamic'] = {'channels': []}
        self.currentApplication = attrs
        self.currentManufacturer['applicationPrograms'].append(attrs)

    def onOptionsStart(self, name, attrs):
        attrs = self.convertAttributes(attrs)
        self.convert(attrs, 'preferPartialDownloadIfApplicationLoaded', toBoolean)
        self.convert(attrs, 'easyCtrlModeModeStyleEmptyGroupComTables', toBoolean)
        self.convert(attrs, 'setObjectTableLengthAlwaysToOne', toBoolean)
        self.convert(attrs, 'textParameterZeroTerminate', toBoolean)
        self.convert(attrs, 'legacyNoPartialDownload', toBoolean)
        self.convert(attrs, 'legacyNoMemoryVerifyMode', toBoolean)
        self.convert(attrs, 'legacyNoOptimisticWrite', toBoolean)
        self.convert(attrs, 'comparable', toBoolean)
        self.convert(attrs, 'reconstructable', toBoolean)
        self.convert(attrs, 'legacyDoNotReportPropertyWriteErrors', toBoolean)
        self.convert(attrs, 'legacyNoBackgroundDownload', toBoolean)
        self.convert(attrs, 'legacyDoNotCheckManufacturerId', toBoolean)
        self.convert(attrs, 'legacyAlwaysReloadAppIfCoVisibilityChanged', toBoolean)
        self.convert(attrs, 'legacyNeverReloadAppIfCoVisibilityChanged', toBoolean)
        self.convert(attrs, 'legacyDoNotSupportUndoDelete', toBoolean)
        self.convert(attrs, 'legacyAllowPartialDownloadIfAp2Mismatch', toBoolean)
        self.convert(attrs, 'legacyKeepObjectTableGaps', toBoolean)
        self.convert(attrs, 'partialDownloadOnlyVisibleParameters', toBoolean)
        self.convert(attrs, 'legacyProxyCommunicationObjects', toBoolean)
        self.convert(attrs, 'deviceInfoIgnoreRunState', toBoolean)
        self.convert(attrs, 'deviceInfoIgnoreLoadedState', toBoolean)
        self.convert(attrs, 'deviceCompareAllowCompatibleManufacturerId', toBoolean)
        self.convert(attrs, 'lineCoupler0912NewProgrammingStyle', toBoolean)
        self.currentApplication['static']['options'] = attrs

    def onAddressTableStart(self, name, attrs):
        attrs = self.convertAttributes(attrs)
        self.convert(attrs, 'offset', int)
        self.convert(attrs, 'maxEntries', int)
        self.currentApplication['static']['addressTable'] = attrs

    def onAssociationTableStart(self, name, attrs):
        attrs = self.convertAttributes(attrs)
        self.convert(attrs, 'offset', int)
        self.convert(attrs, 'maxEntries', int)
        self.currentApplication['static']['associationTable'] = attrs

    def onExtensionStart(self, name, attrs):
        attrs = self.convertAttributes(attrs)
        self.convert(attrs, 'requiresExternalSoftware', toBoolean)
        attrs['baggages'] = []
        self.currentExtension = attrs
        self.currentApplication['static']['extensions'].append(attrs)

    def onBaggageStart(self, name, attrs):
        attrs = self.convertAttributes(attrs)
        self.currentExtension['baggages'].append(attrs)

    def onFixupStart(self, name, attrs):
        attrs = self.convertAttributes(attrs)
        attrs['offsets'] = []
        self.currentFixup = attrs
        self.currentApplication['static']['fixups'].append(self.currentFixup)

    def onOffsetEnd(self, name):
        self.currentFixup['offsets'].append(int(self.textContent))

    def onAbsoluteSegmentStart(self, name, attrs):
        attrs = self.convertAttributes(attrs)
        self.convert(attrs, 'address', int)
        self.convert(attrs, 'size', int)
        self.convert(attrs, 'userMemory', toBoolean)
        attrs['data'] = None
        attrs['mask'] = None
        attrs['type'] = "absolute"
        self.currentSegment = attrs
        self.currentApplication['static']['code']["segments"].append(attrs)

    def onRelativeSegmentStart(self, name, attrs):
        attrs = self.convertAttributes(attrs)
        self.convert(attrs, 'offset', int)
        self.convert(attrs, 'size', int)
        self.convert(attrs, 'loadStateMachine', int)
        attrs['type'] = "relative"
        #attrs['data'] = None
        #attrs['mask'] = None
        self.currentSegment = attrs
        self.currentApplication['static']['code']["segments"].append(attrs)

    def onDataEnd(self, name):
        self.currentSegment['data'] = self.textContent

    def onMaskEnd(self, name):
        self.currentSegment['mask'] = self.textContent

    def onComObjectTableStart(self, name, attrs):
        attrs = self.convertAttributes(attrs)
        self.convert(attrs, 'offset', int)
        self.currentApplication['static']['comObjectTable'].update(attrs)

    def onComObjectStart(self, name, attrs):
        attrs = self.convertAttributes(attrs)
        self.convert(attrs, 'number', int)
        self.currentApplication['static']['comObjectTable']['comObjects'].append(attrs)

    def onParameterTypeStart(self, name, attrs):
        attrs = self.convertAttributes(attrs)
        self.currentParameterType = attrs
        self.currentApplication['static']['parameterTypes'].append(attrs)

    def onTypeNumberStart(self, name, attrs):
        attrs = self.convertAttributes(attrs)
        self.convert(attrs, 'sizeInBit', int)
        self.convert(attrs, 'minInclusive', int)
        self.convert(attrs, 'maxInclusive', int)
        self.currentParameterType['type'] = "number"
        self.currentParameterType.update(attrs)

    def onTypeTextStart(self, name, attrs):
        attrs = self.convertAttributes(attrs)
        self.convert(attrs, 'sizeInBit', int)
        self.currentParameterType['type'] = "text"
        self.currentParameterType.update(attrs)

    def onTypeNoneStart(self, name, attrs):
        self.currentParameterType['type'] = None

    def onTypeRestrictionStart(self, name, attrs):
        attrs = self.convertAttributes(attrs)
        self.convert(attrs, 'sizeInBit', int)
        attrs['values'] = []
        self.currentParameterType['type'] = "enumeration"   # ???
        self.currentParameterType['restriction'] = attrs

    def onEnumerationStart(self, name, attrs):
        attrs = self.convertAttributes(attrs)
        self.convert(attrs, 'displayOrder', int)
        self.convert(attrs, 'value', int)
        self.currentParameterType['restriction']['values'].append(attrs)

    def addLoadControl(self, attrs, type_, converter = None):
        if converter is None:
            converter = {}
        attrs = self.convertAttributes(attrs)
        for k, v in converter.items():
            self.convert(attrs, k, v)
        attrs['type'] = type_
        self.currentApplication['static']['loadProcedures'].append(attrs)

    def onLdCtrlConnectStart(self, name, attrs):
        self.addLoadControl(attrs, 'connect')

    def onLdCtrlUnloadStart(self, name, attrs):
        self.addLoadControl(attrs, 'unload', {'lsmIdx': int})

    def onLdCtrlLoadStart(self, name, attrs):
        self.addLoadControl(attrs, 'load', {'lsmIdx': int})

    def onLdCtrlAbsSegmentStart(self, name, attrs):
        self.addLoadControl(attrs, 'absSegment', {
            'lsmIdx': int, 'segType': int, 'address': int, 'size': int, 'access': int, 'memType': int, 'segFlags': int}
        )

    def onLdCtrlTaskSegmentStart(self, name, attrs):
        self.addLoadControl(attrs, 'taskSegment', {'lsmIdx': int, 'address': int})

    def onLdCtrlLoadCompletedStart(self, name, attrs):
        self.addLoadControl(attrs, 'loadCompleted', {'lsmIdx': int})

    def onLdCtrlRestartStart(self, name, attrs):
        self.addLoadControl(attrs, 'restart')

    def onLdCtrlDisconnectStart(self, name, attrs):
        self.addLoadControl(attrs, 'disconnect')

    def onLdCtrlComparePropStart(self, name, attrs):
        self.addLoadControl(attrs, 'compareProp', {"objIdx": int, "propId": int})

    def onLdCtrlTaskPtrStart(self, name, attrs):
        self.addLoadControl(attrs, 'taskPtr', {'lsmIdx': int, 'initPtr': int, 'savePtr': int, 'serialPtr': int})

    def onLdCtrlTaskCtrl2Start(self, name, attrs):
        self.addLoadControl(attrs, 'taskCtrl2', {'lsmIdx': int, 'callback': int, 'address': int, 'seg0': int, 'seg1': int})

    def onLdCtrlTaskCtrl1Start(self, name, attrs):
        self.addLoadControl(attrs, 'taskCtrl1', {'lsmIdx': int, 'address': int, 'count': int})

    def onLdCtrlDelayStart(self, name, attrs):
        self.addLoadControl(attrs, 'delay', {'milliSeconds': int})

    def onLdCtrlSetControlVariableStart(self, name, attrs):
        self.addLoadControl(attrs, 'setControlVariable', {'value': bool})

    def onLdCtrlLoadImagePropStart(self, name, attrs):
        self.addLoadControl(attrs, 'loadImageProp', {'objIdx': int, 'objType': int, 'occurence': int,
            'propId': int, 'count': int, 'startElement': int,}
        )

    def onLdCtrlRelSegmentStart(self, name, attrs):
        self.addLoadControl(attrs, 'relSegment', {'lsmIdx': int, 'objType': int, 'occurence': int,
            'size': int, 'mode': int, 'fill': int }
        )

    def onLdCtrlWriteMemStart(self, name, attrs):
        self.addLoadControl(attrs, 'writeMem', {'address': int, 'size': int, 'verify': bool, })

    def onLdCtrlWritePropStart(self, name, attrs):
        self.addLoadControl(attrs, 'writeProp', {'objIdx': int, 'objType': int, 'occurence': int,
            'propId': int, 'startElement': int}
        )

    def onLdCtrlWriteRelMemStart(self, name, attrs):
        self.addLoadControl(attrs, 'writeRelMem', {'objIdx': int, 'offset': int, 'size': int,
            'verify': bool})

    def onParameterStart(self, name, attrs):
        attrs = self.convertAttributes(attrs)
        self.currentApplication['static']['parameters'].append(attrs)

    def onParameterRefStart(self, name, attrs):
        attrs = self.convertAttributes(attrs)
        self.convert(attrs, 'displayOrder', int)
        self.currentApplication['static']['parameterRefs'].append(attrs)

    def onComObjectRefStart(self, name, attrs):
        attrs = self.convertAttributes(attrs)
        self.currentApplication['static']['comObjectRefs'].append(attrs)

    def onChannelStart(self, name, attrs):
        attrs = self.convertAttributes(attrs)
        self.convert(attrs, 'number', int)
        #print "Channel:", attrs
        #self.currentParameterRefContainer.append(attrs)
        self.currentApplication['dynamic']['channels'].append(copy(attrs))

    def onChannelEnd(self, name):
        pass
        #self.currentParameterRefContainer.pop()

    #def onParameterBlockStart(self, name, attrs):
    #    attrs = self.convertAttributes(attrs)

