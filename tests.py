#!/usr/bin/env python
# encoding: utf-8

import unittest
from tornado import testing

from redisorm.model import Model
from redisorm.fields import IntField, SetField


class TestModel(Model):
    num = IntField()


class MyTestCase(testing.AsyncTestCase):
    @testing.gen_test
    def test_model_create(self):
        t = TestModel(num=1)
        self.assertEqual(t.num, 1)


def all():
    suites = []
    suites.append(unittest.TestLoader().loadTestsFromTestCase(MyTestCase))
    return unittest.TestSuite(suites)

if __name__ == '__main__':
    testing.main()
