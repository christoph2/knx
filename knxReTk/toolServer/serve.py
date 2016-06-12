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


import base64
import os
import urllib
import uuid
import zlib

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import pymongo as mongo
import json

from tornado.options import define, options
from knxReTk.utilz.knx_escape import escape, unescape

SERVER_VERSION = "1.0"
SERVER_NAME = "KNXToolServer"

define("port", default = 8086, help = "run on the given port", type = int)

cookieSecret = lambda: base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
unescaper = lambda x: unescape(urllib.unquote(x))
escaper = lambda x: urllib.quote(escape(x))
expiration = lambda minutes: datetime.datetime.utcnow() + datetime.timedelta(minutes = minutes)


class Catalog(object):

    def __init__(self, conn, dbName):
        self._rawEntries = list(conn[dbName].catalog.find())
        self._items = {}
        self._sections = []
        for entry in self._rawEntries:
            self._sections.append(self.getSection(entry))
        self._sections = self._sections[0]

    @property
    def sections(self):
        return self._sections

    def items(self, path):
        return self._items.get(path, [])

    def _cleanupItems(self, items):
        result = []
        for item in items:
            if '_id' in item:
                item.pop('_id')
            if 'defaultLanguage' in item:
                item.pop('defaultLanguage')
            result.append(item)
        return result

    def getSection(self, entry, level = 0, path = None):
        if path is None:
            path = []
        result = []
        level += 1
        for section in entry['sections']:
            visibleDescription = section['visibleDescription'] if 'visibleDescription' in section else ''
            newSection = {'name': section['name'], 'number': section['number'], 'visibleDescription': visibleDescription , 'sections': []}
            path.append(escape(section['number']).encode('utf-8'))
            pathStr = urllib.quote('/'.join(path))
            self._items[pathStr] = self._cleanupItems(section['items'])
            newSection['path'] = pathStr
            result.append(newSection)                
            subSections = self.getSection(section, level, path)
            path.pop()
            if subSections:
                newSection['sections'].append(subSections[0])
        level -= 1
        return result


def catalogDBs(conn):
    result = []
    for dbName in conn.database_names():
        collections = set(conn[dbName].collection_names())
        catalog = set(('catalog', 'hardware') )
        if catalog.issubset(collections):
            result.append(escaper(dbName))
    return sorted(result)

def dbExists(conn, dbName):
    return dbName in conn.database_names()


class Application(tornado.web.Application):
    def __init__(self):
        self.conn = mongo.Connection()
        self._catalogCache = {}
        
        handlers = [
            #(r"/", MainHandler),
            (r"/catalogs", CatalogListingHandler, dict(conn = self.conn)),
            (r"/catalog/([a-zA-Z0-9.]+)", CatalogHandler, dict(conn = self.conn)),
            (r"/catalog-items/([a-zA-Z0-9.]+)/([a-zA-Z0-9./]+)", CatalogItemHandler, dict(conn = self.conn)),
        ]
        settings = dict(
            template_path = os.path.join(os.path.dirname(__file__), "templates"),
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            #ui_modules = {"Book": BookModule},
            debug = True,
            cookie_secret = "aFL9dOPzTG6UE8b/HetIHOB3tsaC40CGhPuZRWgaJQ0=",
            #xsrf_cookies = True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

    def catalog(self, name):
        if not dbExists(self.conn, name):
            return None
        if not name in self._catalogCache:
            self._catalogCache[name] = Catalog(self.conn, name)
        return self._catalogCache[name]


class BaseHandler(tornado.web.RequestHandler):
    
    def initialize(self, conn):
        self.conn = conn

    def set_default_headers(self):
        self.set_header('Server', '{0!s}/{1!s}'.format(SERVER_NAME, SERVER_VERSION))

    def write(self, chunk, contentType = None):
        acceptedEncodings = self.request.headers.get('accept-encoding', '')
        if 'deflate' in acceptedEncodings:
            self.add_header('Content-Encoding', 'deflate')
            if not isinstance(chunk, (basestring, buffer)):
                chunk = json.dumps(chunk)
            chunk = zlib.compress(chunk, zlib.Z_BEST_COMPRESSION)
        super(BaseHandler, self).write(chunk)
        if contentType:
            self.set_header('Content-Type', contentType)

    def catalog(self, name):
        return self.application.catalog(name)


class CatalogHandler(BaseHandler):
    
    def get(self, name):
        name = unescaper(name)
        catalog = self.catalog(name)
        if not catalog:
            self.set_status(404)
            #self.send_error(404)
        else:
            #catalog = Catalog(self.conn, name)
            self.write(json.dumps(catalog.sections), 'application/json')


class CatalogItemHandler(BaseHandler):

    def get(self, name, item):
        name = unescaper(name)
        catalog = self.catalog(name)
        if not catalog:
            #self.send_error(404)
            self.set_status(404)
        else:
            self.write(json.dumps(catalog.items(item)), 'application/json')        


class CatalogListingHandler(BaseHandler):
    
    def get(self):
        self.write(json.dumps(catalogDBs(self.conn)), 'application/json')


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
