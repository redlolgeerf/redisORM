#!/usr/bin/env python
# encoding: utf-8

import unittest
from tornado import testing

from redisorm.model import Model
from redisorm.fields import IntField
from redisorm.containers import RedisInt


class TestModel(Model):
    num = IntField()


class MyTestCase(testing.AsyncTestCase):
    @testing.gen_test
    def test_model_create(self):
        t = TestModel(num=1)
        self.assertEqual(t.num, 1)
        self.assertTrue(isinstance(t.num, RedisInt))

        f = TestModel(_id=1, num=2)
        self.assertEqual(f.redis_key(), u'TestModel:1')
        self.assertEqual(f.num.redis_key(), u'TestModel:1:num')


def all():
    suites = []
    suites.append(unittest.TestLoader().loadTestsFromTestCase(MyTestCase))
    return unittest.TestSuite(suites)

if __name__ == '__main__':
    testing.main()
