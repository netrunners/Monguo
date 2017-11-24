======
Monguo
======

This is the port of Monguo to Python3.6
using python async functions instead of tornado coroutines

the previous version is in the 3.0 branch

You may need to uninstall the previous installation
before installing this one.

.. image:: https://github.com/shiyanhui/monguo/blob/master/doc/source/_static/monguo.jpg?raw=true
	:width: 100px

:Info: Monguo is a full-featured, asynchronous MongoDB_ ORM with Motor_ dirver for Tornado_ applications.
:Author: Lime YH.Shi
:Maintainer: Phil Estival


Installation
============

.. code-block:: bash

    $ pip install monguo

Dependencies
============

Monguo works in all the environments officially supported by Tornado_ and Motor_. It requires:

* pymongo_ >=3.4,<4
* tornado_ >=4.4
* greenlet_ >=0.4
* motor_ >=1.1

Examples
========

.. code-block:: python

    from monguo import *

    Connection.connect('db') # connect to database

    class UserDocument(Document):
        name  = StringField(required=True, unique=True, max_length=20)
        email = EmailField(required=True)
        age   = IntegerField()
        sex   = StringField(default='male', candidate=['male', 'female'])

        meta = {
            'collection': 'user'
        }

        @gen.coroutine
        def get_user_list(skip=0, limit=None):
            cursor = UserDocument.find().skip(skip)

            if limit:
                assert isinstance(limit, int) and limit > 0
                cursor.limit(limit)

            user_list = yield cursor.to_list(None)
            raise gen.Return(user_list)

    # insert
    user_id = yield UserDocument.insert({
        'name': 'Bob',
        'email': 'bob@gmail.com'
    })

    # query
    user = yield UserDocument.find_one({'name': 'Bob'})
    user_list = yield UserDocument.get_user_list()

    # update
    yield UserDocument.update(
        {'_id': user_id},
        {'$set': {'age': 19}})

    # delete
    yield UserDocument.remove({'_id': user_id})


.. _MongoDB: http://mongodb.org
.. _Tornado: http://tornadoweb.org
.. _Motor: https://github.com/mongodb/motor

