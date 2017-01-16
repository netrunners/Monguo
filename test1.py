#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: lime
# @Date:   2014-03-26 14:00:01
# @Last Modified by:   lime
# @Last Modified time: 2014-03-26 14:37:29

from datetime import datetime
from bson.dbref import DBRef
from tornado import gen
from tornado.ioloop import IOLoop
from pprint import pprint

from monguo.document import *
from monguo.field import *
from monguo.connection import *

class UserDocument(Document):
    name  = StringField(required=True, unique=True, max_length=20)
    email = EmailField(required=True)
    age   = IntegerField()
    sex   = StringField(required=True, default='male',
                                       candidate=['male', 'female'])

    meta = {
        'collection': 'user'
    }

    @gen.coroutine
    def get_user_list_1():
        result = yield UserDocument.to_list(UserDocument.find())
        raise gen.Return(result)


    @staticmethod
    @gen.coroutine
    def get_user_list_2():
        result = yield UserDocument.to_list(UserDocument.find())
        raise gen.Return(result)


    @classmethod
    @gen.coroutine
    def get_user_list_3(cls):
        result = yield UserDocument.to_list(UserDocument.find())
        raise gen.Return(result)


    def get_user_list_4():
        result = [item for item in UserDocument.get_collection(True).find()]
        return result

    @staticmethod
    def get_user_list_5():
        result = [item for item in UserDocument.get_collection(True).find()]
        return result

    @classmethod
    def get_user_list_6(cls):
        result = [item for item in UserDocument.get_collection(True).find()]
        return result


class CommentDocument(EmbeddedDocument):
    commentor = ReferenceField(UserDocument, required=True)
    contents  = StringField(required=True, max_length=200)


class PostDocument(Document):
    author       = ReferenceField(UserDocument, required=True)
    publish_time = DateTimeField(required=True)
    title        = StringField(required=True, max_length=100)
    contents     = StringField(max_length=5000)
    comments     = ListField(EmbeddedDocumentField(CommentDocument))

    meta = {
        'collection': 'post'
    }


@gen.coroutine
#XXX todo : enforce tests, more assertions, migrate to testunit
def test():

    print('drop users')
    yield UserDocument.remove()
    print('insert user 1')
    bob_id = yield UserDocument.insert({
        'name': 'Bob',
        'email': 'bob@gmail.com',
        'age': 19
    })
    print('insert user 2')

    alice_id = yield UserDocument.insert({
        'name': 'Alice',
        'email': 'alice@gmail.com',
        'sex': 'female',
        'age': 18
    })

    print('insert post')

    post_id = yield PostDocument.insert({
        'author': DBRef(UserDocument.meta['collection'], bob_id),
        'publish_time': datetime.now(),
        'title': 'title',
    })

    comment = {
        'commentor': DBRef(UserDocument.meta['collection'], alice_id),
        'contents': 'I am comments.'
    }
    print('update post with comment')

    yield PostDocument.update({'_id': post_id},
                              {'$push': {'comments': comment}})


    print('\nResults')
    user = yield UserDocument.find_one({'name': 'Bob'})
    print('find bob : ', user)

    posts = yield PostDocument.find().to_list(5)
    print('post list :')
    pprint(posts)
    assert len(posts) is 5
    user_list = yield UserDocument.get_user_list_1()
    print('user list method 1', user_list)
    user_list = yield UserDocument.get_user_list_2()
    print (user_list)
    print('user list method 2', user_list)

    print('user list method 3', user_list)

    user_list = yield UserDocument.get_user_list_3()

    print (user_list)
    user_list = UserDocument.get_user_list_4()
    print (user_list)
    user_list = UserDocument.get_user_list_5()
    print (user_list)
    user_list = UserDocument.get_user_list_6()
    print (user_list)


if __name__ == '__main__':
    Connection.connect('test2')
    IOLoop.instance().run_sync(test)

