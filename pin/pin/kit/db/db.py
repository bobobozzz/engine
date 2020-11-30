#!/usr/bin/env python3

#BoBoBo#

import configparser
import abc
import os
import collections
from dbutils.pooled_db import PooledDB
import pymysql


def get_db(creator, get_conf):
    conn_pool = None

    def _get_conn():
        nonlocal conn_pool
        if None is conn_pool:
            conn_pool = init_db(creator, get_conf)
        return conn_pool.connection()

    return _get_conn


def default_dbconf():
    dbconf = {}

    dbconf['creator'] = pymysql
    dbconf['host'] = 'localhost'
    dbconf['port'] = 3306
    dbconf['name'] = 'db_test'
    dbconf['user'] = 'test'
    dbconf['passwd'] = 'test'
    dbconf['mincached'] = 1
    dbconf['maxcached'] = 1
    dbconf['maxconnections'] = 1
    dbconf['maxshared'] = 1
    dbconf['blocking'] = 1
    dbconf['ping'] = 'select 1'

    return dbconf


def init_db(creator, get_dbconf):
    dbconf = get_dbconf()
    dbconf['creator'] = creator
    return build_conn_pool(dbconf)


def build_conn_pool(dbconf):
    conn_pool = PooledDB(creator=dbconf['creator'],
                         host=dbconf['host'],
                         port=dbconf['port'],
                         db=dbconf['name'],
                         user=dbconf['user'],
                         passwd=dbconf['passwd'],
                         mincached=dbconf['mincached'],
                         maxcached=dbconf['maxcached'],
                         maxconnections=dbconf['maxconnections'],
                         maxshared=dbconf['maxshared'],
                         blocking=dbconf['blocking'],
                         ping=dbconf['ping'])
    return conn_pool


db_conf_keys = ['host', 'port', 'name', 'user', 'passwd', 'mincached',
                'maxcached', 'maxconnections', 'maxshared', 'blocking', 'ping']


def get_dbconf_from(conf, section):
    db_conf_values = list(map(lambda k: conf.get(
        section, k, fallback=None), db_conf_keys))
    db_conf_values = list(
        map(lambda s: int(s) if s.isnumeric() else s, db_conf_values))
    return build_dbconf(db_conf_values)


def build_dbconf(db_conf_values):
    return dict(zip(db_conf_keys, db_conf_values))


def execute(conn, sqls, auto_commit=True, auto_close=True, hook_cur=None):
    if None is conn:
        return None

    cur = None
    try:
        cur = conn.cursor()
        ret = []
        for tp in sqls:
            if tp[1]:
                cur.execute(tp[0], tp[1])
                if hook_cur:
                    ret.append(hook_cur(cur))
            else:
                cur.execute(tp[0])
                if hook_cur:
                    ret.append(hook_cur(cur))
        if auto_commit:
            conn.commit()
        return conn, cur, ret
    except Exception as e:
        if auto_commit and conn:
            conn.rollback()
        raise e
    finally:
        if auto_close:
            if cur:
                cur.close()
            if auto_close and conn:
                conn.close()


def insert(conn, sqls, auto_close):
    def getlastid(cur):
        return cur.lastrowid()

    return execute(conn, sqls, hook_cur=getlastid, auto_close=auto_close)


def update(conn, sql, param, auto_close):
    sqls = [(sql, param)]
    return execute(conn, sqls, auto_close=auto_close)


def query(conn, sql, param, auto_close=True):
    def getall(cur):
        return (cur.fetchall(), cur.description)

    sqls = [(sql, param)]
    _, _, ret = execute(conn, sqls, hook_cur=getall)
    if ret:
        return convert_ret(ret[0][0], ret[0][1])
    else:
        return None


def convert_ret(res_all, description):
    rows = []
    if res_all is None:
        return rows
    for res in res_all:
        row = {}
        for i in range(len(description)):
            row[description[i][0]] = res[i]
        rows.append(row)
    return rows
