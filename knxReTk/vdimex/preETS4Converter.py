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

from collections import OrderedDict, namedtuple
from copy import copy
import hashlib
import itertools
from pprint import pprint
import re
import sys

import pymongo as mongo
import bson
from bson.objectid import ObjectId

from knxReTk.utilz import knx_escape
from knxReTk.utilz.locales import getLocalCode
from knxReTk.utilz.classes import SingletonBase
#from knxReTk.utilz.profilehooks import profile


Link = namedtuple('Link', 'type, order, target, collection, key, foreignKey')
LinkM = namedtuple('Link', 'type, order, target, collection, key, foreignKey, secondaryKey')


def mapAttributes(attrs, map):
    result = {}
    for k, v in attrs.items():
        if k in map:
            result[map[k]] = v
        else:
            result[k] = v
    return result


class RepresentationMixIn(object):

    def __repr__(self):
        keys = [k for k in self.__dict__ if not (k.startswith('__') and k.endswith('__'))]
        result = []
        result.append("%s {" % self.__class__.__name__)
        for key in keys:
            line = "    %s = '%s'" % (key, getattr(self, key))
            result.append(line)
        result.append("}")
        return '\n'.join(result)


class LinkToOne(RepresentationMixIn):
    def __init__(self, order, tableName, key, foreignKey):
        self.order = order
        self.tableName = tableName
        self.key = key
        self.foreignKey = foreignKey


class LinkToMany(RepresentationMixIn):
    def __init__(self, order, tableName, key, foreignKey, secondaryKey):
        self.order = order
        self.tableName = tableName
        self.key = key
        self.foreignKey = foreignKey
        self.secondaryKey = secondaryKey


class SubObject(RepresentationMixIn):
    pass


class TableInformation(SingletonBase):

    def __init__(self, db):
        self.db = db
        if not hasattr(TableInformation, 'tableMeta'):
            self._setMetaData()

    def _setMetaData(self):
        TableInformation.tableMeta = {}
        TableInformation.stringColumns = {}
        meta = self.db.meta.find_one({})
        for table in meta['tables']:
            tcolumns = {}
            for column in table['columns']:
                number = column.pop('number')
                if column['type'] == 'varchar' and not column['name'] in ('functional_entity_numb', ):
                    TableInformation.stringColumns.setdefault(table['_id'], []).append(column['name'])
                tcolumns[number] = column
            TableInformation.tableMeta[table['_id']] = {'columns': tcolumns}

    def getColumnNameByNumber(self, collection, columnNumber):
        result = self.getColumnByNumber(collection, columnNumber).get('name', '')
        if not result:
            result = TableInformation.stringColumns[collection][columnNumber % 10]
        return result

    def getColumnByNumber(self, collection, columnNumber):
        return self.tableMeta[collection]['columns'].get(columnNumber, {})

class TableType(type):
    ColumnCache = {}

    def __new__(klass, name, bases, namespace):
        newClass = super(TableType, klass).__new__(klass, name, bases, namespace)
        newClass.links = []
        for k, v in namespace.items():
            if isinstance(v, LinkToOne):
                newClass.links.append(Link(LinkToOne, v.order, k, v.tableName, v.key, v.foreignKey))
                #setattr(newClass, k, SubObject())
            elif isinstance(v, LinkToMany):
                newClass.links.append(LinkM(LinkToMany, v.order, k, v.tableName, v.key, v.foreignKey, v.secondaryKey))
                #setattr(newClass, k, [])
        return newClass

    def setColumnNames(klass, collection, translations):
        result = []
        for translation in translations:
            translation['column_name'] = klass.tableMeta.getColumnNameByNumber(collection, translation['column_id'])
            result.append(translation)
        return result

    #@profile
    def fetchOne(klass, collection, key, value):
        record = klass.db[collection].find_one({key: value})
        if not record:
            return {}
        translations = list(klass.db['text_attribute'].find({'entity_id': value}))
        translationDict = {}
        for g, v in itertools.groupby(sorted(translations, key = lambda x: str(x['language_id']) + str(x['column_id'])), lambda x: x['language_id']):
            translationDict[g] = klass.setColumnNames(collection, list(v))
        record['translations'] = translationDict
        return record

    def fetchMany(klass, collection, key, value, secondaryKey):
        records = klass.db[collection].find({key: value})
        result = []
        for record in records:
            #print record
            translations = list(klass.db['text_attribute'].find({'entity_id': record[secondaryKey]}))
            if translations:
                pass
            result.append(record)
                #print translations
        return result


class Table(RepresentationMixIn):
    __metaclass__ = TableType
    cache = {}

    def __new__(klass, key):
        newObj = super(Table, klass).__new__(klass)
        if key in klass.cache:
            return klass.cache[key]
        return newObj

    #@profile
    def __init__(self, key):
        self.key = key

        self.tableMeta = TableInformation(self.db)

        for k, v in Table.fetchOne(self.collection, self.keyColumn, self.key).items():
            setattr(self, k, v)
        self.links.sort(key = lambda o: o.order)
        for link in self.links:
            if link.type is LinkToOne:
                setattr(self, link.target, SubObject())
            elif link.type is LinkToMany:
                setattr(self, link.target, [])
            target = getattr(self, link.target)
            if '.' in link.foreignKey:
                objName, attrName = link.foreignKey.split('.')
                obj = getattr(self, objName)
                if link.type is LinkToMany:
                    print
                objValue = getattr(obj, attrName)
            else:
                objValue = getattr(self, link.foreignKey)
            fetcher = Table.fetchOne if link.type == LinkToOne else Table.fetchMany
            if link.type is LinkToOne:
                result = fetcher(link.collection, link.key, objValue)
                for k, v in result.items():
                    setattr(target, k, v)
            elif link.type is LinkToMany:
                result = fetcher(link.collection, link.key, objValue, link.secondaryKey)
                setattr(self, link.target, result)
        Table.cache[key] = self


class NameMapper(object):

    def __init__(self, attrs):
        for k, v in attrs.items():
            setattr(self, k, v)
        self.attribute_map_inverse = dict([(v, k) for k, v in self.attribute_map.items()])

    def __getattr__(self, attr):
        if attr in self.attribute_map:
            return getattr(self, self.attribute_map[attr])
        else:
            raise AttributeError("%s" % attr)


class Application(Table):
    collection = 'application_program'
    keyColumn = 'program_id'

    parameterTypes = LinkToMany(10, 'parameter_type', 'program_id', 'program_id', 'parameter_type_id')
    parameters = LinkToMany(20, 'parameter', 'program_id', 'program_id', 'parameter_id')
    #parameterListOfValues = LinkToMany(30, 'parameter_list_of_values', 'parameter_type_id', 'parameterTypes.parameter_type_id', 'parameter_value_id')

    @property
    def applicationId(self):
        appId = "M-%04X_A-%X-%X" % (self.manufacturer_id, self.device_type, int(self.program_version))
        appId = "%s-%s" % (appId, hashlib.sha1(appId).hexdigest()[-4 : ].upper())
        return appId


class Device(Table):
    collection = 'virtual_device'
    keyColumn = 'virtual_device_id'

    catalogEntry = LinkToOne(10, 'catalog_entry', 'catalog_entry_id', 'catalog_entry_id')
    hardwareProduct = LinkToOne(20, 'hw_product', 'product_id', 'catalogEntry.product_id')
    application = LinkToOne(30, 'application_program', 'program_id', 'program_id')

    @property
    def hardwareId(self):
        hardwareId = "M-%04X_H-%s-%X" % (self.catalogEntry.manufacturer_id,
            (knx_escape.escape(self.hardwareProduct.product_serial_number)),
            self.virtual_device_number, # product_version_number???
        )
        if self.hardwareProduct.original_manufacturer_id:
            hardwareId = "%s-O%04X" % (hardwareId, self.hardwareProduct.original_manufacturer_id)
        return hardwareId

    @property
    def hardwareProductId(self):
        try:
            hardwareProductId = "%s_HP-%04X-%02X"% (self.hardwareId, self.application.device_type, int(self.application.program_version),)
            hardwareProductId = "%s-%s" % (hardwareProductId, hashlib.sha1(hardwareProductId).hexdigest()[-4 : ].upper())
        except AttributeError as e:
            # In this case no 'application_program' exists!
            if self.hardwareProduct.original_manufacturer_id:
                hardwareProductId = "%s_O%04u_HP" % (self.hardwareId, int(self.hardwareProduct.original_manufacturer_id), )
            else:
                hardwareProductId = "%s_HP" % (self.hardwareId, )
        return hardwareProductId

    @property
    def catalogItemId(self):
        catalogItemId = "%s_CI-%s-%u" % (self.hardwareProductId, knx_escape.escape(self.catalogEntry.order_number),
            self.hardwareProduct.product_version_number)
        return catalogItemId

    @property
    def productId(self):
        productId = "%s_P-%s" % (self.hardwareId, knx_escape.escape(self.catalogEntry.order_number), )
        return productId


class CatalogSectionMapper(NameMapper):
    _identifier = None

    attribute_map = {
        'Name': 'functional_entity_name' ,
        'Number':'functional_entity_numb',
        'VisibleDescription': 'functional_entity_description',
        'Id': 'identifier'
    }

    def __init__(self, attrs, numbers):
        super(CatalogSectionMapper, self).__init__(attrs)
        self._identifier = "M-%04u_CS-%s" % (self.manufacturer_id, '-'.join(numbers + [self.Number]))

    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, value):
        self._identifier = value


class CatalogItemMapper(NameMapper):

    attribute_map = {
        'Name': 'virtual_device_name' ,
        'Number': 'virtual_device_number',
        'VisibleDescription': 'virtual_device_description',
        'ProductRefId': 'productId',
        'Hardware2ProgramRefId': 'hardwareProductId',
        'Id': 'catalogItemId'
    }

    def __init__(self, attrs):
        super(CatalogItemMapper, self).__init__(attrs)


class CatalogSection(Table):

    collection = 'functional_entity'
    keyColumn = 'fun_functional_entity_id'


class GenericBuilder(object):

    def __init__(self, conn, dbName):
        self.conn = conn
        self.db = conn[dbName]
        Table.tableMeta = TableInformation(self.db)

    def getTranslations(self, collection, entityId, mapper = None):
        resultList = []
        translations = list(self.db.text_attribute.find({'entity_id': entityId}, ).sort([('language_id', 1), ('column_id', 1)]))
        for translation in translations:
            columnName = self.tableMeta.getColumnNameByNumber(collection, translation['column_id'])
            if mapper:
                tcn = mapper.attribute_map_inverse.get(columnName)
                if tcn:
                    columnName = tcn
            if translation['text_attribute_text']:
                resultList.append({"AttributeName": columnName, "Text": translation['text_attribute_text'],
                    'Language': getLocalCode(translation['language_id'])
                    })
        result = {}
        for group, items in itertools.groupby(resultList, lambda e: e['Language']):
            titems = []
            for item in items:
                item.pop('Language')
                titems.append(item)
            result[group] = titems
        return result

class CatalogBuilder(GenericBuilder):

    def __init__(self, conn, dbName):
        super(CatalogBuilder, self).__init__(conn, dbName)
        self.languages = list(self.db.ete_language.find())
        self.devices = {}
        Table.db = self.db
        self.createIndices()

    def createIndices(self):
        self.db.catalog_entry.create_index('catalog_entry_id', mongo.ASCENDING)
        self.db.catalog_entry.create_index('product_id', mongo.ASCENDING)
        self.db.hw_product.create_index('product_id', mongo.ASCENDING)
        self.db.application_program.create_index('program_id', mongo.ASCENDING)
        self.db.functional_entity.create_index('functional_entity_id', mongo.ASCENDING)
        self.db.functional_entity.create_index('fun_functional_entity_id', mongo.ASCENDING)
        self.db.text_attribute.create_index('entity_id', mongo.ASCENDING)   # Really important for performance!
        self.db.application_program.create_index('program_id')
        self.db.parameter.create_index('parameter_id', mongo.ASCENDING)
        self.db.parameter.create_index('program_id', mongo.ASCENDING)
        self.db.parameter_type.create_index('parameter_type_id', mongo.ASCENDING)
        self.db.parameter_type.create_index('parameter_id', mongo.ASCENDING)
        self.db.parameter_list_of_values.create_index('parameter_type_id' , mongo.ASCENDING)
        self.db.parameter_list_of_values.create_index('parameter_value_id' , mongo.ASCENDING)

    def run(self):
        print "creating 'catalog' ",
        self.hashValue = hashlib.sha1(self.db.name).hexdigest()
        resultDict = {'_id': self.hashValue, 'refId': 'M-', 'sections': []}
        self.getCatalogSections(None, None, resultDict = resultDict)
        meta = self.db.meta.find_one()
        _id = meta['_id']
        resultDict['_id'] = _id
        resultDict['defaultLanguage'] = meta['defaultLanguage']
        self.db.catalog.update({"_id": _id}, resultDict, upsert = True, safe = True)
        print
        print "done."
        return resultDict

    def getCatalogSections(self, obj, key, numbers = [],level = 0, resultDict = {}):
        result = self.db.functional_entity.find({"fun_functional_entity_id": key}).sort([("functional_entity_id", mongo.ASCENDING,), ])
        level += 1
        sys.stdout.write('.')
        sections = []
        for entry in result:
            am = CatalogSectionMapper(entry, numbers)
            numbers.append(am.Number)

            translations = self.getTranslations('functional_entity', am.functional_entity_id, am)
            section = {'name': am.Name, 'items': [], 'visibleDescription': am.VisibleDescription or '', '_id': am.Id, 'sections': [],
                'number': am.Number, 'translations': translations
            }

            for item in self.db.virtual_device.find({"functional_entity_id": entry['functional_entity_id']}, {'virtual_device_id': 1, '_id': 0}).sort([('catalog_entry_id', 1)]):
                im = CatalogItemMapper(item)

                translations = self.getTranslations('virtual_device', item['virtual_device_id'], im)
                vd = Device(item['virtual_device_id'])
                self.devices[vd.productId] = vd
                section['items'].append({"Id": vd.catalogItemId, "Name": vd.virtual_device_name, "Number": vd.virtual_device_number,
                    "VisibleDescription": vd.virtual_device_description or '', "ProductRefId": vd.productId,
                    "Hardware2ProgramRefId": vd.hardwareProductId, 'translations': translations
                })
            sections.append(section)
            self.getCatalogSections(entry, entry['functional_entity_id'], numbers, level, section)
        resultDict['sections'] = sections
        if numbers:
            numbers.pop()
        level -= 1

    def getHardware(self, devices):
        print """<?xml version="1.0" encoding="utf-8"?>
<KNX xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" CreatedBy="knxconv" ToolVersion="4.0.1837.35879" xmlns="http://knx.org/xml/project/11">
  <ManufacturerData>
    <Manufacturer RefId="M-0002">
      <Hardware>"""
        for dev in sorted(devices.values(), key = lambda x: x.catalog_entry_id): # virtual_device_id
            print '         <Hardware Id="%s" Name="%s" SerialNumber="%s" VersionNumber="%s" BusCurrent="%s" HasIndividualAddress="true" HasApplicationProgram="%s" NoDownloadWithoutPlugin="true"' % (dev.hardwareId, dev.hardwareProduct.product_name, dev.hardwareProduct.product_serial_number, dev.hardwareProduct.product_version_number, dev.hardwareProduct.bus_current, "true" if dev.program_id else "*false")
            products = list(self.db.catalog_entry.find({"product_id": dev.catalogEntry.product_id}, sort = [("catalog_entry_id", mongo.ASCENDING)]))
            if products:
                print "            <Products>"
            for product in products:
                description = self.db.product_description.find_one({"catalog_entry_id": product['catalog_entry_id']})   # je Sprache!?
                productId = "%s2_P-%s" % (dev.hardwareId, knx_escape.escape(product['order_number']))
                if description:
                    print '               <Product Id="%s" Text="%s" OrderNumber="%s" IsRailMounted="%s"  WidthInMillimeter="%s" VisibleDescription="%s" DefaultLanguage="en-US" Hash="">' % (productId, product['entry_name'], product['order_number'], "true" if product['din_flag'] else "false", product['entry_width_in_millimeters'], description['product_description_text'])
                else:
                    print '               <Product Id="%s" Text="%s" OrderNumber="%s" IsRailMounted="%s"  WidthInMillimeter="%s" DefaultLanguage="en-US" Hash="">' % (productId, product['entry_name'], product['order_number'], "true" if product['din_flag'] else "false", product['entry_width_in_millimeters'],)
                print "               </Product>"
            if products:
                print "            </Products>"
            prodProg = list(self.db.product_to_program.find({"product_id": dev.hardwareProduct.product_id}))
            for p2p in prodProg:
                dt = self.db.application_program.find_one({'program_id': p2p['program_id']}, {'device_type': 1, 'program_version': 1, '_id': 0})
                if dt:
                    deviceType = dt['device_type']
                    programVersion = dt['program_version']
                    programNumber = "M-%04X_H-%s-%u_HP-%04X-%02X" % (product['manufacturer_id'], knx_escape.escape(dev.hardwareProduct.product_serial_number), dev.hardwareProduct.product_version_number, deviceType, int(programVersion))
                    programNumber = "%s-%s" % (programNumber, hashlib.sha1(programNumber).hexdigest()[-4 : ].upper())
                    print '<Hardware2Program %s />' % (programNumber)
                if p2p['registration_year']:
                    year = p2p['registration_year']
                    if year < 1900:
                        year += 1900
                    if p2p['prod2prog_status_code'] in (10, 20):
                        print "        *** Reg-Number: %u/%u" % (year, p2p['registration_number'])

        print """         </Hardware>
      </Manufacturer>
  </ManufacturerData>
</KNX>"""

def convert(filename):
    conn = mongo.Connection()
    cb = CatalogBuilder(conn, filename)
    cb.run()
    #cb.getHardware(cb.devices)

#convert('n562_11_vd5')
#sys.exit()

class ApplicationBuilder(GenericBuilder):

    def __init__(self, dbName):
        super(ApplicationBuilder, self).__init__(dbName)
        self.languages = list(self.db.ete_language.find())
        self.application = {}

    def getParameterListOfValues(self, app):
        result = {}
        for parameterType in app.parameterTypes:
            parameterTypeId = parameterType.pop('parameter_type_id')
            # TODO:Lookup atomic_type_number'!
            result[parameterTypeId] = parameterType
        app.parameterTypes = result
        for parameterTypeId, parameterType in app.parameterTypes.items():
            result = list(self.db.parameter_list_of_values.find({'parameter_type_id': parameterTypeId}))
            parameterType['listOfValues'] = result

    def run(self):
        for appNo in self.db.application_program.find({}, {'program_id': 1 , '_id': 0}):
            app = Application(appNo['program_id'])
            self.getParameterListOfValues(app)
            print app.applicationId
            self.dumpParameterTypes(app)
            #print app

    def dumpParameterTypes(self, app):
        if app.device_type == 0xa01d:
            pass
        # ParameterTypes
        for key, item in sorted(app.parameterTypes.items(), key = lambda x: x[0]):
            parameterTypeId = "%s_PT-%s" % (app.applicationId, knx_escape.escape(item['parameter_type_name']))
            atNumber = item['atomic_type_number']
            print '<ParameterType Id="%s" Name="%s" InternalDescription="%s">' % (parameterTypeId, item['parameter_type_name'], item['parameter_type_description'] or '')
            if atNumber == 1:
                print '   <TypeNumber SizeInBit="%u" Type="unsignedInt" minInclusive="%u" maxInclusive="%u" />' % (item['parameter_type_size'], item['parameter_minimum_value'], item['parameter_maximum_value'])
            elif atNumber == 4:
                print '   <TypeRestriction Base="Value" SizeInBit="%u">' % (item['parameter_type_size'], )
                for value in sorted(item['listOfValues'], key = lambda x: x['display_order']):
                    enumId = "%s_EN-%u" % (parameterTypeId, value['real_value'])
                    print '      <Enumeration Text="%s" Value="%s" Id="%s" DisplayOrder="%u" />' % (value['displayed_value'], value['real_value'], enumId, value['display_order'])
                print '   </TypeRestriction>'
            elif atNumber == 5:
                print '   <TypeRestriction Base="BinaryValue" SizeInBit="%u">' % (item['parameter_type_size'], )
                for value in sorted(item['listOfValues'], key = lambda x: x['display_order']):
                    enumId = "%s_EN-%u" % (parameterTypeId, value['real_value'])
                    print '      <Enumeration Text="%s" Value="%s" Id="%s" DisplayOrder="%u" BinaryValue="%s" />' % (value['displayed_value'], value['real_value'], enumId, value['display_order'], value['binary_value'])
                print '   </TypeRestriction>'
            elif atNumber == 0:
                print "   <TypeNone />"
            else:
                print "Uups!"
            print "</ParameterType>"
        # Parameter
        for item in sorted(app.parameters, key = lambda x: x['parameter_number']):
            if item['par_parameter_id'] is None:
                print item['parameter_name'], item['parameter_description']


#app = ApplicationBuilder('SAS_X6-16_VD-TP_XX_V06-11-03_VD3')
#app.run()

