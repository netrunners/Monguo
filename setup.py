#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: lime
# @Date:   2013-11-07 14:45:40
# @Last Modified by:   lime
# @Last Modified time: 2014-03-26 15:24:22

try:
    from setuptools import setup, Feature
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, Feature

# Removed because pip fails to install -r requirements.txt 
#import monguo

classifiers = """\
Intended Audience :: Developers
License :: OSI Approved :: Apache Software License
Development Status :: 5 - Production/Stable
Natural Language :: English
rogramming Language :: Python :: 3.0
Programming Language :: Python :: 3.4
Operating System :: MacOS :: MacOS X
Operating System :: Unix
Programming Language :: Python
Programming Language :: Python :: Implementation :: CPython
"""

# Version definition in hardcode
version = '0.3.0'
description = 'Asynchronous MongoDB ORM for Tornado'
long_description = open("README.rst").read()
packages = ['monguo']

setup(name='monguo',
    version=version,
    packages=packages,
    description=description,
    long_description=long_description,
    author='Lime YH.Shi',
    author_email='shiyanhui66@gmail.com',
    url='https://github.com/shiyanhui/monguo',
    install_requires=[
        'motor >= 0.6.2',
    ],
    license='http://www.apache.org/licenses/LICENSE-2.0',
    classifiers=filter(None, classifiers.split('\n')),
    keywords=[
        "monguo", "mongo", "mongodb", "pymongo", "gridfs", "bson", "motor", 
        "tornado", "ORM", "asynchronous"
    ],
    zip_safe=False,
)
