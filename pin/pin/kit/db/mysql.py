#!/usr/bin/env python3

#BoBoBo#

import os
import pymysql
from dbutils.pooled_db import PooledDB
import pin.kit.db.db as dbbase
from pin.kit.common import get_conf


def default_mysqlconf():
    return {
        'creator': pymysql,
        'host': 'localhost',
        'port': 3306,
        'db': 'db_test',
        'user': 'test',
        'passwd': 'test',
        'mincached': 1,
        'maxcached': 1,
        'maxconnections': 1,
        'maxshared': 1,
        'blocking': 1,
        'ping': 'select 1'
    }


def get_db(conf=None):
    if not conf:
        conf = get_conf(None)

    def get_dbconf():
        nonlocal conf
        default = default_mysqlconf()
        dbconf = dict(
            map(lambda k: (k, conf('mysql', k, None)), default.keys()))

        if dbconf['host'] is None:
            dbconf = default
        else:
            dbconf['creator'] = pymysql
        return dbconf

    def get_db():
        conn_pool = None
        dbconf = get_dbconf()
        print('Use DB configuration: ' + str(dbconf))

        def _get_conn():
            nonlocal dbconf
            nonlocal conn_pool
            if conn_pool is None:
                conn_pool = PooledDB(**dbconf)
            return conn_pool.connection()

        return _get_conn

    return get_db()


def query(db, sql, param=None):
    conn = db()
    if conn:
        return dbbase.query(conn, sql, param)
    else:
        raise Exception("Failed to get db conn.")


def insert(db, sql, param=None):
    conn = db()
    if conn:
        sqls = [(sql, param)]
        return dbbase.insert(conn, sqls)
    else:
        raise Exception("Failed to get db conn.")


def execute(db, sql, param=None):
    conn = db()
    if conn:
        sqls = [(sql, param)]
        return dbbase.execute(conn, sqls)
    else:
        raise Exception("Failed to get db conn.")
