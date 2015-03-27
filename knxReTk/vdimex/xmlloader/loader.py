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

from collections import namedtuple, OrderedDict, defaultdict
import os
from pprint import pprint
import sys
import pymongo as mongo
import bson

from knxReTk.utilz.ziptool import getZipFileContents
from knxReTk.vdimex.xmlloader.mixins import CatalogMixin, HardwareMixin, LanguageMixin, ApplicationMixin
from knxReTk.vdimex.xmlloader.parser import parse, XMLHandler


class HardwareParser(XMLHandler, HardwareMixin, LanguageMixin):

    def __init__(self):
        XMLHandler.__init__(self)
        HardwareMixin.__init__(self)
        LanguageMixin.__init__(self)


class CatalogParser(XMLHandler, CatalogMixin, LanguageMixin):

    def __init__(self):
        XMLHandler.__init__(self)
        CatalogMixin.__init__(self)
        LanguageMixin.__init__(self)


class ApplicationParser(XMLHandler, ApplicationMixin, LanguageMixin):

    def __init__(self):
        XMLHandler.__init__(self)
        ApplicationMixin.__init__(self)
        LanguageMixin.__init__(self)


def getMongoClient(host = 'localhost', port = None):
    return mongo.MongoClient(host = 'localhost', port = port)

def translate(obj, translations):
    if '_id' in obj and obj['_id'] in translations:
        trans = translations[obj['_id']]
        obj['translations'] = translations[obj['_id']]
    for k, v in obj.items():
        if k == 'translations':
            continue
        if isinstance(v, list):
            for item in v:
                if not isinstance(item, (list, dict, )):
                    continue
                translate(item, translations)
        elif isinstance(v, dict):
            translate(v, translations)


def processResult(resultObj, collection):
    mongoClient = getMongoClient()

    db = mongoClient.catalogue
    #db[collection].drop()
    #bulk = db.hardware.initialize_unordered_bulk_op()

    translations = resultObj.translations

    for v in resultObj.result:
        if v['_id'] in translations:
            pass
        for product in v['products']:
            productId = product['_id']
            if productId in translations:
                translation = translations[productId].get(productId)
                if translation:
                    product['translations'] = translations[productId].pop(productId)
                    translations.pop(productId)
        try:
            #bulk.insert(v)
            #db[collection].insert(v)
            db[collection].update({'_id': v['_id']}, v, upsert = True)
        except mongo.errors.DuplicateKeyError as e:
            print "Exception: ", str(e)
    #if translations:
    #    print translations

def processHardware(db, resultObj, collection):
    #bulk = db.hardware.initialize_unordered_bulk_op()

    translations = resultObj.translations

    for product in resultObj.result:
        if product['_id'] in translations:
            translate(product, translations[product['_id']])

        #db[collection].insert(product)
        db[collection].update({'_id': product['_id']}, product, upsert = True)

def processCatalog(db, resultObj, collection):
    #bulk = db.hardware.initialize_unordered_bulk_op()

    translations = resultObj.translations

    #translate(resultObj.result, translations)
#    if resultObj.result['_id'] in translations:
#        translate(resultObj.result, translations[resultObj.result['_id']])

    #db[collection].insert(resultObj.result)
    db[collection].update({'_id': resultObj.result['_id']}, resultObj.result, upsert = True)


def processApplication(db, resultObj, collection):

    translations = resultObj.translations

    for k, v in resultObj.result.items():
        for app in v['applicationPrograms']:
            if app['_id'] in translations:
                translate(app, translations[app['_id']])
            #print app['_id']
            try:
#                db[collection].insert(app)
                db[collection].update({'_id': app['_id']}, app, upsert = True)
            except mongo.errors.DuplicateKeyError as e:
                print "Exception: ", str(e)
    return


def processXML(filename):
    uniqueTags = []

    mongoClient = getMongoClient()

    _, fname = os.path.split(filename)
    db = mongoClient[fname.replace('.', '_')]
    db["catalog"].drop()
    db["application"].drop()
    db["hardware"].drop()
    unhandledTags = set()

    for (data, path, hashValue) in getZipFileContents(filename):
        if path.endswith('xml'):
            _, fname = os.path.split(path)
            XMLHandler.hashValue = hashValue
            print path
            if fname == 'Catalog.xml':
                resultObj = parse(data, CatalogParser)
                processCatalog(db, resultObj, "catalog")
            elif fname == 'Hardware.xml':
                resultObj = parse(data, HardwareParser)
                processHardware(db, resultObj, "hardware")
            elif fname.startswith("M-"):
                resultObj = parse(data, ApplicationParser)
                processApplication(db, resultObj, "application")
            else:
                continue
            #pprint(sorted(resultObj.unhandledTags))
            unhandledTags = unhandledTags.union(resultObj.unhandledTags)
    print "Finished Loading."
    print
    #pprint(sorted(unhandledTags))


