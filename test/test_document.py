#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: lime
# @Date:   2014-03-26 14:00:01
# @Last Modified by:   lime
# @Last Modified time: 2014-03-26 14:07:06

import unittest

from tornado.testing import AsyncTestCase

from tornado.testing import gen_test

from monguo.connection import Connection
from monguo.document import Document, EmbeddedDocument
from monguo.field import *

from test import MonguoTestBase

class BookDocument(EmbeddedDocument):
    name  = StringField(required=True)
    pages = IntegerField(required=True)


class SkillDocument(EmbeddedDocument):
    name = StringField(required=True)


class PetDocument(Document):
    name = StringField(required=True)
    say  = StringField()

    meta = {
        'collection': 'pet'
    }


class UserDocument(Document):
    name   = StringField(required=True, unique=True)
    sex    = StringField(required=True, default='male')
    age    = IntegerField(required=True)
    skills = ListField(DictField(SkillDocument), required=True)
    book   = EmbeddedDocumentField(BookDocument, required=True)
    pet = ReferenceField(PetDocument)

    meta = {
        'collection': 'user'
    }


class DocumentTest(MonguoTestBase):
    def setUp(self):
        super(DocumentTest, self).setUp()
        Connection.connect('monguo_test')

    def tearDown(self):
        super(DocumentTest, self).tearDown()
        Connection.disconnect()

    @gen_test
    def test_0_remove(self):
        x = yield UserDocument.remove()
        print(x)

    @gen_test
    def test_insert(self):
        user = {
            'name': 'Lime',
            'age': 100,
            'skills': [{'name': 'python'}, {'name': 'Web Programming'}],
            'book': {'name': 'I am a bad guy', 'pages': '888'},
        }
        user_id = yield UserDocument.insert(user)
        print(user_id)

    def test_save(self):
        pass

    def test_update(self):
        pass


if __name__ == '__main__':
    unittest.main()

