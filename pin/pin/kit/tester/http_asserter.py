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
    assert r == asserter_param
