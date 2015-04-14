#!/usr/bin/env python
# encoding: utf-8


class RedisContainer(object):

    def __init__(self, *args, **kwargs):
        super(RedisContainer, self).__init__(*args, **kwargs)

class RedisInt(RedisContainer, int):
    pass
