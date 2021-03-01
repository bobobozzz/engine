#!/usr/bin/env python3

#BoBoBo#

from pin.kit.db.redis import get_redis
from pin.kit.common import get_conf


redis = get_redis(get_conf('engine'))


def get_auth_str(token):
    if None is token or '' == token:
        return None
    return redis().get(token)
