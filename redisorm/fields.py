#!/usr/bin/env python
# encoding: utf-8


from tornado import gen
from redisorm.containers import RedisInt, RedisStr


class Field(object):

    def __init__(self, *args, **kwargs):
        self._value = None
        for k, v in kwargs.items():
            setattr(self, k, v)

    def add_to_class(self, model_class, name):
        self.model_class = model_class
        self.name = name
        setattr(model_class, name, self)

    def __get__(self, instance, instance_type=None):
        if instance is not None:
            return instance._data[self.name]
        return self

    def __set__(self, instance, value):
        if self.name not in instance._data:
            instance._data[self.name] = self._container(value)
            instance._data[self.name]._instance = instance
            instance._data[self.name]._field = self
        else:
            instance._data[self.name].set_value(value)

    @gen.coroutine
    def load(self, instance, pipe):
        container = self._container()
        container._instance = instance
        container._field = self
        yield container.load(pipe)

    @gen.coroutine
    def save(self, instance, pipe):
        yield instance._data[self.name].save(pipe)


class StrField(Field):
    _container = RedisStr


class IntField(Field):
    _container = RedisInt
