#!/usr/bin/env python3

#BoBoBo#

import os
import pymysql
import pin.kit.db.db as db
import pin.kit.util as util


def get_dbconf():
    return db.get_dbconf_from(util.conf, 'db')


def query(sql, param=None):
    get_dbconn = db.get_db(pymysql, get_dbconf)
    conn = get_dbconn()
    if conn:
        return db.query(conn, sql, param)
    else:
        raise Exception("Failed to get db conn.")
