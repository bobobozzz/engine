#!/usr/bin/env python3

#BoBoBo#

import os
import pymysql
from dbutils.pooled_db import PooledDB
import pin.kit.db.db as db
import pin.kit.util as util


def default_mysqlconf():
    return {
        'creator': pymysql,
        'host': 'localhost',
        'port': 3306,
        'name': 'db_test',
        'user': 'test',
        'passwd': 'test',
        'mincached': 1,
        'maxcached': 1,
        'maxconnections': 1,
        'maxshared': 1,
        'blocking': 1,
        'ping': 'select 1'
    }


def get_mysqlconf():
    try:
        return util.conf['mysql']
    except KeyError:
        return None


def get_db():
    conn_pool = None

    def _get_conn():
        nonlocal conn_pool
        if conn_pool is None:
            conn_pool = init_db()
        return conn_pool.connection()

    return _get_conn


def init_db():
    dbconf = get_mysqlconf()
    if dbconf is None:
        dbconf = default_mysqlconf()
    else:
        dbconf['creator'] = pymysql
    return PooledDB(**dbconf)


db_mysql = get_db()


def query(sql, param=None):
    conn = db_mysql()
    if conn:
        return db.query(conn, sql, param)
    else:
        raise Exception("Failed to get db conn.")


def insert(sql, param=None):
    conn = db_mysql()
    if conn:
        sqls = [(sql, param)]
        return db.insert(conn, sqls)
    else:
        raise Exception("Failed to get db conn.")


def execute(sql, param=None):
    conn = db_mysql()
    if conn:
        sqls = [(sql, param)]
        return db.execute(conn, sqls)
    else:
        raise Exception("Failed to get db conn.")
