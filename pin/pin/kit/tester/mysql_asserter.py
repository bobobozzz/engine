#!/usr/bin/env python3

#BoBoBo#

import pin.kit.db.mysql as mysql
from pin.kit.db.mysql import default_mysqlconf
from pin.kit.db.mysql import get_db


dbconf = default_mysqlconf()


def t(a):
    if not a:
        pytest.fail("None test target.")

    global dbconf
    try:
        asserter_param = a["param"]
        cfg = a["cfg"]
        dbconf["host"] = cfg["host"]
        dbconf["port"] = cfg["port"]
        dbconf["db"] = cfg["database"]
        dbconf["user"] = cfg["user"]
        dbconf["passwd"] = cfg["password"]
    except Exception as e:
        raise AssertionError("Invalid test yaml script: " + str(e))

    list(map(lambda k: assert_not_empty(
        asserter_param[k]) if "assert-not-empty" == k else None, asserter_param))


def get_dbconf():

    def _dbconf(section, key, default=None):
        global dbconf
        return dbconf.get(key, default)

    return _dbconf


def assert_not_empty(sql):
    if not sql:
        raise AssertionError("None sql to assert not empty.")
    db = get_db(get_dbconf())
    r = mysql.query(db, sql)
    assert not r is None and len(r) > 0
