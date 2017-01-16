#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: lime
# @Date:   2014-03-26 14:00:01
# @Last Modified by:   lime
# @Last Modified time: 2014-03-26 14:01:29

from tornado.testing import gen_test

from motor import MotorClient, MotorDatabase
from motor import MotorReplicaSetClient

from monguo.connection import Connection
from . import MonguoTestBase

class ConnectionTest(MonguoTestBase):

    def test_connection(self):
        # test connect(), get_connection(), get_database()...
        Connection.connect('monguo_test1')
        connection = Connection.get_connection()
        database = Connection.get_database()
        db_name = Connection.get_default_database_name()
        connection_name = Connection.get_default_connection_name()

        self.assertIsInstance(connection, MotorClient)
        self.assertIsInstance(database, MotorDatabase)
        self.assertEqual(db_name, 'monguo_test1')
        self.assertEqual(connection_name, Connection.DEFAULT_CONNECTION_NAME)

        Connection.connect('monguo_test2', 'con')
        db_name = Connection.get_default_database_name()
        connection_name = Connection.get_default_connection_name()

        self.assertEqual(db_name, 'monguo_test2')
        self.assertEqual(connection_name, 'con')

        # test get_connection_name_list()
        connection_name_list = Connection.get_connection_name_list()
        self.assertIn(Connection.DEFAULT_CONNECTION_NAME, connection_name_list)
        self.assertIn('con', connection_name_list)
        self.assertEqual(sorted([Connection.DEFAULT_CONNECTION_NAME, 'con']),
                         sorted(connection_name_list))

        # test switch_connection()
        Connection.switch_connection(Connection.DEFAULT_CONNECTION_NAME)
        connection_name = Connection.get_default_connection_name()
        self.assertEqual(connection_name, Connection.DEFAULT_CONNECTION_NAME)

        # test switch_database()
        Connection.switch_database('monguo_test3')
        db_name = Connection.get_default_database_name()
        self.assertEqual(db_name, 'monguo_test3')

    def test_disconnect(self):
        Connection.disconnect()

        connection_name_list = Connection.get_connection_name_list()
        connection_name = Connection.get_default_connection_name()

        self.assertEqual(['con'], connection_name_list)
        self.assertEqual(connection_name, 'con')
