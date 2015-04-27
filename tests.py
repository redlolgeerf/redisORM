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

        z = TestModel(_id=2, num=3)
        yield z.save()

        d = yield TestModel.get_by_id(_id=2)
        self.assertEqual(d.num, 3)


class ComparableTest(testing.AsyncTestCase):
    def setUp(self):
        super(ComparableTest, self).setUp()
        self.t = TestModel(num=1)

    def test_eq(self):
        self.assertTrue(self.t.num == 1)

    def test_ge(self):
        self.assertTrue(self.t.num >= 1)

    def test_gt(self):
        self.assertTrue(self.t.num > 0)

    def test_le(self):
        self.assertTrue(self.t.num <= 2)

    def test_lt(self):
        self.assertTrue(self.t.num < 3)

    def test_ne(self):
        self.assertTrue(self.t.num != 2)


class RedisIntTest(testing.AsyncTestCase):
    def setUp(self):
        super(RedisIntTest, self).setUp()
        self.t = TestModel(num=3)

    def test_abs(self):
        self.assertEqual(abs(self.t.num), 3)

    def test_add(self):
        x = self.t.num + 1
        self.assertEqual(x, 4)
        x = 1 + self.t.num
        self.assertEqual(x, 4)

    def test_sub(self):
        x = self.t.num - 1
        self.assertEqual(x, 2)
        x = 5 - self.t.num
        self.assertEqual(x, 2)

    def test_mul(self):
        x = self.t.num * 2
        self.assertEqual(x, 6)
        x = 2 * self.t.num
        self.assertEqual(x, 6)

    def test_floordiv(self):
        x = self.t.num // 2
        self.assertEqual(x, 1)

    def test_mod(self):
        x = self.t.num % 2
        self.assertEqual(x, 1)

    def test_divmod(self):
        self.assertEqual(divmod(self.t.num, 2), (1, 1))
        self.assertEqual(divmod(7, self.t.num), (2, 1))

    def test_pow(self):
        self.assertEqual(self.t.num ** 2, 9)

    def test_lshift(self):
        self.assertEqual(self.t.num << 2, 12)

    def test_rshift(self):
        self.assertEqual(self.t.num >> 2, 0)

    def test_and(self):
        self.assertEqual(self.t.num & 2, 2)

    def test_xor(self):
        self.assertEqual(self.t.num ^ 2, 1)

    def test_or(self):
        self.assertEqual(self.t.num | 2, 3)

    def test_div(self):
        self.assertEqual(self.t.num / 2, 1)
        self.assertEqual(self.t.num.__div__(2), 1)

    def test_truediv(self):
        self.assertEqual(self.t.num.__truediv__(2), 1.5)
        # TODO: add tests for binary operation


def all():
    suites = []
    suites.append(unittest.TestLoader().loadTestsFromTestCase(MyTestCase))
    suites.append(unittest.TestLoader().loadTestsFromTestCase(ComparableTest))
    suites.append(unittest.TestLoader().loadTestsFromTestCase(RedisIntTest))
    return unittest.TestSuite(suites)

if __name__ == '__main__':
    testing.main()
