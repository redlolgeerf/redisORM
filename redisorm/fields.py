#!/usr/bin/env python
# encoding: utf-8


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
        instance._data[self.name] = value


class IntField(Field):
    pass
