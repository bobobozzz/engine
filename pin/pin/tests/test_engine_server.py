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
def hello(auth, p1):
    global test_str
    print(str(auth))
    print(str(p1))
    return test_res


class AppHandler(server.EngineHandler):
    def do_app(self, request):
        global app
        return app(request)


@pytest.fixture(scope='module', autouse=True)
def start_server():
    def serve(host, port):
        server.serve(HandlerClass=AppHandler, port=port, bind=host)

    t = Thread(target=serve, args=('127.0.0.1',  8000), daemon=True)
    t.start()
    print("Waiting server start for 5 seconds...")
    time.sleep(5)


def test_server():
    global test_str

    headers = {'Auth-Token': 'abc'}
    param = {"p1": "v1"}
    try:
        resp = requests.get(
            'http://127.0.0.1:8000/pin/test/engine/hello_serv', params=param, headers=headers)
        r = resp.json()
    except Exception as e:
        #pytest.fail('Error: ' + str(e))
        print('Error')
    else:
        assert r == test_res


def test_post():
    global test_str

    headers = {'Auth-Token': 'abc'}
    param = {"p1": "v1"}
    try:
        resp = requests.post(
            'http://127.0.0.1:8000/pin/test/engine/hello_serv', json=param, headers=headers)
        r = resp.json()
    except Exception as e:
        #pytest.fail('Error: ' + str(e))
        print('Error')
    else:
        assert r == test_res
