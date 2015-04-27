#!/usr/bin/env python
# encoding: utf-8


from tornado import gen


class RedisContainer(object):

    def __init__(self, val=None):
        if val:
            self.set_value(val)

    def redis_key(self):
        return self._instance.delimiter.join([
            self._instance.redis_key(), self._field.name])

    @gen.coroutine
    def save(self, pipe):
        pipe.set(self.redis_key(), self._value)

    @gen.coroutine
    def load(self, pipe):
        pipe.get(self.redis_key())

    def set_value(self, val):
        self._value = self._type(val)


class Comparable(object):

    def __cmp__(self, other):
        return self._value.__cmp__(other)

    def __eq__(self, other):
        return self._value == other

    def __ge__(self, other):
        return self._value >= other

    def __gt__(self, other):
        return self._value > other

    def __le__(self, other):
        return self._value <= other

    def __lt__(self, other):
        return self._value < other

    def __ne__(self, other):
        return self._value != other


class RedisInt(Comparable, RedisContainer):
    _type = int

    def __abs__(self):
        return self._value.__abs__()

    def __add__(self, other):
        return self._value.__add__(other)

    def __and__(self, other):
        return self._value.__and__(other)

    def __bool__(self):
        # FIXME
        return bool(self._value)

    def __ceil__(self):
        return self._value.__ceil__()

    def __div__(self, other):
        return self._value.__div__(other)

    def __divmod__(self, other):
        return self._value.__divmod__(other)

    def __float__(self):
        return self._value.__float__()

    def __floor__(self):
        return self._value.__floor__()

    def __floordiv__(self, other):
        return self._value.__floordiv__(other)

    def __index__(self):
        return self._value.__index__()

    def __int__(self):
        return self._value.__int__()

    def __invert__(self):
        return self._value.__invert__()

    def __lshift__(self, other):
        return self._value.__lshift__(other)

    def __mod__(self, other):
        return self._value.__mod__(other)

    def __mul__(self, other):
        return self._value.__mul__(other)

    def __neg__(self):
        return self._value.__neg__()

    def __or__(self, other):
        return self._value.__or__(other)

    def __pos__(self):
        return self._value.__pos__()

    def __pow__(self, other):
        return self._value.__pow__(other)

    def __radd__(self, other):
        return self._value.__radd__(other)

    def __rand__(self, other):
        return self._value.__rand__(other)

    def __rdivmod__(self, other):
        return self._value.__rdivmod__(other)

    def __rfloordiv__(self, other):
        return self._value.__rfloordiv__(other)

    def __rlshift__(self, other):
        return self._value.__rlshift__(other)

    def __rmod__(self, other):
        return self._value.__rmod__(other)

    def __rmul__(self, other):
        return self._value.__rmul__(other)

    def __ror__(self, other):
        return self._value.__ror__(other)

    def __round__(self):
        return self._value.__round__()

    def __rpow__(self, other):
        return self._value.__rpow__(other)

    def __rrshift__(self, other):
        return self._value.__rrshift__(other)

    def __rshift__(self, other):
        return self._value.__rshift__(other)

    def __rsub__(self, other):
        return self._value.__rsub__(other)

    def __rtruediv__(self, other):
        return self._value.__rtruediv__(other)

    def __rxor__(self, other):
        return self._value.__rxor__(other)

    def __sub__(self, other):
        return self._value.__sub__(other)

    def __truediv__(self, other):
        print "called"
        return self._value.__truediv__(other)

    def __trunc__(self):
        return self._value.__trunc__()

    def __xor__(self, other):
        return self._value.__xor__(other)

    ######### magick methods end #########
