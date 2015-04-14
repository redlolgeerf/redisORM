#!/usr/bin/env python
# encoding: utf-8


from tornado import gen
from redisorm.containers import RedisInt


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
        instance._data[self.name] = self._container(value)
        instance._data[self.name]._instance = instance
        instance._data[self.name]._field = self


class IntField(Field):
    _container = RedisInt
