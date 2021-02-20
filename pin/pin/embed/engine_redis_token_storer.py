#!/usr/bin/env python3

#BoBoBo#

from pin.kit.db.redis import get_redis


redis = get_redis()


def get_auth_str(token):
    if None is token or '' == token:
        return None
    return redis.get(token)
