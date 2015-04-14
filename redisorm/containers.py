#!/usr/bin/env python
# encoding: utf-8


class RedisContainer(object):

    def __init__(self, *args, **kwargs):
        super(RedisContainer, self).__init__(*args, **kwargs)

    def redis_key(self):
        return self._instance.delimiter.join([
            self._instance.redis_key(), self._field.name])


class RedisInt(RedisContainer, int):
    pass
