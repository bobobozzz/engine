#!/usr/bin/env python3

#BoBoBo#


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


def insert(conn, sqls, auto_close=True):
    def getlastid(cur):
        return cur.lastrowid

    return execute(conn, sqls, hook_cur=getlastid, auto_close=auto_close)


def update(conn, sql, param, auto_close=True):
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
