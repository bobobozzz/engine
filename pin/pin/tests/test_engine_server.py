#!/usr/bin/env python3

#BoBoBo#

import pytest
from threading import Thread
from pin.router import *
import pin.embed.engine_simular_server as server
import requests
import time

app = engine_app(pin_app(True))

test_str = "Hello Pin from embed server."
test_res = {"errCode": 0, "errMsg": None, "data": test_str}


@route("/pin/test/engine/hello_serv", response_json)
def hello(p1):
    global test_str
    print(str(p1))
    return test_res


class AppHandler(server.EngineHandler):
    def do_app(self, request):
        global app
        return app(request)


def test_server():
    global test_str

    def serve(host, port):
        server.serve(HandlerClass=AppHandler, port=port, bind=host)

    t = Thread(target=serve, args=('127.0.0.1',  8000), daemon=True)
    t.start()
    #serve('127.0.0.1',  8000)
    print("Waiting server start for 10 seconds...")
    time.sleep(10)
    param = {"p1": "v1"}
    resp = requests.get(
        'http://127.0.0.1:8000/pin/test/engine/hello_serv', params=param)
    r = resp.json()
    assert r == test_res
