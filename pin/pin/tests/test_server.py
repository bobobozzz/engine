#!/usr/bin/env python3

#BoBoBo#

import pytest
from threading import Thread
from pin.router import *
import pin.embed.server as server
import requests
import time

test_str = "Hello Pin from embed server."


@route("/pin/test/hello_serv", response_json)
def hello(p1):
    global test_str
    print(str(p1))
    return {"errCode": 0, "errMsg": "", "content": test_str}


@route("/pin/test/exception", response_json)
def exception():
    raise Exception("Test exception message.")


@route("/pin/test/hello_serv_post")
def hello_post(p1, p2):
    global test_str
    print(str(p1) + " & " + str(p2))
    return {"errCode": 0, "errMsg": "", "content": test_str}


app = pin_app(True)


def test_server():
    global test_str
    global app
    t = Thread(target=server.bootstrap, args=(app,), daemon=True)
    t.start()

    print("Waiting server start for 10 seconds...")
    time.sleep(10)
    param = {"p1": "v1"}
    resp = requests.get(
        'http://localhost:8080/pin/test/hello_serv', params=param)
    r = resp.json()
    assert r["content"] == test_str

    resp = requests.get(
        'http://localhost:8080/pin/test/exception')
    r = resp.json()
    assert r["errCode"] == -500
    assert r["errMsg"] == "Test exception message."

    param = {"p1": "post1", "p2": {"p2k1": 1, "p2k2": [1, 2]}}
    resp = requests.post(
        'http://localhost:8080/pin/test/hello_serv_post', json=param)
    r = resp.json()
    assert r["content"] == test_str
