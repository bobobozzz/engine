#!/usr/bin/env python3

#BoBoBo#

import os
import pymysql
import pin.kit.db.db as db

def get_dbconf():
    conf_file = os.environ['PIN_DB_CONF']
    return db.get_dbconf_from(conf_file, 'db')

def query(sql, param = None):
    get_dbconn = db.get_db(pymysql, get_dbconf)
    conn = get_dbconn()
    if conn:
        return db.query(conn, sql, param)
    else:
        raise Exception("Failed to get db conn.")
