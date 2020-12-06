#!/usr/bin/env python3

#BoBoBo#

import redis
from pin.kit.util import get_section


def default_redisconf():
    return {
        'host': 'localhost',
        'port': 6379,
        'max_connections': 1,
        'decode_responses': True
    }


def get_redisconf():
    return get_section('redis')


def get_redis(redisconf):
    pool = None

    def get_conn():
        nonlocal redisconf
        nonlocal pool
        if pool is None:
            pool = redis.ConnectionPool(**redisconf)
        conn = redis.Redis(connection_pool=pool, decode_responses=True)
        return conn

    return get_conn


def init_redis():
    redisconf = get_redisconf()
    if redisconf is None:
        redisconf = default_redisconf()
    return redisconf


db_redis = get_redis(init_redis())


def reset_db(dbconf):
    global db_redis
    db_redis = get_redis(dbconf)


def get(key):
    global db_redis
    conn = db_redis()
    return conn.get(key)


def set(key, value):
    global db_redis
    conn = db_redis()
    return conn.set(key, value)


def delete(key):
    global db_redis
    conn = db_redis()
    return conn.delete(key)
