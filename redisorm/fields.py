#!/usr/bin/env python
# encoding: utf-8


class Field(object):

    def __init__(self, *args, **kwargs):
        self._value = None
        for k, v in kwargs.items():
            setattr(self, k, v)

    def assign_value(self, value):
        self._value = self._coerce(value)
        return self

    def add_to_class(self, model_class, name):
        self.model_class = model_class
        self.name = name
        setattr(model_class, name, self)

    def __get__(self, instance, instance_type=None):
        if instance is not None:
            return self._value
        return self

    def __set__(self, instance, value):
        instance._value = value


class IntField(Field):
    _coerce = int


class SetField(Field):
    _coerce = set
