#!/bin/env/python

from distutils.core import setup, Extension
import os
from setuptools import find_packages
from glob import glob

def packagez(base):
    return  ["%s%s%s" % (base, os.path.sep, p) for p in find_packages(base)]

setup(
    name = 'knxReTk',
    version = '0.1.0',
    description = "'Konnex / EIB Reverserz Toolkit",
    author = 'Christoph Schueler',
    author_email = 'cpu12.gems@googlemail.com',
    url = 'https://www.github.com/Christoph2/knx',
    packages = packagez('knxReTk'),
    install_requires = ['mako', 'pymongo', 'tornado', 'pyserial', 'pyro4', 'requests'],
    entry_points = {
        'console_scripts': [
                'ets_loader = knxReTk.vdimex.ets_loader:main',
                'knx_blink          = knxReTk.busaccess.knx_blink:main',
                'knx_dump           = knxReTk.busaccess.knx_dump:main',
                'knx_progmode       = knxReTk.busaccess.knx_progmode:main',
                'knx_setaddr        = knxReTk.busaccess.knx_setaddr:main',
                'knx_busmon         = knxReTk.busaccess.knx_busmon:main',
                'knx_load           = knxReTk.busaccess.knx_load:main',
                'knx_properties     = knxReTk.busaccess.knx_properties:main',
                'knx_devinfo        = knxReTk.busaccess.knx_devinfo:main',
                'knx_mnt            = knxReTk.busaccess.knx_mnt:main',
                'knx_scan           = knxReTk.busaccess.knx_scan:main',
                'knx_devstate       = knxReTk.busaccess.knx_devstate:main',
                'knx_send           = knxReTk.busaccess.knx_send:main',
        ],
    },
    data_files = [
            ('knxReTk/config', glob('knxReTk/config/*.*')),
            ('knxReTk/imagez', glob('knxReTk/imagez/*.bin')),
            ('knxReTk/templates/bcu1', glob('knxReTk/templates/bcu1/*.tmpl')),
            ('knxReTk/symbols', glob('knxReTk/symbols/*.*')),
    ],
)

