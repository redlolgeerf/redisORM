#!/usr/bin/env python
# encoding: utf-8


from tornado import gen


class RedisContainer(object):

    def __init__(self, *args, **kwargs):
        super(RedisContainer, self).__init__(*args, **kwargs)

    def redis_key(self):
        return self._instance.delimiter.join([
            self._instance.redis_key(), self._field.name])

    @gen.coroutine
    def save(self, pipe):
        pipe.set(self.redis_key(), self)


class RedisInt(RedisContainer, int):
    pass
