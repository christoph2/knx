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
    entry_points = {
	'console_scripts': [
		'vd_exporter = knxReTk.catalogue.vd_exporter:main'
        ],
    },
    data_files = [
            ('knxReTk/config', glob('knxReTk/config/*.*')),
            ('knxReTk/imagez', glob('knxReTk/imagez/*.bin')),
    ],
)

