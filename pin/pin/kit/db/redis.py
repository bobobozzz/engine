#!/usr/bin/env python3

#BoBoBo#

import redis
from pin.kit.common import get_conf


def default_redisconf():
    return {
        'host': 'localhost',
        'port': 6379,
        'max_connections': 1,
        'decode_responses': True
    }


def get_redis(conf=None):
    if not conf:
        conf = get_conf(None)

    def get_redisconf():
        nonlocal conf
        default = default_redisconf()
        redisconf = dict(
            map(lambda k: (k, conf('redis', k, None)), default.keys()))

        if redisconf['host'] is None:
            redisconf = default

        return redisconf

    def _get_redis():
        conn_pool = None
        redisconf = get_redisconf()

        def _get_conn():
            nonlocal redisconf
            nonlocal conn_pool
            if conn_pool is None:
                conn_pool = redis.ConnectionPool(**redisconf)
            conn = redis.Redis(connection_pool=conn_pool,
                               decode_responses=True)
            return conn

        return _get_conn

    return _get_redis()
