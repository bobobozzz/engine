#!/usr/bin/env python3

#BoBoBo#

from pin.controller import route
from pin.view import render_json

@route("/engine_example/hello", render_json)
def hello(param):
    return response_json(0, '', {"content": "Hello Engine!"})
