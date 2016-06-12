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

##
## Convenience functions for Mako Templates.
##

from cStringIO import StringIO
import re

from mako.template import Template
from mako.runtime import Context
from mako import exceptions

from knxReTk.utilz import strings

indentText = lambda text, leftmargin = 0: '\n'.join(["%s%s" % ((" " * leftmargin), line, ) for line in text.splitlines()])


def renderTemplate(filename = None, text = None, namespace = None, leftMargin = 0, rightMargin = 80, formatExceptions = True, encoding = 'utf-8'):
    if namespace is None:
        namespace = {}
    if filename is None and text is None:
        raise AttributeError("Neither 'filename' nor 'text' specified.")
    buf = StringIO()
    ctx = Context(buf, **namespace)
    try:
        if filename is not None:
            tobj = Template(filename = filename, output_encoding = encoding,  format_exceptions = formatExceptions) #, imports ='re' # TODO: imports parameter.
        elif text is not None:
            tobj = Template(text = text, output_encoding = encoding, format_exceptions = formatExceptions) #, imports ='re'
        tobj.render_context(ctx)
    except:
        print exceptions.text_error_template().render()
        return None
    return strings.reformat(buf.getvalue(), leftMargin, rightMargin)
    #return buf.getvalue()


def callDef(template, definition, *args, **kwargs):
    return template.get_def(definition).render(*args, **kwargs)

