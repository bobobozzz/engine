#!/usr/bin/env python3

#BoBoBo#

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

def dispatch(url, param):
    action = urls.get(url)
    if None is action:
        render_404()
    return action(param)

urls, route = app()
