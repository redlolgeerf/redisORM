#!/usr/bin/env python
# encoding: utf-8


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

    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            if k in self._fields:
                v = self._fields[k].assign_value(v)
            setattr(self, k, v)