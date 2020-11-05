#!/usr/bin/env python3

#BoBoBo#

from pin.router import route
from pin.view import response_json

@route("/hello_pin/hello", response_json)
def hello(param):
    return response_json({"errCode":0, "errMsg":"", "content": "Hello Pin!"})
