#!/usr/bin/env python3

#BoBoBo#

import redis
import pin.kit.util as util


def default_redisconf():
    return {
        'host': 'localhost',
        'port': 6379,
        'max_connections': 1,
        'decode_responses': True
    }


def get_redisconf():
    return util.conf['redis']


def get_redis():
    pool = None

    def get_conn():
        nonlocal pool
        if pool is None:
            redisconf = get_redisconf()
            if redisconf is None:
                redisconf = default_redisconf()
            pool = redis.ConnectionPool(**redisconf)
        conn = redis.Redis(connection_pool=pool, decode_responses=True)
        return conn

    return get_conn


def get(key):
    redis = get_redis()
    conn = redis()
    return conn.get(key)


def set(key, value):
    redis = get_redis()
    conn = redis()
    return conn.set(key, value)


def delete(key):
    redis = get_redis()
    conn = redis()
    return conn.delete(key)
