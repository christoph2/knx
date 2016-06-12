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

import datetime
import glob
from hashlib import sha1
import json
import os
import re
import sys
import pymongo as mongo
from bson.objectid import ObjectId

from knxReTk.catalogue import bootstrap
from knxReTk.catalogue.locales import getLocalCode
from knxReTk.vdimex.loader import CatalogueReverser, process
from knxReTk.vdimex.xmlloader.loader import processXML
from knxReTk.vdimex import preETS4Converter

CLASSIC_ETS = re.compile(r'vd[x1-5] | pr[x1-5]$', re.I | re.VERBOSE)
MODERN_ETS = re.compile(r'knxprod$', re.I)

def getMongoClient(host = 'localhost', port = None):
    return mongo.MongoClient(host = 'localhost', port = port)

try:
    mongoClient = getMongoClient()
    bootstrap.init(mongoClient)
except Exception as e:
    print "Problem with Database Connection: '{0!s}'.".format(str(e))
    print "Exiting."
    sys.exit(1)

RTF_MAGIC = [123, 92, 114, 116, 102]    # ==> '{\rtf'

class MongoLoader(CatalogueReverser):

    def __init__(self, data, path, uniqueName, hashValue):
        super(MongoLoader, self).__init__(data, path, uniqueName, hashValue)
        self.database = mongoClient[uniqueName]

    def onHeader(self, headerInfo):
        self.headerInfo = headerInfo

        self.database.meta.update({"_id": headerInfo["hashValue"]}, {"_id": headerInfo["hashValue"], "tables": []},
                                  safe = True, upsert = True
        )
        print "Importing tables: ",

    def onFinished(self):
        defaultLanguage = self.database.ete_language.find_one({"database_language": 1}, {"language_id": 1, '_id': 0}).get('language_id', 1033)
        defaultLanguageCode = getLocalCode(defaultLanguage)
        self.database.meta.update({"_id": self.headerInfo["hashValue"]}, {
                "$set": {
                    "defaultLanguage": defaultLanguageCode,
                    "languages": [getLocalCode(lang['language_id']) for lang in list(self.database.ete_language.find({}, {'_id': 0, 'language_id': 1}))]
                    }
            },
            safe = True
        )
        print
        print "-" * 79
        print "Finished Loading."
        print

    def onRow(self, rowInfo):
        hashValue = sha1(json.dumps(rowInfo)).hexdigest()
        rowInfo['_id'] = hashValue
        #result = self.database[self.currentTable].insert(rowInfo, safe = True)
        result = self.database[self.currentTable].update({"_id": hashValue}, rowInfo, safe = True, upsert = True)

    def startTable(self, name, tableNumber, columnList):
        self.currentTable = name
        self.database.meta.update({"_id": self.headerInfo["hashValue"]},
                                  {"$push": {"tables": {"_id": name, "number": tableNumber, "columns": columnList}}},
                                  safe = True
        )
        print name,

    def endTable(self, name):
        pass

#sys.argv.append(r'C:\projekte\csProjects\knxReTk\tests\SAS_X6-16_VD-TP_XX_V06-11-03.knxprod')
#sys.argv.append(r'C:\projekte\csProjects\knxReTk\tests\ETS3_ALL.knxprod')

def main():
    if len(sys.argv) != 2:
        print "usage: ets_loader filespec"
        sys.exit(1)
    else:
        if len(glob.glob(sys.argv[1])) == 0:
            print "filespec does not match."
            sys.exit(1)
        for filename in sorted(glob.glob(sys.argv[1])):
            if CLASSIC_ETS.search(filename):
                print "Processing:", filename
                process(MongoLoader, filename, 'Orleander')
                preETS4Converter.convert(os.path.split(filename)[1].replace('.', '_'))
            elif MODERN_ETS.search(filename):
                print "Processing:", filename
                processXML(filename)

if __name__ == '__main__':
    main()

