#!/usr/bin/env python
# encoding: utf-8

import unittest
from tornado import testing

from redisorm.model import Model
from redisorm.field import IntField, SetField


class TestModel(Model):
    id = IntField()
    members = SetField()


class MyTestCase(testing.AsyncTestCase):
    @testing.gen_test
    def test_model_create(self):
        t = TestModel(id=1, members=[1, 2, 3])


def all():
    suites = []
    suites.append(unittest.TestLoader().loadTestsFromTestCase(MyTestCase))
    return unittest.TestSuite(suites)

if __name__ == '__main__':
    testing.main()
