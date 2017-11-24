#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: lime
# @Date:   2014-03-26 14:00:01
# @Last Modified by:   lime
# @Last Modified time: 2014-03-26 14:01:38

from tornado.testing import AsyncTestCase

class MonguoTestBase(AsyncTestCase):
    print('test run order is alphabetical')

    def __init__(self,test):
        AsyncTestCase.__init__(self,test)
        print ('test : ',test)
    pass


__all__ = ['MonguoTestBase','test_connection']
