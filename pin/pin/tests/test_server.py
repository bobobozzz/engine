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
