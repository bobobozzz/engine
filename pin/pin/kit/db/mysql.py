#!/usr/bin/env python3

#BoBoBo#

import os
import pymysql
import pin.kit.db.db as db
import pin.kit.util as util


def get_dbconf():
    return db.get_dbconf_from(util.conf, 'db')


def query(sql, param=None, get_conf=get_dbconf):
    get_dbconn = db.get_db(pymysql, get_conf)
    conn = get_dbconn()
    if conn:
        return db.query(conn, sql, param)
    else:
        raise Exception("Failed to get db conn.")


def insert(sql, param=None, get_conf=get_dbconf):
    get_dbconn = db.get_db(pymysql, get_conf)
    conn = get_dbconn()
    if conn:
        sqls = [(sql, param)]
        return db.insert(conn, sqls)
    else:
        raise Exception("Failed to get db conn.")


def execute(sql, param=None, get_conf=get_dbconf):
    get_dbconn = db.get_db(pymysql, get_conf)
    conn = get_dbconn()
    if conn:
        sqls = [(sql, param)]
        return db.execute(conn, sqls)
    else:
        raise Exception("Failed to get db conn.")
