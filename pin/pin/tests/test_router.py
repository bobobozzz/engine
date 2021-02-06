#!/usr/bin/env python3

#BoBoBo#

from pin.router import *

app = pin_app(True)


def response_(src):
    res = {}
    res['headers'] = []
    res['headers'].append(('Content-Type', 'text/plain;charset=utf-8'))
    res['status'] = '200 OK'
    res['content'] = src
    return res


@route("/pin/test/hello", response_)
def hello(param):
    print(param)
    return "Hello Pin!"


def test_dispatch():
    request = {}
    request['PATH_INFO'] = '/pin/test/hello'
    request['REQUEST_METHOD'] = 'GET'
    request['QUERY_STRING'] = 'param=testparam'

    response = dispatch(request)
    assert response['content'] == "Hello Pin!"


def test_controller_param():
    hello(100)
