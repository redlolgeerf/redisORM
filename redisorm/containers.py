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

    @gen.coroutine
    def db_operation(self, operation, pipe=None, conn=None):
        """
        Perform operation on db.

        :operation: tuple ('name_of_operation', 'args')
        """
        assert pipe or conn, 'Either pipe or conn shall be provided'
        if pipe:
            if len(operation) == 1:
                getattr(pipe, operation[0])(self.redis_key())
            else:
                getattr(pipe, operation[0])(self.redis_key(), operation[1])
            raise gen.Return(pipe)
        if conn:
            x = getattr(conn, operation[0])
            if len(operation) == 1:
                result = yield gen.Task(x, self.redis_key())
            else:
                result = yield gen.Task(x, self.redis_key(), operation[1])
            raise gen.Return(result)

    def __repr__(self):
        return "{}({})".format(type(self).__name__, self._value)


class Expirable(object):
    """
    Mixin to provide expiration functionality.
    """
    @gen.coroutine
    def persist(self, *args, **kwargs):
        """
        Turn the key back into a persistent key.
        """
        result = yield self.db_operation(('persist', ), *args, **kwargs)
        raise gen.Return(result)

    @gen.coroutine
    def expire(self, seconds, *args, **kwargs):
        """
        Set a timeout on key.
        """
        result = yield self.db_operation(('expire', seconds), *args, **kwargs)
        raise gen.Return(result)

    @gen.coroutine
    def ttl(self, *args, **kwargs):
        """
        Get a timeout on key.
        """
        result = yield self.db_operation(('ttl', ), *args, **kwargs)
        raise gen.Return(result)


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


class RedisStr(Comparable, Expirable, RedisContainer):
    _type = str

    @gen.coroutine
    def append(self, increment, *args, **kwargs):
        """
        APPEND key value Append a value to a key
        """
        self._value += increment
        result = yield self.db_operation(('append', increment), *args, **kwargs)
        raise gen.Return(result)

    def __add__(self, other):
        return self._value.__add__(other)

    def __len__(self):
        return self._value.__len__()

    def __mul__(self, multiplier):
        return self._value.__mul__(multiplier)

    def __contains__(self, substr):
        return substr in self._value

    def __getslice__(self, *args, **kwargs):
        return self._value.__getslice__(*args, **kwargs)

    def capitalize(self, *args, **kwargs):
        return self._value.capitalize(*args, **kwargs)

    def center(self, *args, **kwargs):
        return self._value.center(*args, **kwargs)

    def count(self, *args, **kwargs):
        return self._value.count(*args, **kwargs)

    def decode(self, *args, **kwargs):
        return self._value.decode(*args, **kwargs)

    def encode(self, *args, **kwargs):
        return self._value.encode(*args, **kwargs)

    def endswith(self, *args, **kwargs):
        return self._value.endswith(*args, **kwargs)

    def expandtabs(self, *args, **kwargs):
        return self._value.expandtabs(*args, **kwargs)

    def find(self, *args, **kwargs):
        return self._value.find(*args, **kwargs)

    def format(self, *args, **kwargs):
        return self._value.format(*args, **kwargs)

    def index(self, *args, **kwargs):
        return self._value.index(*args, **kwargs)

    def isalnum(self, *args, **kwargs):
        return self._value.isalnum(*args, **kwargs)

    def isalpha(self, *args, **kwargs):
        return self._value.isalpha(*args, **kwargs)

    def isdigit(self, *args, **kwargs):
        return self._value.isdigit(*args, **kwargs)

    def islower(self, *args, **kwargs):
        return self._value.islower(*args, **kwargs)

    def isspace(self, *args, **kwargs):
        return self._value.isspace(*args, **kwargs)

    def istitle(self, *args, **kwargs):
        return self._value.istitle(*args, **kwargs)

    def isupper(self, *args, **kwargs):
        return self._value.isupper(*args, **kwargs)

    def join(self, *args, **kwargs):
        return self._value.join(*args, **kwargs)

    def ljust(self, *args, **kwargs):
        return self._value.ljust(*args, **kwargs)

    def lower(self, *args, **kwargs):
        return self._value.lower(*args, **kwargs)

    def lstrip(self, *args, **kwargs):
        return self._value.lstrip(*args, **kwargs)

    def partition(self, *args, **kwargs):
        return self._value.partition(*args, **kwargs)

    def replace(self, *args, **kwargs):
        return self._value.replace(*args, **kwargs)

    def rfind(self, *args, **kwargs):
        return self._value.rfind(*args, **kwargs)

    def rindex(self, *args, **kwargs):
        return self._value.rindex(*args, **kwargs)

    def rjust(self, *args, **kwargs):
        return self._value.rjust(*args, **kwargs)

    def rpartition(self, *args, **kwargs):
        return self._value.rpartition(*args, **kwargs)

    def rsplit(self, *args, **kwargs):
        return self._value.rsplit(*args, **kwargs)

    def rstrip(self, *args, **kwargs):
        return self._value.rstrip(*args, **kwargs)

    def split(self, *args, **kwargs):
        return self._value.split(*args, **kwargs)

    def splitlines(self, *args, **kwargs):
        return self._value.splitlines(*args, **kwargs)

    def startswith(self, *args, **kwargs):
        return self._value.strip(*args, **kwargs)

    def strip(self, *args, **kwargs):
        return self._value.strip(*args, **kwargs)

    def swapcase(self, *args, **kwargs):
        return self._value.swapcase(*args, **kwargs)

    def title(self, *args, **kwargs):
        return self._value.title(*args, **kwargs)

    def translate(self, *args, **kwargs):
        return self._value.translate(*args, **kwargs)

    def upper(self, *args, **kwargs):
        return self._value.upper(*args, **kwargs)

    def zfill(self, *args, **kwargs):
        return self._value.zfill(*args, **kwargs)


class RedisInt(Comparable, Expirable, RedisContainer):
    _type = int

    @gen.coroutine
    def incr(self, *args, **kwargs):
        self._value += 1
        result = yield self.db_operation(('incr', ), *args, **kwargs)
        raise gen.Return(result)

    @gen.coroutine
    def incrby(self, increment, *args, **kwargs):
        self._value += increment
        result = yield self.db_operation(('incrby', increment), *args, **kwargs)
        raise gen.Return(result)

    @gen.coroutine
    def decr(self, *args, **kwargs):
        self._value -= 1
        result = yield self.db_operation(('decr', ), *args, **kwargs)
        raise gen.Return(result)

    @gen.coroutine
    def decrby(self, decrement, *args, **kwargs):
        self._value -= decrement
        result = yield self.db_operation(('decrby', decrement), *args, **kwargs)
        raise gen.Return(result)

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
        return self._value.__truediv__(other)

    def __trunc__(self):
        return self._value.__trunc__()

    def __xor__(self, other):
        return self._value.__xor__(other)
