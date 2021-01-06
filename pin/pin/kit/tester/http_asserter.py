#!/usr/bin/env python3

#BoBoBo#

import pytest
import requests


def t(a):
    if not a:
        pytest.fail("None test target.")

    try:
        serv = a["serv"]
        asserter_param = a["param"]
        cfg = a["cfg"]

        baseURL = "http://" + cfg["host"] + ":" + str(cfg["port"])
        url = baseURL + serv["path"]
        request_param = serv["data"]
    except Exception as e:
        raise AssertionError("Invalid test yaml script: " + str(e))

    resp = requests.get(url, params=request_param)
    r = resp.json()
    assert assert_keys(asserter_param, r)


def assert_keys(d1, d2):
    if d1 == None and d2 != None:
        raise AssertionError("Not None: " + str(d2))

    if type(d1) == str:
        if d1 != "!!ignore!!":
            if d1 == d2:
                return True
            else:
                raise AssertionError("Different string: " + d2)
        else:
            return True
    else:
        if type(d1) != type(d2):
            raise AssertionError("Different type: " + str(d2))

        if type(d1) == list:
            return assert_keys(d1[0], d2[0])

        if type(d1) != dict:
            if d1 == d2:
                return True
            else:
                raise AssertionError("Different value: " + str(d2))
        else:
            for k in d1:
                if k not in d2:
                    raise AssertionError("No key: " + k)
                assert_keys(d1[k], d2[k])
            return True
