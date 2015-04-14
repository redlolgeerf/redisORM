#!/usr/bin/env python
# encoding: utf-8


from uuid import uuid4
from tornado import gen
from tornadoredis import Client
from redisorm.fields import Field


class BaseModel(type):
    """
    MetaClass, which gathers fields to private attribute.
    """
    def __new__(cls, name, bases, attrs):
        model_class = super(BaseModel, cls).__new__(cls, name, bases, attrs)

        fields = {}
        for key, value in model_class.__dict__.items():
            if isinstance(value, Field):
                value.add_to_class(model_class, key)
                fields[key] = value

        model_class._fields = fields
        return model_class


def _with_metaclass(meta, base=object):
    return meta("NewBase", (base,), {'database': None, 'namespace': None})


class Model(_with_metaclass(BaseModel)):
    """
    Provides machinery of populating fields.
    """

    delimiter = u':'

    def __init__(self, _id=None, *args, **kwargs):
        self._data = {}
        self._id = _id or uuid4()
        for k, v in kwargs.items():
            setattr(self, k, v)

    def redis_key(self):
        return self.delimiter.join([type(self).__name__, str(self._id)])

    @gen.coroutine
    def save(self, pipe=None):
        if pipe is None:
            conn = Client()
            _pipe = conn.pipeline()
        else:
            _pipe = pipe
        for k, field in self._fields.items():
            yield field.save(self, _pipe)
        if pipe is None:
            yield gen.Task(_pipe.execute)

    @classmethod
    @gen.coroutine
    def get_by_id(cls, _id):
        instance = cls(_id=_id)
        yield instance.load()
        raise gen.Return(instance)

    @gen.coroutine
    def load(self):
        conn = Client()
        pipe = conn.pipeline()
        fields = []
        for k, field in self._fields.items():
            yield field.load(self, pipe)
            fields.append(k)
        results = yield gen.Task(pipe.execute)
        for i, field in enumerate(fields):
            setattr(self, field, results[i])
