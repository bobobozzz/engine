#!/usr/bin/env python3

#BoBoBo#

import json
from http import HTTPStatus
from functools import wraps
from pin.view import render_404

def app():
    url_map={}

    def route(url, render):
        def wrapper_a(func):
            def wrapper_b(*args):
                return render(func(*args))

            url_map[url] = wrapper_b
            return wrapper_b
        return wrapper_a
    return url_map, route

def dispatch(request):
    path = request['path']
    action = urls.get(path)
    if None is action:
        return render_404()
    else:
        #TODO: check content-type and parse param
        body = request['body']
        param = json.loads(body)
        return action(param)

urls, route = app()
