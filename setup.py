#!/usr/bin/env python
# @Author: lime
# @Author: Phil
# @Last Modified by: Phil
# Date:<2017/11/24 05:04:35>

try:
    from setuptools import setup
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

# Removed because pip fails to install -r requirements.txt
#import monguo

classifiers = """\
Intended Audience :: Developers
License :: OSI Approved :: Apache Software License
Development Status :: 5 - Production/Stable
Natural Language :: English
Programming Language :: Python :: 3.6
Operating System :: Linux :: MacOS X
Programming Language :: Python
"""

# Version definition in hardcode
version = '0.3.6'
description = 'Asynchronous MongoDB ORM for Tornado'
long_description = open("README.rst").read()
packages = ['monguo']

setup(
    name='monguo',
    version=version,
    packages=packages,
    description=description,
    long_description=long_description,
    author='Phil Estival',
    author_email='flint@forge.systems',
    url='https://github.com/flintforge/monguo',
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
