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


from array import array
from base64 import b64encode
import codecs
from collections import namedtuple, defaultdict
from decimal import Decimal
import glob
import os
import re
import string
import sys
import xml.sax.saxutils as saxutils
import zipfile

XML_DECL = '<?xml version="1.0" encoding="utf-8" ?>'

BASE_PATH = r'C:\projekte\csProjects\pyKNX'

def slicer(iteratable, sliceLength, resultType = None):
    if resultType is None:
        resultType = type(iteratable)
    length = len(iteratable)
    return [resultType(iteratable[i : i + sliceLength]) for i in range(0, length, sliceLength)]

def getZipFileContents(fname, password):
    result = dict()
    with zipfile.ZipFile(fname) as zf:
        directory = os.path.splitext(os.path.split(zf.filename)[1])[0]
        zf.printdir()
        for fl in zf.filelist:
            inf = zf.open(fl, 'r', password)
            completePath = os.path.join(directory, fl.filename)
            basedir, filename = os.path.split(completePath)
            if not os.access(basedir, os.F_OK):
                os.makedirs(basedir)
            data = inf.read()
            result[fl.filename] = (data, completePath)
            with open(completePath, 'w') as outf:
                outf.write(data)
    return result

##
##
##
SEPARATOR       = "-" * 37
SEPARATOR2      = re.compile(u'^-{34, 40}$')
CONTINUATION    = r"\\"
MAGIC_SIG       = "EX-IM"
EOF_SIG         = "XXX"

TABLE           = re.compile(r'''
    ^T\s+(?P<tableNumber>\d{,3})\s+
    (?P<name>[a-zA-Z][A-Za-z_0-9]+)$
''', re.VERBOSE)

COL_DESC        = re.compile(r'''
    ^C(?P<colNumber>\d{,3})\s+
    T(?P<tableNumber>\d{,3})\s+
    (?P<type>\d{,2})\s+
    (?P<length>\d{,9})\s+
    (?P<nulls>Y | N)\s+
    (?P<name>[a-zA-Z][a-zA-Z_0-9]+)$
''', re.VERBOSE)

ROW             = re.compile(r'''
    ^R\s+(?P<rowNumber>\d{,9})\s+
    T\s+(?P<tableNumber>\d{,3})\s+
    (?P<name>[a-z][a-z_]+)$
''', re.VERBOSE)


TYPE_MAP = {
    '1': 'integer',
    '2': 'smallint',
    '3': 'varchar',
    '4': 'varchar',
    '5': 'numeric', # 8 ==> 7,2 -
    '6': 'binary',
    '7': '',
    '8': 'long binary',
    '9': '',
    '10': '',
}

TableNamesToNumbers = defaultdict(set)

class FormatError(Exception): pass
class EofError(Exception): pass

class Dummy(object):

    def __str__(self):
        result = []
        for key in [x for x in dir(self) if not (x.startswith('_'))]:
            result.append("%s = '%s'" % (key, getattr(self, key)))
        return '\n'.join(result)


STATE_IDLE      = 0
STATE_TABLE     = 1
STATE_COLUMN    = 2
STATE_ROW       = 3
STATE_ROW_IND   = 4

identity = lambda n: n
hexStrToBase64 = lambda bob: b64encode(''.join([chr(int(b, 16)) for b in slicer(bob, 2)]))
strEscape = lambda s: saxutils.escape(s)

class Column(object):
    TYPE_MAP = {
    'integer':      long,
    'smallint':     int,
    'varchar':      strEscape,
    'numeric':      Decimal,
    'binary':       hexStrToBase64,
    'long binary':  hexStrToBase64,
    }

    def __init__(self, name, type_, nulls, length, colNumber, tableNumber):
        self.name = name
        self.type_ = TYPE_MAP[type_]
        if self.type_ == '':
            raise TypeError()
        self._converter = None  # TODO: Aus dem Typen ableiten!!!
        self.nulls = True if nulls == 'Y' else False
        self.length = int(length)
        self.colNumber = int(colNumber)
        self.tableNumber = int(tableNumber)

    def _getConverter(self):
        if self.type_ == 'numeric':
            pass
        return self.TYPE_MAP[self.type_]

    converter = property(_getConverter)

class Builder(object):

    def __init__(self):
        self.data = []
        self.finished = False

    def add(self, data):
        self.data.append(data)

    def finish(self):
        self.finished = True
        data = self.data
        self.data = []
        return data


class ColumnBuilder(Builder):

    def add(self, data):
        if data.startswith(CONTINUATION):
            data = data[2 : ]
        super(ColumnBuilder, self).add(data)

    def finish(self):
        data = super(ColumnBuilder, self).finish()
        return ''.join(data)


class RowBuilder(Builder): pass


class TableBuilder(object):
    tablesByNumber = {}

    def __init__(self, name, number):
        self.name = name
        self.number = int(number)
        self.columns = []
        self.columnsByNumber = {}
        self.columnCount = 0
        TableBuilder.tablesByNumber[self.number] = self

    def addColumn(self, column):
        self.columns.append(column)
        self.columnsByNumber[column.colNumber] = column
        self.columnCount += 1

    def startInstance(self):
        pass

    def finishInstance(self):
        pass

    def __getitem__(self, item):
        return self.columnsByNumber[item]


class CatalogueReverser(object): # TODO: Strategy

    def __init__(self, data, path):
        self.data = data.splitlines()
        self.checkSignature()
        self.pos = 0
        self.state = STATE_IDLE

        _, relpath = os.path.splitdrive(path)
        fname, _ = os.path.splitext(relpath)
        self.outf = codecs.open('%s.xml' % fname, mode = 'w', encoding = "utf-8")
        print 'TARGET FILE: %s.xml' % fname

    def _getLine(self):
        line = unicode(self.data[self.pos], 'latin-1')
        self.pos += 1
        return line

    def lines(self, count):
        return [self.line for _ in range(count)]

    def _getBlock(self):
        result = []
        line = self.line
        finished = False
        while line != SEPARATOR:
            result.append(line)
            try:
                line = self.line
            except IndexError:
                result.pop()
                finished = True
                break
        return result, finished

    line = property(_getLine)
    block = property(_getBlock)

    def parse(self):
        self.parseFileHeader()
        self.parseTables()
        self.outf.close()

    def checkSignature(self):
        if self.data[0] != MAGIC_SIG:
            raise FormatError("Catalogue doesn't start with '%s'." % MAGIC_SIG)
        if self.data[-1] != EOF_SIG:
            raise FormatError("Catalogue doesn't end with '%s'." % EOF_SIG)

    def parseFileHeader(self):
        ATTRIBUTE_MAP = {
            "N": "originalFilename",
            "K": "creator",
            "D": "date",
            "V": "version",
            "H": "rootTable",
        }
        header = Dummy()
        block, finished = self.block
        for tag, content in filter(lambda x: len(x) == 2, [string.split(l, maxsplit = 1) for l in block[1:]]):
            setattr(header, ATTRIBUTE_MAP[tag], content)
        setattr(self, 'header', header)
        print "HEADER: \n%s\n\n" % header

    def parseTables(self):
        idx = 0
        finished = False
        self.state = STATE_TABLE
        columnIdx = 0
        columnBuilder = ColumnBuilder()
        rowBuilder = RowBuilder()
        self.outf.write("%s\n" % XML_DECL)
        originalFilename = self.header.originalFilename
        if hasattr(self.header, 'creator'):
            creator = self.header.creator
        else:
            creator = "<Unknown>"
        date = 'T'.join(self.header.date.split())
        version = self.header.version
        rootTable = self.header.rootTable
        self.outf.write('<CATALOGUE originalFilename="%s" creator="%s" date="%s" version="%s" rootTable="%s" >\n' % (
            originalFilename, creator, date, version, rootTable)
        )
        while not finished:
            idx += 1
            block, finished = self.block
            #print "Block #%03u\r" % idx,
            self.state = STATE_TABLE
            self.parseTableHeader()
            for lineNumber, line in enumerate(block, 1):
                if self.state == STATE_TABLE:
                    ma = TABLE.match(line)
                    if ma:
                        #print "TABLE:", ma.groupdict()
                        TableNamesToNumbers[ma.group("name")].add(ma.group("tableNumber"))

                        tb = TableBuilder(ma.group("name"), ma.group("tableNumber"))
                        self.outf.write("    <%sS>\n" % tb.name.upper())
                        self.state = STATE_COLUMN
                    else:
                        raise FormatError("Expected table declaration [%u]: '%s'." % (lineNumber, line))
                elif self.state == STATE_COLUMN:
                    ma = COL_DESC.match(line)
                    if ma:
                        tb.addColumn(
                            Column(ma.group("name"), ma.group("type"), ma.group("nulls"),
                                ma.group("length"), ma.group("colNumber"), ma.group("tableNumber")))
                    else:
                        ma = ROW.match(line)
                        if ma:
                            tableNumber = int(ma.group('tableNumber'))
                            rowNumber = int(ma.group('rowNumber'))
                            columnIdx = 1
                            self.outf.write("        <%s>\n" % tb.name.upper())
                            self.state = STATE_ROW
                elif self.state == STATE_ROW:
                    columnBuilder.add(line)
                    if lineNumber <= len(block) - 1:
                        continuation = block[lineNumber].startswith(CONTINUATION)
                        if continuation:
                            pass
                    else:
                        continuation = False
                    if not continuation:
                        chunk = columnBuilder.finish()
                        if chunk == '':
                            chunk = None
                        else:
                            chunk = tb[columnIdx].converter(chunk)
                        rowBuilder.add(chunk)
                        columnIdx += 1
                        if columnIdx > tb.columnCount:
                            row = rowBuilder.finish()
                            for idx, value in enumerate(row, 1):
                                name = tb[idx].name
                                #print name, value
                                if value:
                                    #if isinstance(value, basestring):
                                    #    value = value.encode("utf-8")
                                    self.outf.write("            <%s>%s</%s>\n" % (name, value, name))
                            self.state = STATE_ROW_IND
                            self.outf.write("        </%s>\n" % tb.name.upper())
                elif self.state == STATE_ROW_IND:
                    if not columnBuilder.finished:
                        raise Exception("Uups!")
                    ma = ROW.match(line)
                    if ma:
                        tableNumber = int(ma.group('tableNumber'))
                        rowNumber = int(ma.group('rowNumber'))
                        columnIdx = 1
                        self.state = STATE_ROW
                        self.outf.write("        <%s>\n" % tb.name.upper())
                    else:
                        raise FormatError("Expected row indicator [%u]: '%s'." % (lineNumber, line))
            self.outf.write("    </%sS>\n" % tb.name.upper())
        self.outf.write("</CATALOGUE>\n")

    def parseTableHeader(self):
        pass

    def parserTableData(self):
        tableNumber = int(ma.groupdict('tableNumber'))
        rowNumber = int(ma.groupdict('rowNumber'))
        columnIdx = 1

def run(fileName, password):
    result = getZipFileContents(fileName, password)
    print "\n", "=" * 80
    for key, (data, path) in result.items():
        _, fname = os.path.split(key)
        if fname in ('ets2.vd_', 'ets.vd_', 'ets.pr_'):
            print "\nCATALOGUE: ", key
            rev = CatalogueReverser(data, path)
            rev.parse()
            print
    print "\n", "=" * 80



def main():
    print """
vd_exporter: export / convert ETS 'vd?' and 'pr?' files to XML.
"""
    print
    if len(sys.argv) != 2:
        print "usage: vd_exporter filespec"
        sys.exit(1)
    else:
        if len(glob.glob(sys.argv[1])) == 0:
            print "filespec does not match."
            sys.exit(1)
        password = sys.argv[1]
        for filename in glob.glob(sys.argv[1]):
            run(filename, 'Orleander')

if __name__ == '__main__':
    main()

