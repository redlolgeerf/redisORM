#!/usr/bin/env python
# encoding: utf-8

import unittest
from tornado import testing, gen
from tornadoredis import Client

from redisorm.model import Model
from redisorm.fields import IntField, StrField
from redisorm.containers import RedisInt, RedisStr


class TestModel(Model):
    num = IntField()
    name = StrField()


class RedisMixin(object):

    def setUp(self, *args, **kwargs):
        super(RedisMixin, self).setUp(*args, **kwargs)
        self.conn = Client()
        self.conn.flushall()

    def tearDown(self, *args, **kwargs):
        super(RedisMixin, self).tearDown(*args, **kwargs)
        del self.conn


class MyTestCase(RedisMixin, testing.AsyncTestCase):
    @testing.gen_test
    def test_model_create(self):
        t = TestModel(num=1, name='Alice')
        self.assertEqual(t.num, 1)
        self.assertTrue(isinstance(t.num, RedisInt))
        self.assertEqual(t.name, 'Alice')
        self.assertTrue(isinstance(t.name, RedisStr))

        f = TestModel(_id=1, num=2, name='Bob')
        self.assertEqual(f.redis_key(), u'TestModel:1')
        self.assertEqual(f.num.redis_key(), u'TestModel:1:num')
        self.assertEqual(f.name.redis_key(), u'TestModel:1:name')

        z = TestModel(_id=2, num=3, name='Jane')
        yield z.save()

        d = yield TestModel.get_by_id(_id=2)
        self.assertEqual(d.num, 3)
        self.assertEqual(d.name, 'Jane')


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


class ExpirationTest(RedisMixin, testing.AsyncTestCase):
    def setUp(self):
        super(ExpirationTest, self).setUp()
        self.t = TestModel(_id=2, num=3, name='Alice')

    @testing.gen_test
    def test_expire(self):
        yield self.t.save()

        x = yield self.t.name.expire(20, conn=self.conn)
        self.assertEqual(x, 1)
        x = yield self.t.name.ttl(conn=self.conn)
        self.assertTrue(1 < x <= 20)
        x = yield self.t.name.persist(conn=self.conn)
        self.assertEqual(x, 1)
        x = yield self.t.name.ttl(conn=self.conn)
        self.assertEqual(x, None)  # this is how tornadoredis does things

        pipe = self.conn.pipeline()
        yield self.t.name.expire(20, pipe=pipe)
        x = yield gen.Task(pipe.execute)
        self.assertEqual(x, [True])  # this is awkward
        yield self.t.name.ttl(pipe=pipe)
        x = yield gen.Task(pipe.execute)
        self.assertTrue(1 < x[0] <= 20)
        yield self.t.name.persist(pipe=pipe)
        x = yield gen.Task(pipe.execute)
        self.assertEqual(x, [True])
        yield self.t.name.ttl(pipe=pipe)
        x = yield gen.Task(pipe.execute)
        self.assertEqual(x, [None])  # this is how tornadoredis does things


class RedisStrTest(RedisMixin, testing.AsyncTestCase):
    def setUp(self):
        super(RedisStrTest, self).setUp()
        self.t = TestModel(_id=2, num=3, name='Alice')

    @testing.gen_test
    def test_append(self):
        yield self.t.save()
        result = yield self.t.name.append(' Bob', conn=self.conn)
        self.assertEqual(self.t.name, 'Alice Bob')
        self.assertEqual(result, 9)
        d = yield TestModel.get_by_id(_id=2)
        self.assertEqual(d.name, 'Alice Bob')

        pipe = self.conn.pipeline()
        yield self.t.name.append(' Bob', pipe=pipe)
        result = yield gen.Task(pipe.execute)

        s = yield TestModel.get_by_id(_id=2)
        self.assertEqual(s.name, 'Alice Bob Bob')
        self.assertEqual(result, [13])

    def test_len(self):
        self.assertEqual(len(self.t.name), 5)

    def test_mul(self):
        self.assertEqual(self.t.name * 3, 'AliceAliceAlice')
        self.t.name *= 3
        self.assertEqual(self.t.name, 'AliceAliceAlice')

    def test_add(self):
        self.assertEqual(self.t.name + 'Bob', 'AliceBob')
        self.t.name += 'Bob'
        self.assertEqual(self.t.name, 'AliceBob')

    def test_contains(self):
        self.assertTrue('A' in self.t.name)

    def test_getslice(self):
        self.assertEqual(self.t.name[-3:-1], 'ic')

    def test_capitalize(self):
        self.assertEqual(self.t.name.capitalize(), 'Alice')

    def test_split(self):
        self.assertEqual(self.t.name.split('i'), ['Al', 'ce'])


class RedisIntTest(RedisMixin, testing.AsyncTestCase):
    def setUp(self):
        super(RedisIntTest, self).setUp()
        self.t = TestModel(_id=2, num=3, name='Alice')

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

    @testing.gen_test
    def test_incr(self):
        yield self.t.save()
        result = yield self.t.num.incr(conn=self.conn)
        self.assertEqual(self.t.num, 4)
        self.assertEqual(result, 4)
        d = yield TestModel.get_by_id(_id=2)
        self.assertEqual(d.num, 4)

        pipe = self.conn.pipeline()
        yield self.t.num.incr(pipe=pipe)
        result = yield gen.Task(pipe.execute)
        s = yield TestModel.get_by_id(_id=2)
        self.assertEqual(s.num, 5)
        self.assertEqual(self.t.num, 5)
        self.assertEqual(result, [5])

    @testing.gen_test
    def test_incrby(self):
        yield self.t.save()
        result = yield self.t.num.incrby(2, conn=self.conn)
        self.assertEqual(self.t.num, 5)
        d = yield TestModel.get_by_id(_id=2)
        self.assertEqual(d.num, 5)
        self.assertEqual(result, 5)

        pipe = self.conn.pipeline()
        yield self.t.num.incrby(10, pipe=pipe)
        result = yield gen.Task(pipe.execute)
        s = yield TestModel.get_by_id(_id=2)
        self.assertEqual(s.num, 15)
        self.assertEqual(self.t.num, 15)
        self.assertEqual(result, [15])

    @testing.gen_test
    def test_decr(self):
        yield self.t.save()
        result = yield self.t.num.decr(conn=self.conn)
        self.assertEqual(self.t.num, 2)
        d = yield TestModel.get_by_id(_id=2)
        self.assertEqual(d.num, 2)
        self.assertEqual(result, 2)

        pipe = self.conn.pipeline()
        yield self.t.num.decr(pipe=pipe)
        result = yield gen.Task(pipe.execute)
        s = yield TestModel.get_by_id(_id=2)
        self.assertEqual(s.num, 1)
        self.assertEqual(self.t.num, 1)
        self.assertEqual(result, [1])

    @testing.gen_test
    def test_decrby(self):
        yield self.t.save()
        result = yield self.t.num.decrby(2, conn=self.conn)
        self.assertEqual(self.t.num, 1)
        d = yield TestModel.get_by_id(_id=2)
        self.assertEqual(d.num, 1)
        self.assertEqual(result, 1)

        pipe = self.conn.pipeline()
        yield self.t.num.decrby(1, pipe=pipe)
        result = yield gen.Task(pipe.execute)
        s = yield TestModel.get_by_id(_id=2)
        self.assertEqual(s.num, 0)
        self.assertEqual(self.t.num, 0)
        self.assertEqual(result, [0])


def all():
    suites = []
    suites.append(unittest.TestLoader().loadTestsFromTestCase(MyTestCase))
    suites.append(unittest.TestLoader().loadTestsFromTestCase(ExpirationTest))
    suites.append(unittest.TestLoader().loadTestsFromTestCase(ComparableTest))
    suites.append(unittest.TestLoader().loadTestsFromTestCase(RedisIntTest))
    suites.append(unittest.TestLoader().loadTestsFromTestCase(RedisStrTest))
    return unittest.TestSuite(suites)

if __name__ == '__main__':
    testing.main()
