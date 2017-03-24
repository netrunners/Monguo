#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: lime
# @Date:   2013-10-25 19:45:09
# @Last Modified by:   lime
# @Last Modified time: 2013-11-11 20:22:37

import re
from bson import DBRef
from bson.objectid import ObjectId

def camel_to_underline(camel):
    if not type(camel) is str:
        raise TypeError('camel should be string type!')

    return ''.join([''.join(('_', item.lower()))
        if item.isupper() and index else item.lower() for index, item in enumerate(camel)])

def legal_variable_name(name):
    regex = re.compile('^[_a-zA-Z][_a-zA-Z0-9]*$')
    if regex.match(str(name)):
        return True
    return False

def isnum(value):
    try:
        float(value)
    except:
        return False
    else:
        return True

def DB_Ref(Document,_id):
    ''' this is valid for _id as a string id  ('5890365...')
    or for an ObjectId already ObjectId('5890365...')

    ie : ObjectId(ObjectId('5890365...')) is ok '''

    return DBRef(Document.meta['collection'], ObjectId(_id))
